from createchart.charts import aggregate_languages, language_chart, profile_summary, repo_bars


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
