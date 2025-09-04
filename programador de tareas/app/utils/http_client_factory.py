import os
import httpx
from typing import Dict

def build_header(token: str) -> Dict[str, str]:
    """
    make authentication headers to github
    """
    return {
        "Accept": "application/vnd.github+json",
        "X-Github-Api-Version": "2022-11-28",
        "User-Agent": "git-gub-stats-app",
        "Autorization": f"Bearrer {token}",
    }

def get_async_github_client() -> httpx.AsyncClient:
    """
    return a configurated instance of httpx.AsyncClient
    """
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN not configured on the env")
    
    headers = build_header(github_token)
    return httpx.AsyncClient(headers=headers, timeout=15)