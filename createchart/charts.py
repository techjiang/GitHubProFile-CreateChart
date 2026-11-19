"""SVG chart builders for CreateChart."""

from __future__ import annotations

from collections import Counter
from html import escape
from typing import Dict, Iterable, List, Tuple

PALETTE = [
    "#4f46e5", "#06b6d4", "#10b981", "#f59e0b",
    "#ef4444", "#8b5cf6", "#ec4899", "#64748b",
]


def _svg_header(title: str, width: int, height: int) -> List[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">',
        '<rect width="100%" height="100%" fill="#0d1117" rx="12"/>',
        f'<text x="16" y="28" fill="#e6edf3" font-family="sans-serif" font-size="16" font-weight="700">{escape(title)}</text>',
    ]


def _svg_footer(lines: List[str]) -> str:
    lines.append("</svg>")
    return "\n".join(lines)


def language_chart(languages: Dict[str, int], title: str = "Languages") -> str:
    """Build a horizontal stacked bar chart of byte counts by language."""
    total = sum(v for v in languages.values() if v > 0)
    parts = _svg_header(title, 520, 120)
    if total == 0:
        parts.append('<text x="16" y="64" fill="#8b949e" font-family="sans-serif" font-size="13">No language data</text>')
        return _svg_footer(parts)

    x = 16.0
    bar_width = 488.0
    for idx, (lang, value) in enumerate(sorted(languages.items(), key=lambda kv: -kv[1])):
        if value <= 0:
            continue
        segment = bar_width * value / total
        color = PALETTE[idx % len(PALETTE)]
        parts.append(f'<rect x="{x:.2f}" y="44" width="{segment:.2f}" height="18" fill="{color}"><title>{escape(lang)}: {value} bytes</title></rect>')
        x += segment

    legend_x = 16.0
    legend_y = 84.0
    for idx, (lang, value) in enumerate(sorted(languages.items(), key=lambda kv: -kv[1])[:5]):
        if value <= 0:
            continue
        color = PALETTE[idx % len(PALETTE)]
        pct = 100 * value / total
        label = f"{lang} {pct:.1f}%"
        parts.append(f'<rect x="{legend_x:.2f}" y="{legend_y - 10}" width="10" height="10" rx="2" fill="{color}"/>')
        parts.append(f'<text x="{legend_x + 16:.2f}" y="{legend_y}" fill="#c9d1d9" font-family="sans-serif" font-size="12">{escape(label)}</text>')
        legend_x += 20 + len(label) * 7
    return _svg_footer(parts)


def repo_bars(repos: Iterable[Dict[str, object]], metric: str = "stargazers_count", title: str = "Top repositories") -> str:
    """Build a bar chart ranking repositories by a numeric metric."""
    ranked: List[Tuple[str, int]] = []
    for repo in repos:
        name = str(repo.get("name", "unknown"))
        value = repo.get(metric, 0)
        try:
            ranked.append((name, int(value)))
        except (TypeError, ValueError):
            continue
    ranked = sorted(ranked, key=lambda kv: -kv[1])[:8]

    row_height = 30
    width = 560
    height = max(100, 60 + row_height * len(ranked))
    parts = _svg_header(title, width, height)
    if not ranked:
        parts.append('<text x="16" y="64" fill="#8b949e" font-family="sans-serif" font-size="13">No repositories</text>')
        return _svg_footer(parts)

    max_value = max(value for _, value in ranked) or 1
    bar_max = 300.0
    for idx, (name, value) in enumerate(ranked):
        y = 48 + idx * row_height
        bar = bar_max * value / max_value
        parts.append(f'<text x="16" y="{y + 14}" fill="#c9d1d9" font-family="sans-serif" font-size="12">{escape(name)}</text>')
        parts.append(f'<rect x="180" y="{y}" width="{bar:.2f}" height="16" rx="3" fill="{PALETTE[idx % len(PALETTE)]}"><title>{escape(name)}: {value}</title></rect>')
        parts.append(f'<text x="{190 + bar:.2f}" y="{y + 14}" fill="#8b949e" font-family="sans-serif" font-size="11">{value}</text>')
    return _svg_footer(parts)


def profile_summary(user: Dict[str, object], repos: Iterable[Dict[str, object]]) -> str:
    """Build a compact summary card for a GitHub user."""
    repo_list = list(repos)
    followers = int(user.get("followers") or 0)
    following = int(user.get("following") or 0)
    public_repos = int(user.get("public_repos") or len(repo_list))
    total_stars = 0
    for repo in repo_list:
        try:
            total_stars += int(repo.get("stargazers_count") or 0)
        except (TypeError, ValueError):
            pass

    name = str(user.get("name") or user.get("login") or "GitHub user")
    lines = _svg_header(f"{name} · GitHub overview", 520, 170)
    stats = [
        ("Followers", followers),
        ("Following", following),
        ("Public repos", public_repos),
        ("Total stars", total_stars),
    ]
    for idx, (label, value) in enumerate(stats):
        x = 16 + (idx % 2) * 252
        y = 62 + (idx // 2) * 52
        lines.append(f'<text x="{x}" y="{y}" fill="#8b949e" font-family="sans-serif" font-size="12">{escape(label)}</text>')
        lines.append(f'<text x="{x}" y="{y + 26}" fill="#e6edf3" font-family="sans-serif" font-size="24" font-weight="700">{value}</text>')
    return _svg_footer(lines)


def aggregate_languages(repos: Iterable[Dict[str, object]], languages_by_repo: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    """Sum language bytes across repositories."""
    total: Counter[str] = Counter()
    for repo in repos:
        name = str(repo.get("name", ""))
        for lang, value in languages_by_repo.get(name, {}).items():
            if isinstance(value, int) and value > 0:
                total[lang] += value
    return dict(total)
