"""Minimal GitHub REST API client used by CreateChart."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

API_BASE = "https://api.github.com"


class GitHubClient:
    def __init__(self, token: Optional[str] = None, base_url: str = API_BASE) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "CreateChart/0.2",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self.session.headers.update(headers)

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=20)
        response.raise_for_status()
        return response.json()

    def get_user(self, username: str) -> Dict[str, Any]:
        return self._get(f"/users/{username}")

    def list_repos(self, username: str, per_page: int = 100) -> List[Dict[str, Any]]:
        repos: List[Dict[str, Any]] = []
        page = 1
        while True:
            batch = self._get(
                f"/users/{username}/repos",
                params={"per_page": per_page, "page": page, "type": "owner", "sort": "updated"},
            )
            repos.extend(batch)
            if len(batch) < per_page:
                break
            page += 1
        return repos

    def list_languages(self, username: str, repo_name: str) -> Dict[str, int]:
        return self._get(f"/repos/{username}/{repo_name}/languages")
