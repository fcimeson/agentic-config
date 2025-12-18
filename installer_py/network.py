"""Network utilities for fetching remote files."""

import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional


def fetch_url(url: str, output_path: Path) -> bool:
    """
    Fetch a URL and save to a file.

    Returns:
        True if successful, False otherwise
    """
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()

        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(data)

        return True
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        return False


def fetch_text(url: str) -> Optional[str]:
    """
    Fetch a URL and return as text.

    Returns:
        The text content if successful, None otherwise
    """
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
        return data.decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        return None
