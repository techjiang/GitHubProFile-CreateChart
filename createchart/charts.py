"""SVG chart builders for CreateChart."""

from __future__ import annotations

from collections import Counter
from html import escape
from typing import Dict, Iterable, List, Tuple

PALETTE = [
    "#6366f1", "#22d3ee", "#34d399", "#fbbf24",
    "#fb7185", "#a78bfa", "#f472b6", "#94a3b8",
]

LANGUAGE_LABELS = {
    "zh": {
        "profile_title": "GitHub 概览",
        "repos_title": "热门仓库",
        "languages_title": "语言分布",
        "followers": "关注者",
        "following": "正在关注",
        "public_repos": "公开仓库",
        "total_stars": "累计星标",
        "no_language_data": "暂无语言数据",
        "no_repositories": "暂无仓库数据",
        "bytes": "字节",
        "preview_title": "CreateChart · 预览",
        "preview_eyebrow": "实时 SVG 图表",
        "preview_heading": "CreateChart 预览",
        "preview_subtitle": "GitHub 主页统计 · 离线演示 · 第 1 轮：统一卡片描边与标题层级",
        "profile_section": "01 / 个人概览",
        "repos_section": "02 / 仓库排行",
        "languages_section": "03 / 语言分布",
        "preview_footer": "由 CreateChart 在本地生成 · 纯 SVG · 中英文标签可切换 · 第 5 轮收尾 · 可直接用于 GitHub Profile README。",
    },
    "en": {
        "profile_title": "GitHub overview",
        "repos_title": "Top repositories",
        "languages_title": "Languages",
        "followers": "Followers",
        "following": "Following",
        "public_repos": "Public repos",
        "total_stars": "Total stars",
        "no_language_data": "No language data",
        "no_repositories": "No repositories",
        "bytes": "bytes",
        "preview_title": "CreateChart · Preview",
        "preview_eyebrow": "Live SVG charts",
        "preview_heading": "CreateChart preview",
        "preview_subtitle": "GitHub profile statistics · offline demo · another pass on clarity and detail",
        "profile_section": "01 / Profile",
        "repos_section": "02 / Repositories",
        "languages_section": "03 / Languages",
        "preview_footer": "Generated locally by CreateChart · pure SVG · switchable zh/en labels · ready for GitHub Profile README.",
    },
}

DEFAULT_LANG = "en"


def t(key: str, lang: str = DEFAULT_LANG) -> str:
    """Return a localized UI string with English fallback."""
    return LANGUAGE_LABELS.get(lang, LANGUAGE_LABELS[DEFAULT_LANG]).get(
        key, LANGUAGE_LABELS[DEFAULT_LANG].get(key, key)
    )


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
        f'<text x="18" y="29" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="14" font-weight="700" letter-spacing="0.3">{escape(title)}</text>',
        f'<line x1="18" y1="38" x2="{width - 18}" y2="38" stroke="url(#accent)" stroke-opacity="0.55"/>',
    ]


def _svg_footer(lines: List[str]) -> str:
    lines.append("</svg>")
    return "\n".join(lines)


def language_chart(languages: Dict[str, int], title: str | None = None, lang: str = DEFAULT_LANG) -> str:
    """Build a horizontal stacked bar chart of byte counts by language."""
    total = sum(v for v in languages.values() if v > 0)
    parts = _svg_header(title or t("languages_title", lang), 520, 120)
    if total == 0:
        parts.append(f'<text x="18" y="66" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12">{escape(t("no_language_data", lang))}</text>')
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
        parts.append(f'<rect x="{x:.2f}" y="44" width="{segment:.2f}" height="18" rx="3" fill="{color}" stroke="#0d1117" stroke-width="0.6"><title>{escape(lang)}: {value} {escape(t("bytes", lang))}</title></rect>')
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
        parts.append(f'<text x="{legend_x + 16:.2f}" y="{legend_y}" fill="#e6edf3" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12"><tspan fill="#a5b4fc" font-weight="700">{pct:.1f}%</tspan> {escape(lang)}</text>')
        legend_x += 20 + len(label) * 7
    return _svg_footer(parts)


def repo_bars(
    repos: Iterable[Dict[str, object]],
    metric: str = "stargazers_count",
    title: str | None = None,
    lang: str = DEFAULT_LANG,
) -> str:
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
    parts = _svg_header(title or t("repos_title", lang), width, height)
    if not ranked:
        parts.append(f'<text x="18" y="66" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12">{escape(t("no_repositories", lang))}</text>')
        return _svg_footer(parts)

    max_value = max(value for _, value in ranked) or 1
    bar_max = 300.0
    for idx, (name, value) in enumerate(ranked):
        y = 48 + idx * row_height
        bar = bar_max * value / max_value
        rank_color = PALETTE[idx % len(PALETTE)]
        parts.append(f'<circle cx="28" cy="{y + 8}" r="9" fill="{rank_color}" fill-opacity="0.18" stroke="{rank_color}" stroke-opacity="0.5"/>')
        parts.append(f'<text x="28" y="{y + 12}" text-anchor="middle" fill="#e6edf3" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10" font-weight="700">{idx + 1}</text>')
        parts.append(f'<text x="44" y="{y + 14}" fill="#c9d1d9" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12">{escape(name)}</text>')
        parts.append(f'<rect x="180" y="{y}" width="300" height="16" rx="3" fill="#ffffff" fill-opacity="0.04"/>')
        parts.append(f'<rect x="180" y="{y}" width="{bar:.2f}" height="16" rx="3" fill="url(#accent)"><title>{escape(name)}: {value}</title></rect>')
        parts.append(f'<text x="496" y="{y + 14}" text-anchor="end" fill="#e6edf3" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11" font-weight="700" font-feature-settings="tnum">{value:,}</text>')
    return _svg_footer(parts)


def profile_summary(user: Dict[str, object], repos: Iterable[Dict[str, object]], lang: str = DEFAULT_LANG) -> str:
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
    lines = _svg_header(f"{name} · {t('profile_title', lang)}", 520, 170)
    stats = [
        (t("followers", lang), followers),
        (t("following", lang), following),
        (t("public_repos", lang), public_repos),
        (t("total_stars", lang), total_stars),
    ]
    for idx, (label, value) in enumerate(stats):
        x = 16 + (idx % 2) * 252
        y = 60 + (idx // 2) * 62
        lines.append(f'<text x="{x}" y="{y}" fill="#a5b4fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11" font-weight="700" letter-spacing="0.8">{escape(label)}</text>')
        lines.append(f'<rect x="{x}" y="{y + 6}" width="220" height="32" rx="7" fill="#161b22" stroke="#30363d"/>')
        lines.append(f'<text x="{x + 12}" y="{y + 29}" fill="#e6edf3" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="24" font-weight="700" font-feature-settings="tnum">{value}</text>')
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


def demo_charts(lang: str = DEFAULT_LANG) -> Dict[str, str]:
    """Build sample charts for local preview without network access."""
    user, repos, languages = demo_data()
    return {
        "profile": profile_summary(user, repos, lang=lang),
        "repos": repo_bars(repos, lang=lang),
        "languages": language_chart(languages, lang=lang),
    }


def preview_html(charts: Dict[str, str], lang: str = DEFAULT_LANG) -> str:
    """Wrap generated SVG charts into a single standalone preview page."""
    title = escape(t("preview_title", lang))
    return f"""<!doctype html>
<html lang="{escape(lang)}">
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
      border: 1px solid #30363d; border-radius: 16px; transition: border-color .2s ease, transform .2s ease;
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
      font-size: 10px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
    }}
    .card:first-child {{ grid-column: 1 / -1; }}
    .card svg {{ display: block; width: 100%; height: auto; }}
    .card:hover {{ border-color: rgba(99, 102, 241, .72); box-shadow: 0 22px 52px rgba(0,0,0,.38), 0 0 0 1px rgba(99,102,241,.18); transform: translateY(-2px); }}
    .card svg text {{ paint-order: stroke; }}
    footer {{ margin-top: 22px; color: #6e7681; font-size: 12px; line-height: 1.6; }}
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
      <div class="eyebrow">{escape(t("preview_eyebrow", lang))}</div>
      <h1>{escape(t("preview_heading", lang))}</h1>
      <div class="subtitle">{escape(t("preview_subtitle", lang))}</div>
    </header>
    <section class="grid">
      <div class="card"><span class="section-label">{escape(t("profile_section", lang))}</span>{charts["profile"]}</div>
      <div class="card"><span class="section-label">{escape(t("repos_section", lang))}</span>{charts["repos"]}</div>
      <div class="card"><span class="section-label">{escape(t("languages_section", lang))}</span>{charts["languages"]}</div>
    </section>
    <footer>{escape(t("preview_footer", lang))}</footer>
  </main>
</body>
</html>
"""
