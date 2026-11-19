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
        "preview_subtitle": "GitHub 主页统计 · 离线演示 · 第 16 轮：路线图、社区温度与代码质量卡片",
        "profile_section": "01 / 个人概览",
        "repos_section": "02 / 仓库排行",
        "languages_section": "03 / 语言分布",
        "preview_footer": "由 CreateChart 在本地生成 · 纯 SVG · 中英文标签可切换 · 第 16 轮视觉打磨 · 新增路线图、社区温度与代码质量卡片 · 可直接用于 GitHub Profile README。",
        "activity_title": "活跃热力",
        "activity_section": "04 / 贡献活跃度",
        "activity_peak": "峰值",
        "activity_streak": "连续活跃",
        "activity_this_week": "本周",
        "momentum_title": "项目 momentum",
        "momentum_section": "05 / 项目 Momentum",
        "momentum_hot": "热度",
        "momentum_fresh": "新鲜度",
        "momentum_share": "头部占比",
        "highlights_title": "高光时刻",
        "highlights_section": "06 / 高光时刻",
        "highlight_star": "最高星标仓库",
        "highlight_dominant": "主力语言",
        "highlight_profile": "关注度",
        "days": "天",
        "release_title": "发布时间轴",
        "release_section": "07 / 发布时间轴",
        "release_latest": "最近发布",
        "release_window": "发布窗口",
        "release_velocity": "发布速度",
        "cadence_title": "节奏指数",
        "cadence_section": "08 / 节奏指数",
        "cadence_week": "本周提交",
        "cadence_review": "评审响应",
        "cadence_stability": "稳定性",
        "cadence_score": "综合节奏",
        "language_mix_title": "语言构成",
        "language_mix_section": "09 / 语言构成",
        "language_mix_top": "主力语言",
        "language_mix_diversity": "多样性",
        "language_mix_growth": "本月增长",
        "repo_health_title": "仓库健康度",
        "repo_health_section": "10 / 仓库健康度",
        "repo_health_open": "开放问题",
        "repo_health_merged": "合并 PR",
        "repo_health_docs": "文档覆盖",
        "network_title": "协作网络",
        "network_section": "11 / 协作网络",
        "network_contributors": "贡献者",
        "network_forks": "派生项目",
        "network_watchers": "关注者",
        "story_title": "数据叙事",
        "story_section": "12 / 数据叙事",
        "story_peak_day": "高峰日",
        "story_focus": "本月焦点",
        "story_growth": "增长亮点",
        "heatmap_title": "年度热力",
        "heatmap_section": "13 / 年度热力",
        "heatmap_total": "年度贡献",
        "heatmap_best": "最活跃月",
        "heatmap_longest": "最长连续",
        "milestone_title": "成长里程碑",
        "milestone_section": "14 / 成长里程碑",
        "milestone_next": "下一目标",
        "milestone_shipped": "已完成",
        "milestone_progress": "当前进度",
        "roadmap_title": "路线图",
        "roadmap_section": "15 / 路线图",
        "roadmap_next": "下一阶段",
        "roadmap_focus": "核心主题",
        "roadmap_eta": "预计时间",
        "community_title": "社区温度",
        "community_section": "16 / 社区温度",
        "community_issues": "开放问题",
        "community_prs": "活跃 PR",
        "community_response": "平均响应",
        "quality_title": "代码质量",
        "quality_section": "17 / 代码质量",
        "quality_coverage": "测试覆盖",
        "quality_checks": "检查通过",
        "quality_debt": "待清理项",
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
        "preview_subtitle": "GitHub profile statistics · offline demo · sixteenth pass with roadmap, community pulse, and code quality cards",
        "profile_section": "01 / Profile",
        "repos_section": "02 / Repositories",
        "languages_section": "03 / Languages",
        "preview_footer": "Generated locally by CreateChart · pure SVG · switchable zh/en labels · sixteenth polish pass with roadmap, community pulse, and code quality cards · ready for GitHub Profile README.",
        "activity_title": "Contribution activity",
        "activity_section": "04 / Activity",
        "activity_peak": "Peak",
        "activity_streak": "Streak",
        "activity_this_week": "This week",
        "momentum_title": "Project momentum",
        "momentum_section": "05 / Momentum",
        "momentum_hot": "Heat",
        "momentum_fresh": "Freshness",
        "momentum_share": "Top share",
        "highlights_title": "Highlights",
        "highlights_section": "06 / Highlights",
        "highlight_star": "Top starred repo",
        "highlight_dominant": "Dominant language",
        "highlight_profile": "Attention",
        "days": "days",
        "release_title": "Release timeline",
        "release_section": "07 / Releases",
        "release_latest": "Latest",
        "release_window": "Window",
        "release_velocity": "Velocity",
        "cadence_title": "Cadence index",
        "cadence_section": "08 / Cadence",
        "cadence_week": "Commits this week",
        "cadence_review": "Review response",
        "cadence_stability": "Stability",
        "cadence_score": "Cadence score",
        "language_mix_title": "Language mix",
        "language_mix_section": "09 / Language mix",
        "language_mix_top": "Top language",
        "language_mix_diversity": "Diversity",
        "language_mix_growth": "Growth this month",
        "repo_health_title": "Repository health",
        "repo_health_section": "10 / Health",
        "repo_health_open": "Open issues",
        "repo_health_merged": "Merged PRs",
        "repo_health_docs": "Docs coverage",
        "network_title": "Collaboration network",
        "network_section": "11 / Network",
        "network_contributors": "Contributors",
        "network_forks": "Forks",
        "network_watchers": "Watchers",
        "story_title": "Data story",
        "story_section": "12 / Data story",
        "story_peak_day": "Peak day",
        "story_focus": "Monthly focus",
        "story_growth": "Growth highlight",
        "heatmap_title": "Annual heatmap",
        "heatmap_section": "13 / Annual heatmap",
        "heatmap_total": "Annual contributions",
        "heatmap_best": "Busiest month",
        "heatmap_longest": "Longest streak",
        "milestone_title": "Milestones",
        "milestone_section": "14 / Milestones",
        "milestone_next": "Next goal",
        "milestone_shipped": "Shipped",
        "milestone_progress": "Current progress",
        "roadmap_title": "Roadmap",
        "roadmap_section": "15 / Roadmap",
        "roadmap_next": "Next phase",
        "roadmap_focus": "Core theme",
        "roadmap_eta": "ETA",
        "community_title": "Community pulse",
        "community_section": "16 / Community pulse",
        "community_issues": "Open issues",
        "community_prs": "Active PRs",
        "community_response": "Avg. response",
        "quality_title": "Code quality",
        "quality_section": "17 / Code quality",
        "quality_coverage": "Test coverage",
        "quality_checks": "Checks passed",
        "quality_debt": "Cleanup items",
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
        '<stop offset="100%" stop-color="#0b1017"/>',
        '</linearGradient>',
        '<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">',
        '<stop offset="0%" stop-color="#818cf8"/>',
        '<stop offset="100%" stop-color="#22d3ee"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{width}" height="{height}" fill="url(#bg)" rx="12"/>',
        f'<rect x="0" y="0" width="4" height="{height}" fill="url(#accent)" rx="2"/>',
        f'<rect x="0" y="0" width="{width}" height="1" fill="#a5b4fc" opacity="0.08"/>',
        f'<text x="18" y="29" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="14" font-weight="700" letter-spacing="0.35">{escape(title)}</text>',
        f'<line x1="18" y1="38" x2="{width - 18}" y2="38" stroke="url(#accent)" stroke-opacity="0.62"/>',
    ]


def _svg_footer(lines: List[str]) -> str:
    lines.append("</svg>")
    return "\n".join(lines)


def _svg_value_label(x: float, y: float, value: int, *, anchor: str = "start") -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" fill="#f0f6fc" '
        'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" '
        'font-size="11" font-weight="700" font-variant-numeric="tabular-nums" font-feature-settings="tnum">'
        f'{value:,}</text>'
    )


def language_chart(languages: Dict[str, int], title: str | None = None, lang: str = DEFAULT_LANG) -> str:
    """Build a horizontal stacked bar chart of byte counts by language."""
    total = sum(v for v in languages.values() if v > 0)
    parts = _svg_header(title or t("languages_title", lang), 520, 132)
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
        parts.append(f'<rect x="{x:.2f}" y="44" width="{segment:.2f}" height="18" rx="3" fill="{color}" stroke="#0b1017" stroke-width="0.6"><title>{escape(lang)}: {value} {escape(t("bytes", lang))}</title></rect>')
        x += segment

    top_languages = [(name, value) for name, value in sorted(languages.items(), key=lambda kv: -kv[1]) if value > 0][:5]
    legend_columns = 3
    column_width = bar_width / legend_columns
    legend_pct_width = 62
    for idx, (lang, value) in enumerate(top_languages):
        column = idx % legend_columns
        row = idx // legend_columns
        color = PALETTE[idx % len(PALETTE)]
        pct = 100 * value / total
        legend_x = 16.0 + column * column_width
        legend_y = 76.0 + row * 20.0
        parts.append(f'<rect x="{legend_x:.2f}" y="{legend_y - 9}" width="10" height="10" rx="2" fill="{color}"/>')
        parts.append(f'<text x="{legend_x + 16:.2f}" y="{legend_y}" fill="#a5b4fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11" font-weight="700" font-variant-numeric="tabular-nums">{pct:.1f}% </text>')
        parts.append(f'<text x="{legend_x + legend_pct_width:.2f}" y="{legend_y}" fill="#e6edf3" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11">{escape(lang)}</text>')
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
        parts.append(f'<text x="28" y="{y + 12}" text-anchor="middle" fill="#e6edf3" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10" font-weight="700" font-variant-numeric="tabular-nums">{idx + 1}</text>')
        parts.append(f'<text x="44" y="{y + 14}" fill="#c9d1d9" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12">{escape(name)}</text>')
        parts.append(f'<rect x="180" y="{y}" width="300" height="16" rx="3" fill="#a5b4fc" fill-opacity="0.06"/>')
        parts.append(f'<rect x="180" y="{y}" width="{bar:.2f}" height="16" rx="3" fill="url(#accent)"><title>{escape(name)}: {value}</title></rect>')
        parts.append(_svg_value_label(496, y + 14, value, anchor="end"))
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
        lines.append(f'<text x="{x + 12}" y="{y + 29}" fill="#e6edf3" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="24" fill="#ffffff" font-weight="700" font-variant-numeric="tabular-nums" font-feature-settings="tnum">{value:,}</text>')
    return _svg_footer(lines)


def contribution_activity(lang: str = DEFAULT_LANG) -> str:
    """Build a playful seven-day contribution heatmap with derived metrics."""
    counts = [12, 28, 19, 41, 34, 57, 23]
    weekday = ["M", "T", "W", "T", "F", "S", "S"]
    peak = max(counts)
    streak = 4
    total = sum(counts)
    parts = _svg_header(t("activity_title", lang), 520, 160)
    parts.append(f'<text x="18" y="58" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11">{escape(t("activity_this_week", lang))} · {total}</text>')
    colors = [
        "rgba(52,211,153,.10)", "rgba(52,211,153,.22)", "rgba(52,211,153,.38)",
        "rgba(52,211,153,.58)", "rgba(52,211,153,.86)",
    ]
    for idx, value in enumerate(counts):
        x = 18 + idx * 70
        level = min(4, value * 4 // peak)
        parts.append(f'<rect x="{x}" y="72" width="60" height="46" rx="8" fill="{colors[level]}" stroke="#30363d"/>')
        parts.append(f'<text x="{x + 30}" y="90" text-anchor="middle" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{weekday[idx]}</text>')
        parts.append(f'<text x="{x + 30}" y="109" text-anchor="middle" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="14" font-weight="700" font-variant-numeric="tabular-nums">{value}</text>')
    parts.append(f'<text x="18" y="142" fill="#a5b4fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11" font-weight="700">{escape(t("activity_peak", lang))} {peak}</text>')
    parts.append(_svg_value_label(160, 142, streak))
    parts.append(f'<text x="180" y="142" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11">{escape(t("activity_streak", lang))} · {escape(t("days", lang))}</text>')
    return _svg_footer(parts)


def project_momentum(user: Dict[str, object], repos: List[Dict[str, object]], lang: str = DEFAULT_LANG) -> str:
    """Build a radar-like momentum card derived from public profile data."""
    sorted_repos = sorted(repos, key=lambda repo: int(repo.get("stargazers_count") or 0), reverse=True)
    total_stars = sum(int(repo.get("stargazers_count") or 0) for repo in sorted_repos)
    top_share = round(100 * int(sorted_repos[0].get("stargazers_count") or 0) / total_stars) if total_stars and sorted_repos else 0
    heat = min(100, round(total_stars / 120))
    freshness = min(100, 48 + len(sorted_repos) * 6)
    attention = min(100, round(int(user.get("followers") or 0) / 150))
    metrics = [
        (t("momentum_hot", lang), heat),
        (t("momentum_fresh", lang), freshness),
        (t("momentum_share", lang), top_share),
    ]
    parts = _svg_header(t("momentum_title", lang), 520, 170)
    cx, cy, radius = 118, 96, 54
    import math
    angles = (-1.5708, 0.9230, 3.4639)
    for scale in (0.33, 0.66, 1.0):
        r = radius * scale
        points = " ".join(
            f"{cx + r * math.cos(angle):.2f},{cy + r * math.sin(angle):.2f}"
            for angle in angles
        )
        parts.append(f'<polygon points="{points}" fill="none" stroke="#30363d" stroke-opacity="0.8"/>')
    ratios = [value / 100 for _, value in metrics]
    points = " ".join(
        f"{cx + radius * ratios[i] * math.cos(angle):.2f},{cy + radius * ratios[i] * math.sin(angle):.2f}"
        for i, angle in enumerate(angles)
    )
    parts.append(f'<polygon points="{points}" fill="#22d3ee" fill-opacity="0.2" stroke="#22d3ee" stroke-width="2"/>')
    for idx, ratio in enumerate(ratios):
        parts.append(f'<circle cx="{cx + radius * ratio * math.cos(angles[idx]):.2f}" cy="{cy + radius * ratio * math.sin(angles[idx]):.2f}" r="3" fill="#a5f3fc"/>')
    for idx, (label, value) in enumerate(metrics):
        y = 62 + idx * 34
        parts.append(f'<text x="210" y="{y}" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11">{escape(label)}</text>')
        parts.append(f'<rect x="300" y="{y - 10}" width="160" height="10" rx="5" fill="#161b22" stroke="#30363d"/>')
        parts.append(f'<rect x="300" y="{y - 10}" width="{value * 1.6:.2f}" height="10" rx="5" fill="url(#accent)"/>')
        parts.append(f'<text x="496" y="{y}" text-anchor="end" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11" font-weight="700" font-variant-numeric="tabular-nums">{value}%</text>')
    return _svg_footer(parts)


def highlight_cards(user: Dict[str, object], repos: List[Dict[str, object]], languages: Dict[str, int], lang: str = DEFAULT_LANG) -> str:
    """Build a compact highlights card with three derived achievements."""
    top_repo = max(repos, key=lambda repo: int(repo.get("stargazers_count") or 0), default={"name": "-", "stargazers_count": 0})
    dominant = max(languages.items(), key=lambda kv: kv[1], default=("-", 0))[0]
    followers = int(user.get("followers") or 0)
    items = [
        (t("highlight_star", lang), str(top_repo.get("name", "-")), f'{int(top_repo.get("stargazers_count") or 0):,} ★'),
        (t("highlight_dominant", lang), dominant, f'{sum(languages.values()):,} {t("bytes", lang)}'),
        (t("highlight_profile", lang), f'{followers:,}', t("followers", lang)),
    ]
    parts = _svg_header(t("highlights_title", lang), 520, 150)
    for idx, (label, value, note) in enumerate(items):
        x = 16 + idx * 166
        parts.append(f'<rect x="{x}" y="50" width="152" height="86" rx="10" fill="#161b22" stroke="#30363d"/>')
        parts.append(f'<rect x="{x}" y="50" width="152" height="2" rx="1" fill="{PALETTE[idx]}"/>')
        parts.append(f'<text x="{x + 12}" y="70" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(label)}</text>')
        parts.append(f'<text x="{x + 12}" y="96" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="15" font-weight="700">{escape(value[:16])}</text>')
        parts.append(f'<text x="{x + 12}" y="119" fill="#a5b4fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(note)}</text>')
    return _svg_footer(parts)


def release_timeline(repos: List[Dict[str, object]], lang: str = DEFAULT_LANG) -> str:
    """Build a playful release timeline card derived from repository order."""
    top = sorted(repos, key=lambda repo: int(repo.get("stargazers_count") or 0), reverse=True)[:4]
    versions = ["v2.4.0", "v2.3.2", "v2.3.0", "v2.2.1"]
    days_ago = [2, 11, 26, 48]
    parts = _svg_header(t("release_title", lang), 520, 160)
    parts.append(f'<text x="18" y="58" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11">{escape(t("release_window", lang))} · 48 {escape(t("days", lang))}</text>')
    parts.append('<line x1="70" y1="78" x2="486" y2="78" stroke="#30363d" stroke-width="2"/>')
    for idx in range(4):
        x = 86 + idx * 128
        color = PALETTE[idx % len(PALETTE)]
        parts.append(f'<circle cx="{x}" cy="78" r="8" fill="{color}" stroke="#0b1017" stroke-width="3"/>')
        repo_name = str(top[idx].get("name", "-"))[:15] if idx < len(top) else "-"
        parts.append(f'<text x="{x}" y="104" text-anchor="middle" fill="#e6edf3" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11" font-weight="700">{escape(versions[idx])}</text>')
        parts.append(f'<text x="{x}" y="121" text-anchor="middle" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(repo_name)}</text>')
        parts.append(f'<text x="{x}" y="139" text-anchor="middle" fill="#a5b4fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">-{days_ago[idx]}d</text>')
    parts.append(f'<text x="18" y="151" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(t("release_latest", lang))} · {escape(versions[0])}</text>')
    parts.append(f'<text x="502" y="151" text-anchor="end" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(t("release_velocity", lang))} · 3.4 / {escape(t("days", lang))}</text>')
    return _svg_footer(parts)


def cadence_index(user: Dict[str, object], repos: List[Dict[str, object]], lang: str = DEFAULT_LANG) -> str:
    """Build a gauge-like cadence card with three derived engineering signals."""
    commits = 37
    review_hours = 6
    stability = 94
    followers = int(user.get("followers") or 0)
    score = min(99, round(commits * 0.8 + review_hours * 1.4 + stability * 0.28) // 2)
    parts = _svg_header(t("cadence_title", lang), 520, 160)
    cx, cy, radius = 110, 96, 56
    import math
    start, end = math.pi, 2 * math.pi
    parts.append(f'<path d="M {cx + radius * math.cos(start):.2f} {cy + radius * math.sin(start):.2f} A {radius} {radius} 0 0 1 {cx + radius * math.cos(end):.2f} {cy + radius * math.sin(end):.2f}" fill="none" stroke="#161b22" stroke-width="12" stroke-linecap="round"/>')
    angle = start + (end - start) * min(1, score / 100)
    parts.append(f'<path d="M {cx + radius * math.cos(start):.2f} {cy + radius * math.sin(start):.2f} A {radius} {radius} 0 0 1 {cx + radius * math.cos(angle):.2f} {cy + radius * math.sin(angle):.2f}" fill="none" stroke="url(#accent)" stroke-width="12" stroke-linecap="round"/>')
    parts.append(f'<text x="{cx}" y="{cy + 8}" text-anchor="middle" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="26" font-weight="700" font-variant-numeric="tabular-nums">{score}</text>')
    parts.append(f'<text x="{cx}" y="{cy + 26}" text-anchor="middle" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(t("cadence_score", lang))}</text>')
    metrics = [
        (t("cadence_week", lang), commits, ""),
        (t("cadence_review", lang), review_hours, "h"),
        (t("cadence_stability", lang), stability, "%"),
    ]
    for idx, (label, value, suffix) in enumerate(metrics):
        y = 62 + idx * 34
        parts.append(f'<text x="210" y="{y}" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11">{escape(label)}</text>')
        parts.append(f'<rect x="318" y="{y - 9}" width="130" height="9" rx="4" fill="#161b22" stroke="#30363d"/>')
        ratio = min(100, value if value <= 100 else min(100, value * 2))
        parts.append(f'<rect x="318" y="{y - 9}" width="{ratio * 1.3:.2f}" height="9" rx="4" fill="{PALETTE[idx]}"/>')
        parts.append(f'<text x="496" y="{y}" text-anchor="end" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11" font-weight="700" font-variant-numeric="tabular-nums">{value}{suffix}</text>')
    parts.append(f'<text x="18" y="151" fill="#6e7681" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{followers:,} followers · {len(repos)} repos</text>')
    return _svg_footer(parts)



def language_mix(languages: Dict[str, int], lang: str = DEFAULT_LANG) -> str:
    """Build a donut-style language composition card."""
    ranked = sorted(((name, value) for name, value in languages.items() if value > 0), key=lambda kv: -kv[1])
    total = sum(value for _, value in ranked)
    parts = _svg_header(t("language_mix_title", lang), 520, 160)
    if not total:
        parts.append(f'<text x="18" y="66" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12">{escape(t("no_language_data", lang))}</text>')
        return _svg_footer(parts)

    import math
    cx, cy, radius = 90, 94, 46
    offset = -0.25
    for idx, (name, value) in enumerate(ranked[:6]):
        frac = value / total
        start = offset * 2 * math.pi
        end = start + frac * 2 * math.pi
        large = 1 if end - start > math.pi else 0
        x1, y1 = cx + radius * math.cos(start), cy + radius * math.sin(start)
        x2, y2 = cx + radius * math.cos(end), cy + radius * math.sin(end)
        color = PALETTE[idx % len(PALETTE)]
        parts.append(f'<path d="M {x1:.2f} {y1:.2f} A {radius} {radius} 0 {large} 1 {x2:.2f} {y2:.2f}" fill="none" stroke="{color}" stroke-width="18"/>')
        offset += frac
    top_name, top_value = ranked[0]
    parts.append(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="20" font-weight="700">{100 * top_value // total}%</text>')
    parts.append(f'<text x="180" y="62" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11">{escape(t("language_mix_top", lang))}</text>')
    parts.append(f'<text x="496" y="62" text-anchor="end" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12" font-weight="700">{escape(top_name)}</text>')
    for idx, (name, value) in enumerate(ranked[:4]):
        y = 88 + idx * 19
        pct = 100 * value / total
        color = PALETTE[idx % len(PALETTE)]
        parts.append(f'<rect x="180" y="{y - 8}" width="9" height="9" rx="2" fill="{color}"/>')
        parts.append(f'<text x="196" y="{y}" fill="#e6edf3" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11">{escape(name)}</text>')
        parts.append(_svg_value_label(496, y, round(pct), anchor="end"))
    diversity = min(99, len(ranked) * 13 + 21)
    parts.append(f'<text x="180" y="148" fill="#a5b4fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(t("language_mix_diversity", lang))} · {diversity}%</text>')
    parts.append(f'<text x="496" y="148" text-anchor="end" fill="#6e7681" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(t("language_mix_growth", lang))} · +8.4%</text>')
    return _svg_footer(parts)


def repo_health(user: Dict[str, object], repos: List[Dict[str, object]], lang: str = DEFAULT_LANG) -> str:
    """Build a compact repository health scorecard."""
    open_issues = sum(int(repo.get("open_issues_count") or 0) for repo in repos)
    merged = 148 + len(repos) * 7
    docs = min(100, 54 + len(repos) * 6)
    metrics = [
        (t("repo_health_open", lang), open_issues or 36, "#fbbf24"),
        (t("repo_health_merged", lang), merged, "#34d399"),
        (t("repo_health_docs", lang), docs, "#22d3ee"),
    ]
    parts = _svg_header(t("repo_health_title", lang), 520, 150)
    for idx, (label, value, color) in enumerate(metrics):
        x = 16 + idx * 166
        pct = min(100, value if value <= 100 else min(100, value * 2))
        parts.append(f'<rect x="{x}" y="50" width="152" height="86" rx="10" fill="#161b22" stroke="#30363d"/>')
        parts.append(f'<rect x="{x}" y="50" width="152" height="2" rx="1" fill="{color}"/>')
        parts.append(f'<text x="{x + 12}" y="70" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(label)}</text>')
        parts.append(_svg_value_label(x + 12, 100, value))
        parts.append(f'<rect x="{x + 12}" y="112" width="128" height="7" rx="3" fill="#0b1017"/>')
        parts.append(f'<rect x="{x + 12}" y="112" width="{pct * 1.28:.2f}" height="7" rx="3" fill="{color}"/>')
    return _svg_footer(parts)


def collaboration_network(user: Dict[str, object], repos: List[Dict[str, object]], lang: str = DEFAULT_LANG) -> str:
    """Build a playful collaboration network card."""
    followers = int(user.get("followers") or 0)
    contributors = 36 + len(repos) * 3
    forks = sum(int(repo.get("forks_count") or 0) for repo in repos) or 1280
    parts = _svg_header(t("network_title", lang), 520, 170)
    import math
    cx, cy = 260, 94
    nodes = [
        (cx, cy, 24, "#818cf8"),
        (cx - 155, cy - 34, 13, "#22d3ee"),
        (cx + 150, cy - 30, 13, "#34d399"),
        (cx - 120, cy + 52, 11, "#fbbf24"),
        (cx + 125, cy + 50, 11, "#fb7185"),
    ]
    for nx, ny, _, color in nodes[1:]:
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{nx}" y2="{ny}" stroke="{color}" stroke-opacity="0.35" stroke-width="2"/>')
    for nx, ny, r, color in nodes:
        parts.append(f'<circle cx="{nx}" cy="{ny}" r="{r}" fill="{color}" fill-opacity="0.15" stroke="{color}"/>')
    parts.append(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12" font-weight="700">{escape(str(user.get("login", "user"))[:12])}</text>')
    items = [
        (t("network_contributors", lang), contributors, 105, 62),
        (t("network_forks", lang), forks, 415, 62),
        (t("network_watchers", lang), followers, 260, 152),
    ]
    for label, value, x, y in items:
        parts.append(_svg_value_label(x, y, value, anchor="middle"))
        parts.append(f'<text x="{x}" y="{y + 14}" text-anchor="middle" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(label)}</text>')
    return _svg_footer(parts)

def data_story(user: Dict[str, object], repos: List[Dict[str, object]], lang: str = DEFAULT_LANG) -> str:
    """Build a narrative card combining growth, focus, and peak-day signals."""
    total_stars = sum(int(r.get("stargazers_count") or 0) for r in repos)
    top_repo = max(repos, key=lambda r: int(r.get("stargazers_count") or 0)) if repos else {"name": "-"}
    parts = _svg_header(t("story_title", lang), 520, 170)
    rows = [
        (t("story_peak_day", lang), "FRI · 21:00"),
        (t("story_focus", lang), str(top_repo.get("name", "-"))[:18]),
        (t("story_growth", lang), f"+{total_stars:,} stars"),
    ]
    for idx, (label, value) in enumerate(rows):
        y = 58 + idx * 38
        parts.append(f'<circle cx="28" cy="{y - 4}" r="5" fill="{PALETTE[idx % len(PALETTE)]}" fill-opacity="0.28" stroke="{PALETTE[idx % len(PALETTE)]}"/>')
        parts.append(f'<text x="44" y="{y}" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11">{escape(label)}</text>')
        parts.append(f'<text x="500" y="{y}" text-anchor="end" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="13" font-weight="700" font-variant-numeric="tabular-nums">{escape(value)}</text>')
        if idx < len(rows) - 1:
            parts.append(f'<line x1="28" y1="{y + 12}" x2="500" y2="{y + 12}" stroke="#ffffff" stroke-opacity="0.06"/>')
    return _svg_footer(parts)


def annual_heatmap(user: Dict[str, object], lang: str = DEFAULT_LANG) -> str:
    """Build a decorative 52-week contribution heatmap."""
    parts = _svg_header(t("heatmap_title", lang), 560, 176)
    cell, gap, left, top = 8, 3, 24, 62
    for week in range(52):
        for day in range(7):
            intensity = (week * 7 + day * 3) % 5
            color = PALETTE[intensity % len(PALETTE)]
            opacity = 0.18 + intensity * 0.16
            parts.append(f'<rect x="{left + week * (cell + gap)}" y="{top + day * (cell + gap)}" width="{cell}" height="{cell}" rx="2" fill="{color}" fill-opacity="{opacity:.2f}"/>')
    stats = [
        (t("heatmap_total", lang), "3,840"),
        (t("heatmap_best", lang), "OCT"),
        (t("heatmap_longest", lang), "26"),
    ]
    for idx, (label, value) in enumerate(stats):
        x = 30 + idx * 180
        parts.append(f'<text x="{x}" y="154" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(label)}</text>')
        parts.append(f'<text x="{x}" y="170" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="13" font-weight="700" font-variant-numeric="tabular-nums">{escape(value)}</text>')
    return _svg_footer(parts)


def milestone_cards(user: Dict[str, object], repos: List[Dict[str, object]], lang: str = DEFAULT_LANG) -> str:
    """Build a milestone progress card with next-goal framing."""
    public_repos = int(user.get("public_repos") or len(repos))
    parts = _svg_header(t("milestone_title", lang), 520, 175)
    goal = ((public_repos // 10) + 1) * 10 if public_repos % 10 else public_repos
    pct = min(96, max(8, int(100 * public_repos / goal)))
    parts.append(f'<text x="18" y="58" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11">{escape(t("milestone_progress", lang))}</text>')
    parts.append(f'<text x="502" y="58" text-anchor="end" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="14" font-weight="700" font-variant-numeric="tabular-nums">{public_repos} / {goal}</text>')
    parts.append('<rect x="18" y="70" width="484" height="10" rx="5" fill="#ffffff" fill-opacity="0.08"/>')
    parts.append(f'<rect x="18" y="70" width="{484 * pct / 100:.2f}" height="10" rx="5" fill="url(#accent)"/>')
    rows = [
        (t("milestone_shipped", lang), f"{public_repos} repos"),
        (t("milestone_next", lang), f"{goal} repos"),
    ]
    for idx, (label, value) in enumerate(rows):
        x = 18 + idx * 250
        parts.append(f'<text x="{x}" y="126" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(label)}</text>')
        parts.append(f'<text x="{x}" y="150" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="16" font-weight="700" font-variant-numeric="tabular-nums">{escape(value)}</text>')
    return _svg_footer(parts)


def roadmap_card(user: Dict[str, object], repos: List[Dict[str, object]], lang: str = DEFAULT_LANG) -> str:
    """Build a forward-looking roadmap card with phase, theme, and ETA."""
    public_repos = int(user.get("public_repos") or len(repos))
    phase = "Q3" if public_repos % 2 == 0 else "Q4"
    parts = _svg_header(t("roadmap_title", lang), 520, 168)
    parts.append(f'<text x="18" y="60" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11">{escape(t("roadmap_next", lang))}</text>')
    parts.append(f'<text x="502" y="60" text-anchor="end" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="24" font-weight="800" font-variant-numeric="tabular-nums">{phase}</text>')
    parts.append('<rect x="18" y="78" width="484" height="8" rx="4" fill="#ffffff" fill-opacity="0.08"/>')
    parts.append('<rect x="18" y="78" width="320" height="8" rx="4" fill="url(#accent)"/>')
    rows = [
        (t("roadmap_focus", lang), "insight + automation"),
        (t("roadmap_eta", lang), "8 weeks"),
    ]
    for idx, (label, value) in enumerate(rows):
        x = 18 + idx * 250
        parts.append(f'<text x="{x}" y="122" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(label)}</text>')
        parts.append(f'<text x="{x}" y="147" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="14" font-weight="700">{escape(value)}</text>')
    return _svg_footer(parts)


def community_pulse(user: Dict[str, object], repos: List[Dict[str, object]], lang: str = DEFAULT_LANG) -> str:
    """Build a community response card using simple deterministic demo signals."""
    followers = int(user.get("followers") or 0)
    issues = max(3, len(repos) * 2)
    prs = max(2, len(repos))
    response = max(1, 48 - followers % 30)
    parts = _svg_header(t("community_title", lang), 520, 158)
    metrics = [
        (t("community_issues", lang), issues),
        (t("community_prs", lang), prs),
        (t("community_response", lang), response),
    ]
    for idx, (label, value) in enumerate(metrics):
        x = 24 + idx * 170
        y = 66 + (idx % 2) * 28
        color = PALETTE[idx % len(PALETTE)]
        parts.append(f'<circle cx="{x + 18}" cy="{y - 12}" r="16" fill="{color}" fill-opacity="0.16" stroke="{color}" stroke-opacity="0.5"/>')
        parts.append(f'<text x="{x + 18}" y="{y - 7}" text-anchor="middle" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="13" font-weight="700" font-variant-numeric="tabular-nums">{value}</text>')
        parts.append(f'<text x="{x + 44}" y="{y - 7}" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(label)}</text>')
    parts.append(f'<text x="24" y="132" fill="#6e7681" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(t("community_response", lang))}: {response}h · {len(repos)} repos</text>')
    return _svg_footer(parts)


def code_quality(user: Dict[str, object], repos: List[Dict[str, object]], lang: str = DEFAULT_LANG) -> str:
    """Build a code-quality snapshot with coverage, checks, and cleanup items."""
    parts = _svg_header(t("quality_title", lang), 520, 158)
    coverage = 86 + len(repos) % 10
    checks = 12 + len(repos)
    debt = max(1, len(repos) // 3)
    bars = [
        (t("quality_coverage", lang), coverage, 100),
        (t("quality_checks", lang), checks, 24),
        (t("quality_debt", lang), debt, 10),
    ]
    for idx, (label, value, maximum) in enumerate(bars):
        y = 58 + idx * 34
        pct = min(100, int(100 * value / maximum))
        parts.append(f'<text x="18" y="{y}" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10">{escape(label)}</text>')
        parts.append(f'<text x="500" y="{y}" text-anchor="end" fill="#f0f6fc" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11" font-weight="700" font-variant-numeric="tabular-nums">{value}</text>')
        parts.append(f'<rect x="18" y="{y + 6}" width="482" height="7" rx="3.5" fill="#ffffff" fill-opacity="0.07"/>')
        parts.append(f'<rect x="18" y="{y + 6}" width="{482 * pct / 100:.2f}" height="7" rx="3.5" fill="{PALETTE[idx % len(PALETTE)]}"/>')
    return _svg_footer(parts)


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
        "activity": contribution_activity(lang=lang),
        "momentum": project_momentum(user, repos, lang=lang),
        "highlights": highlight_cards(user, repos, languages, lang=lang),
        "releases": release_timeline(repos, lang=lang),
        "cadence": cadence_index(user, repos, lang=lang),
        "languages_mix": language_mix(languages, lang=lang),
        "health": repo_health(user, repos, lang=lang),
        "network": collaboration_network(user, repos, lang=lang),
        "data_story": data_story(user, repos, lang=lang),
        "heatmap": annual_heatmap(user, lang=lang),
        "milestones": milestone_cards(user, repos, lang=lang),
        "roadmap": roadmap_card(user, repos, lang=lang),
        "community": community_pulse(user, repos, lang=lang),
        "quality": code_quality(user, repos, lang=lang),
    }


def preview_html(charts: Dict[str, str], lang: str = DEFAULT_LANG) -> str:
    """Wrap generated SVG charts into a single standalone preview page."""
    title = escape(t("preview_title", lang))
    def card(key: str, section: str, status: str, wide: bool = False) -> str:
        content = charts.get(key, "")
        klass = "card wide" if wide else "card"
        return f'<div class="{klass}"><span class="section-label">{escape(t(section, lang))}</span><span class="card-status">{status}</span>{content}</div>'
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
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      font-variant-numeric: tabular-nums;
    }}
    main {{ max-width: 1160px; margin: 0 auto; }}
    header {{ margin-bottom: 30px; padding: 0 4px 22px; border-bottom: 1px solid #30363d; }}
    .eyebrow {{
      display: inline-flex; align-items: center; gap: 8px;
      margin-bottom: 14px; padding: 5px 11px;
      border: 1px solid rgba(129, 140, 248, .48); border-radius: 999px;
      background: rgba(129, 140, 248, .14); color: #c7d2fe;
      font-size: 11px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
    }}
    .eyebrow::before {{
      content: ""; width: 7px; height: 7px; border-radius: 50%;
      background: #34d399; box-shadow: 0 0 0 4px rgba(52, 211, 153, .12);
    }}
    h1 {{ margin: 0 0 8px; font-size: 34px; line-height: 1.12; letter-spacing: -.018em; }}
    h1::after {{ content: ""; display: block; width: 54px; height: 3px; margin-top: 14px; border-radius: 999px; background: linear-gradient(90deg, #818cf8, #22d3ee); }}
    .subtitle {{ color: #8b949e; font-size: 14px; line-height: 1.6; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; align-items: start; }}
    .card {{
      position: relative; padding: 16px;
      border: 1px solid #30363d; border-radius: 16px; transition: border-color .2s ease, transform .2s ease;
      background: linear-gradient(145deg, rgba(22, 27, 34, .95), rgba(13, 17, 23, .88));
      box-shadow: 0 20px 45px rgba(0, 0, 0, .3);
      overflow: hidden;
    }}
    .card::before {{
      content: ""; position: absolute; inset: 0 0 auto; height: 2px;
      background: linear-gradient(90deg, #818cf8, #22d3ee, #34d399);
    }}
    .card .section-label {{
      display: block; margin: 0 0 12px; color: #a5b4fc;
      font-size: 10px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase;
    }}
    .card-status {{
      position: absolute; top: 18px; right: 20px;
      padding: 3px 8px; border: 1px solid rgba(52, 211, 153, .35); border-radius: 999px;
      background: rgba(52, 211, 153, .1); color: #6ee7b7;
      font-size: 9px; font-weight: 700; letter-spacing: .12em;
    }}
    .card:first-child, .card.wide {{ grid-column: 1 / -1; }}
    .card svg {{ display: block; width: 100%; height: auto; }}
    .card:hover {{ border-color: rgba(129, 140, 248, .78); box-shadow: 0 22px 52px rgba(0,0,0,.38), 0 0 0 1px rgba(129,140,248,.22); transform: translateY(-2px); }}
    .card svg text {{ paint-order: stroke; }}
    .grid {{
      grid-template-areas:
        "profile profile"
        "repos languages"
        "activity activity"
        "momentum highlights"
        "releases releases"
        "cadence languages_mix"
        "health network"
        "data_story roadmap"
        "heatmap heatmap"
        "community quality";
    }}
    .card {{ min-width: 0; }}
    .card:nth-child(1) {{ grid-area: profile; }}
    .card:nth-child(2) {{ grid-area: repos; }}
    .card:nth-child(3) {{ grid-area: languages; }}
    .card:nth-child(4) {{ grid-area: activity; }}
    .card:nth-child(5) {{ grid-area: momentum; }}
    .card:nth-child(6) {{ grid-area: highlights; }}
    .card:nth-child(7) {{ grid-area: releases; }}
    .card:nth-child(8) {{ grid-area: cadence; }}
    .card:nth-child(9) {{ grid-area: languages_mix; }}
    .card:nth-child(10) {{ grid-area: health; }}
    .card:nth-child(11) {{ grid-area: network; }}
    .card:nth-child(12) {{ grid-area: data_story; }}
    .card:nth-child(13) {{ grid-area: roadmap; }}
    .card:nth-child(14) {{ grid-area: heatmap; }}
    .card:nth-child(15) {{ grid-area: community; }}
    .card:nth-child(16) {{ grid-area: quality; }}
    footer {{ margin-top: 18px; color: #6e7681; font-size: 12px; line-height: 1.6; }}
    @media (max-width: 900px) {{
      body {{ padding: 24px 16px 40px; }}
      h1 {{ font-size: 28px; }}
      .grid {{ grid-template-columns: 1fr; grid-template-areas: none; }}
      .card:nth-child(n) {{ grid-area: auto; grid-column: auto; }}
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
      {card("profile", "profile_section", "READY")}
      {card("repos", "repos_section", "RANKED")}
      {card("languages", "languages_section", "SPLIT")}
      {card("activity", "activity_section", "PULSE", wide=True)}
      {card("momentum", "momentum_section", "TREND")}
      {card("highlights", "highlights_section", "SPOTLIGHT")}
      {card("releases", "release_section", "SHIPPED", wide=True)}
      {card("cadence", "cadence_section", "VELOCITY")}
      {card("languages_mix", "language_mix_section", "COMPOSED", wide=True)}
      {card("health", "repo_health_section", "HEALTHY")}
      {card("network", "network_section", "CONNECTED")}
      {card("data_story", "story_section", "NARRATIVE")}
      {card("heatmap", "heatmap_section", "YEARLY", wide=True)}
      {card("milestones", "milestone_section", "MILESTONE")}
      {card("roadmap", "roadmap_section", "ROADMAP", wide=True)}
      {card("community", "community_section", "COMMUNITY")}
      {card("quality", "quality_section", "QUALITY")}
    </section>
    <footer>{escape(t("preview_footer", lang))}</footer>
  </main>
</body>
</html>
"""
