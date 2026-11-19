"""Command-line interface for CreateChart."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Dict

from .charts import aggregate_languages, demo_charts, language_chart, profile_summary, repo_bars
from .github_client import GitHubClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="createchart", description="Generate GitHub statistic SVG charts")
    parser.add_argument("username", nargs="?", help="GitHub username (omit with --demo)")
    parser.add_argument("--demo", action="store_true", help="Generate local demo charts without GitHub API")
    parser.add_argument("-o", "--output-dir", default="charts", help="Directory to write SVG files")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"), help="GitHub token (or set GITHUB_TOKEN)")
    parser.add_argument("--metric", default="stargazers_count", help="Repo ranking metric (e.g. stargazers_count, forks_count)")
    parser.add_argument("--repo-languages", action="store_true", help="Aggregate languages across up to 20 repos")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.demo:
        output = Path(args.output_dir)
        output.mkdir(parents=True, exist_ok=True)
        for name, svg in demo_charts().items():
            (output / f"{name}.svg").write_text(svg, encoding="utf-8")
        print(f"Wrote 3 demo charts to {output.resolve()}")
        return 0

    if not args.username:
        print("username is required unless --demo is used", file=sys.stderr)
        return 2

    client = GitHubClient(token=args.token)
    try:
        user = client.get_user(args.username)
        repos = client.list_repos(args.username)
    except Exception as exc:  # network/API errors are surfaced to CLI caller
        print(f"Failed to fetch GitHub data: {exc}", file=sys.stderr)
        return 1

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    (output / "profile.svg").write_text(profile_summary(user, repos), encoding="utf-8")
    (output / "repos.svg").write_text(repo_bars(repos, metric=args.metric), encoding="utf-8")

    languages: Dict[str, int] = {}
    if args.repo_languages:
        by_repo: Dict[str, Dict[str, int]] = {}
        for repo in repos[:20]:
            name = str(repo.get("name", ""))
            by_repo[name] = client.list_languages(args.username, name)
        languages = aggregate_languages(repos, by_repo)
    else:
        # user has no aggregate language endpoint; use top repo as a lightweight default
        if repos:
            languages = client.list_languages(args.username, str(repos[0].get("name", "")))
    (output / "languages.svg").write_text(language_chart(languages), encoding="utf-8")

    print(f"Wrote 3 charts to {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
