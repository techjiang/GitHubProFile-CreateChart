"""SVG chart builders for CreateChart."""

from __future__ import annotations

from collections import Counter
from html import escape
from typing import Dict, Iterable, List, Tuple

PALETTE = [
    "#6366f1", "#22d3ee", "#34d399", "#fbbf24",
    "#fb7185", "#a78bfa", "#f472b6", "#94a3b8",
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
        f'<rect x="0" y="0" width="{width}" height="1" fill="#ffffff" opacity="0.06"/>',
        f'<text x="16" y="28" fill="#e6edf3" font-family="sans-serif" font-size="15" font-weight="700" letter-spacing="0.2">{escape(title)}</text>',
        f'<line x1="16" y1="36" x2="{width - 16}" y2="36" stroke="#ffffff" stroke-opacity="0.08"/>',
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
    for tick in (0, 0.5, 1.0):
        tick_x = 16.0 + tick * bar_width
        parts.append(f'<line x1="{tick_x:.2f}" y1="42" x2="{tick_x:.2f}" y2="64" stroke="#ffffff" stroke-opacity="0.07"/>')
    for idx, (lang, value) in enumerate(sorted(languages.items(), key=lambda kv: -kv[1])):
        if value <= 0:
            continue
        segment = bar_width * value / total
        color = PALETTE[idx % len(PALETTE)]
        parts.append(f'<rect x="{x:.2f}" y="44" width="{segment:.2f}" height="18" rx="3" fill="{color}" stroke="#0d1117" stroke-width="0.6"><title>{escape(lang)}: {value} bytes</title></rect>')
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
        parts.append(f'<text x="{legend_x + 16:.2f}" y="{legend_y}" fill="#e6edf3" font-family="sans-serif" font-size="12"><tspan fill="#a5b4fc" font-weight="700">{pct:.1f}%</tspan> {escape(lang)}</text>')
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
        rank_color = PALETTE[idx % len(PALETTE)]
        parts.append(f'<circle cx="28" cy="{y + 8}" r="9" fill="{rank_color}" fill-opacity="0.18" stroke="{rank_color}" stroke-opacity="0.5"/>')
        parts.append(f'<text x="28" y="{y + 12}" text-anchor="middle" fill="#e6edf3" font-family="sans-serif" font-size="10" font-weight="700">{idx + 1}</text>')
        parts.append(f'<text x="44" y="{y + 14}" fill="#c9d1d9" font-family="sans-serif" font-size="12">{escape(name)}</text>')
        parts.append(f'<rect x="180" y="{y}" width="{bar:.2f}" height="16" rx="3" fill="url(#accent)"><title>{escape(name)}: {value}</title></rect>')
        parts.append(f'<text x="{190 + bar:.2f}" y="{y + 14}" fill="#8b949e" font-family="sans-serif" font-size="11" font-weight="700" font-feature-settings="tnum">{value:,}</text>')
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
        lines.append(f'<text x="{x}" y="{y}" fill="#a5b4fc" font-family="sans-serif" font-size="11" font-weight="700" letter-spacing="1">{escape(label).upper()}</text>')
        lines.append(f'<rect x="{x}" y="{y + 8}" width="220" height="34" rx="7" fill="#161b22" stroke="#30363d"/>')
        lines.append(f'<text x="{x + 12}" y="{y + 31}" fill="#e6edf3" font-family="sans-serif" font-size="24" font-weight="700" font-feature-settings="tnum">{value}</text>')
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
        {"name": "createchart", "stargazers_count": 980},
        {"name": "octokit.rb", "stargazers_count": 640},
    ]
    languages = {
        "Python": 182000, "TypeScript": 96500, "Go": 54300,
        "Rust": 32100, "Shell": 12400, "HTML": 6800,
    }
    return user, repos, languages


def demo_charts() -> Dict[str, str]:
    """Build sample charts for local preview without network access."""
    user, repos, languages = demo_data()
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
      min-height: 100vh;
      padding: 40px 24px 56px;
      background:
        radial-gradient(circle at 8% 0%, rgba(99, 102, 241, .28) 0, transparent 26%),
        radial-gradient(circle at 92% 6%, rgba(6, 182, 212, .18) 0, transparent 24%),
        linear-gradient(160deg, #111827 0%, #0b0f16 52%, #07090d 100%);
      color: #e6edf3;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    main {{ max-width: 1160px; margin: 0 auto; }}
    header {{ margin-bottom: 30px; padding: 0 4px 22px; border-bottom: 1px solid #30363d; }}
    .eyebrow {{
      display: inline-flex; align-items: center; gap: 8px;
      margin-bottom: 14px; padding: 5px 11px;
      border: 1px solid rgba(99, 102, 241, .45); border-radius: 999px;
      background: rgba(99, 102, 241, .12); color: #a5b4fc;
      font-size: 11px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
    }}
    .eyebrow::before {{
      content: ""; width: 7px; height: 7px; border-radius: 50%;
      background: #34d399; box-shadow: 0 0 0 4px rgba(52, 211, 153, .12);
    }}
    h1 {{ margin: 0 0 8px; font-size: 34px; line-height: 1.12; letter-spacing: -.02em; }}
    .subtitle {{ color: #8b949e; font-size: 14px; line-height: 1.6; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; align-items: start; }}
    .card {{
      position: relative; padding: 20px;
      border: 1px solid #30363d; border-radius: 16px;
      background: linear-gradient(145deg, rgba(22, 27, 34, .95), rgba(13, 17, 23, .88));
      box-shadow: 0 20px 45px rgba(0, 0, 0, .3);
      overflow: hidden;
    }}
    .card::before {{
      content: ""; position: absolute; inset: 0 0 auto; height: 2px;
      background: linear-gradient(90deg, #6366f1, #06b6d4, #10b981);
    }}
    .card .section-label {{
      display: block; margin: 0 0 12px; color: #6e7681;
      font-size: 10px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase;
    }}
    .card:first-child {{ grid-column: 1 / -1; }}
    .card svg {{ display: block; width: 100%; height: auto; }}
    footer {{ margin-top: 22px; color: #6e7681; font-size: 12px; }}
    @media (max-width: 900px) {{
      body {{ padding: 24px 16px 40px; }}
      h1 {{ font-size: 28px; }}
      .grid {{ grid-template-columns: 1fr; }}
      .card:first-child {{ grid-column: auto; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div class="eyebrow">Live SVG charts</div>
      <h1>CreateChart preview</h1>
      <div class="subtitle">GitHub profile statistics · offline demo · five more rounds of visual polish</div>
    </header>
    <section class="grid">
      <div class="card"><span class="section-label">01 / Profile</span>{charts["profile"]}</div>
      <div class="card"><span class="section-label">02 / Repositories</span>{charts["repos"]}</div>
      <div class="card"><span class="section-label">03 / Languages</span>{charts["languages"]}</div>
    </section>
    <footer>Generated locally by CreateChart · pure SVG · ready for GitHub Profile README.</footer>
  </main>
</body>
</html>
"""
