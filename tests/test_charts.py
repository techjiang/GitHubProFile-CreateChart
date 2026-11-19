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


def test_demo_charts_returns_three_svg_files():
    from createchart.charts import demo_charts

    charts = demo_charts()
    assert set(charts) == {"profile", "repos", "languages"}
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
    assert "第 7 轮" in html
    assert "第 7 轮视觉打磨" in html
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
