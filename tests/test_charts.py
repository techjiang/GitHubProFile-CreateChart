from createchart.charts import aggregate_languages, language_chart, preview_html, profile_summary, repo_bars, demo_charts, t


def test_language_chart_empty():
    svg = language_chart({})
    assert "<svg" in svg
    assert "No language data" in svg


def test_language_chart_has_legend():
    svg = language_chart({"Python": 800, "Rust": 200})
    assert "Python" in svg
    assert "Rust" in svg


def test_repo_bars_orders_by_metric():
    svg = repo_bars([
        {"name": "small", "stargazers_count": 2},
        {"name": "big", "stargazers_count": 10},
    ])
    assert svg.index("big") < svg.index("small")


def test_profile_summary_counts_stars():
    svg = profile_summary({"login": "octocat", "followers": 3}, [
        {"stargazers_count": 4}, {"stargazers_count": 6},
    ])
    assert ">10</text>" in svg


def test_aggregate_languages():
    result = aggregate_languages(
        [{"name": "a"}, {"name": "b"}],
        {"a": {"Python": 10}, "b": {"Python": 5, "Go": 2}},
    )
    assert result["Python"] == 15
    assert result["Go"] == 2


def test_demo_charts_returns_six_svg_files():
    from createchart.charts import demo_charts

    charts = demo_charts()
    assert set(charts) == {"profile", "repos", "languages", "activity", "momentum", "highlights", "releases", "cadence", "languages_mix", "health", "network", "data_story", "heatmap", "milestones", "roadmap", "community", "quality"}
    assert all(svg.startswith("<svg") and svg.endswith("</svg>") for svg in charts.values())


def test_preview_html_wraps_all_charts():
    html = preview_html({"profile": "<svg>p</svg>", "repos": "<svg>r</svg>", "languages": "<svg>l</svg>"})
    assert "<html" in html
    assert "<svg>p</svg>" in html
    assert "<svg>r</svg>" in html
    assert "<svg>l</svg>" in html


def test_chinese_labels_are_used():
    assert t("followers", "zh") == "关注者"
    charts = demo_charts(lang="zh")
    assert "关注者" in charts["profile"]
    assert "热门仓库" in charts["repos"]
    assert "语言分布" in charts["languages"]


def test_english_labels_remain_default():
    charts = demo_charts()
    assert "Followers" in charts["profile"]
    assert "Top repositories" in charts["repos"]


def test_preview_polish_rounds_are_visible():
    html = preview_html(demo_charts(lang="zh"), lang="zh")
    assert "第 16 轮" in html
    assert "第 16 轮视觉打磨" in html
    assert "累计星标" in html
    assert "rgba(129, 140, 248, .78)" in html


def test_preview_header_and_labels_are_polished():
    html = preview_html(demo_charts(lang="zh"), lang="zh")
    assert "h1::after" in html
    assert "#8b949e" in html


def test_profile_values_use_thousands_separator():
    svg = demo_charts(lang="zh")["profile"]
    assert ">12,840</text>" in svg
    assert ">19,060</text>" in svg


def test_preview_status_badges_are_present():
    html = preview_html(demo_charts(lang="zh"), lang="zh")
    assert "card-status" in html
    assert "READY" in html
    assert "RANKED" in html
    assert "SPLIT" in html
    assert "PingFang SC" in html
    assert "tabular-nums" in html


def test_advanced_cards_are_rendered():
    charts = demo_charts(lang="zh")
    assert "活跃热力" in charts["activity"]
    assert "项目 momentum" in charts["momentum"]
    assert "高光时刻" in charts["highlights"]
    assert "peak" not in charts["activity"].lower()


def test_preview_includes_new_round_nine_cards():
    charts = demo_charts(lang="zh")
    html = preview_html(charts, lang="zh")
    assert "发布时间轴" in charts["releases"]
    assert "节奏指数" in charts["cadence"]
    assert "SHIPPED" in html
    assert "VELOCITY" in html
    assert "07 / 发布时间轴" in html
    assert "08 / 节奏指数" in html


def test_preview_includes_all_sections():
    html = preview_html(demo_charts(lang="zh"), lang="zh")
    for badge in ("PULSE", "TREND", "SPOTLIGHT"):
        assert badge in html
    assert "04 / 贡献活跃度" in html
    assert "05 / 项目 Momentum" in html
    assert "06 / 高光时刻" in html



def test_preview_includes_round_ten_cards():
    charts = demo_charts(lang="zh")
    html = preview_html(charts, lang="zh")
    assert "语言构成" in charts["languages_mix"]
    assert "仓库健康度" in charts["health"]
    assert "协作网络" in charts["network"]
    assert "COMPOSED" in html
    assert "HEALTHY" in html
    assert "CONNECTED" in html
    assert "09 / 语言构成" in html
    assert "10 / 仓库健康度" in html
    assert "11 / 协作网络" in html


def test_preview_includes_round_eleven_cards():
    charts = demo_charts(lang="zh")
    html = preview_html(charts, lang="zh")
    assert "数据叙事" in charts["data_story"]
    assert "年度热力" in charts["heatmap"]
    assert "成长里程碑" in charts["milestones"]
    assert "NARRATIVE" in html
    assert "YEARLY" in html
    assert "MILESTONE" in html
    assert "12 / 数据叙事" in html
    assert "13 / 年度热力" in html
    assert "14 / 成长里程碑" in html


def test_preview_includes_round_twelve_cards():
    charts = demo_charts(lang="zh")
    html = preview_html(charts, lang="zh")
    assert "路线图" in charts["roadmap"]
    assert "社区温度" in charts["community"]
    assert "代码质量" in charts["quality"]
    assert "ROADMAP" in html
    assert "COMMUNITY" in html
    assert "QUALITY" in html
    assert "15 / 路线图" in html
    assert "16 / 社区温度" in html
    assert "17 / 代码质量" in html
