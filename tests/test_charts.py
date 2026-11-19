from createchart.charts import aggregate_languages, language_chart, preview_html, profile_summary, repo_bars


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
