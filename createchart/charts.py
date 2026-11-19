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
        '<defs>',
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0%" stop-color="#111827"/>',
        '<stop offset="100%" stop-color="#0d1117"/>',
        '</linearGradient>',
        '<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">',
        '<stop offset="0%" stop-color="#6366f1"/>',
        '<stop offset="100%" stop-color="#06b6d4"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{width}" height="{height}" fill="url(#bg)" rx="12"/>',
        f'<rect x="0" y="0" width="4" height="{height}" fill="url(#accent)" rx="2"/>',
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
        parts.append(f'<rect x="{x:.2f}" y="44" width="{segment:.2f}" height="18" rx="3" fill="{color}"><title>{escape(lang)}: {value} bytes</title></rect>')
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
        parts.append(f'<rect x="180" y="{y}" width="{bar:.2f}" height="16" rx="3" fill="url(#accent)"><title>{escape(name)}: {value}</title></rect>')
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
        lines.append(f'<rect x="{x}" y="{y + 8}" width="220" height="34" rx="7" fill="#161b22" stroke="#30363d"/>')
        lines.append(f'<text x="{x + 12}" y="{y + 31}" fill="#e6edf3" font-family="sans-serif" font-size="24" font-weight="700">{value}</text>')
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



def demo_data() -> Tuple[Dict[str, object], List[Dict[str, object]], Dict[str, int]]:
    """Return sample data used by the offline preview."""
    user: Dict[str, object] = {
        "login": "octocat",
        "name": "The Octocat",
        "followers": 12840,
        "following": 92,
        "public_repos": 42,
    }
    repos: List[Dict[str, object]] = [
        {"name": "hello-world", "stargazers_count": 5820},
        {"name": "linguist", "stargazers_count": 4310},
        {"name": "hub", "stargazers_count": 3140},
        {"name": "gitignore", "stargazers_count": 2680},
        {"name": "git-consortium", "stargazers_count": 1490},
    ]
    languages = {"Python": 182000, "TypeScript": 96500, "Go": 54300, "Rust": 32100, "Shell": 12400}
    return user, repos, languages


def demo_charts() -> Dict[str, str]:
    """Build sample charts for local preview without network access."""
    user, repos, languages = demo_data()
    user = {
        "login": "octocat",
        "name": "The Octocat",
        "followers": 12840,
        "following": 92,
        "public_repos": 42,
    }
    repos = [
        {"name": "hello-world", "stargazers_count": 5820},
        {"name": "linguist", "stargazers_count": 4310},
        {"name": "hub", "stargazers_count": 3140},
        {"name": "gitignore", "stargazers_count": 2680},
        {"name": "git-consortium", "stargazers_count": 1490},
    ]
    languages = {"Python": 182000, "TypeScript": 96500, "Go": 54300, "Rust": 32100, "Shell": 12400}
    return {
        "profile": profile_summary(user, repos),
        "repos": repo_bars(repos),
        "languages": language_chart(languages, title="Language distribution"),
    }


def preview_html(charts: Dict[str, str]) -> str:
    """Wrap generated SVG charts into a single standalone preview page."""
    title = escape("CreateChart · Preview")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 32px 24px 48px;
      background: radial-gradient(circle at 15% 0%, #1f2937 0, #0b0f16 45%, #07090d 100%);
      color: #e6edf3;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    main {{ max-width: 1180px; margin: 0 auto; }}
    header {{ margin-bottom: 24px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; letter-spacing: .2px; }}
    .subtitle {{ color: #8b949e; font-size: 14px; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; align-items: start; }}
    .card {{
      padding: 18px;
      border: 1px solid #30363d;
      border-radius: 14px;
      background: rgba(13, 17, 23, .82);
      box-shadow: 0 16px 40px rgba(0, 0, 0, .28);
    }}
    .card:first-child {{ grid-column: 1 / -1; }}
    .card svg {{ display: block; width: 100%; height: auto; }}
    footer {{ margin-top: 20px; color: #6e7681; font-size: 12px; }}
    @media (max-width: 900px) {{ .grid {{ grid-template-columns: 1fr; }} .card:first-child {{ grid-column: auto; }} }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>CreateChart preview</h1>
      <div class="subtitle">GitHub profile statistics · offline demo</div>
    </header>
    <section class="grid">
      <div class="card">{charts["profile"]}</div>
      <div class="card">{charts["repos"]}</div>
      <div class="card">{charts["languages"]}</div>
    </section>
    <footer>Generated locally by CreateChart. SVG charts are ready for GitHub Profile README.</footer>
  </main>
</body>
</html>
"""
