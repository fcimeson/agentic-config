from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import subprocess
from typing import Optional

DEFAULT_BRANCH = "main"
DEFAULT_INSTALL_DIR = ".opencode"
DEFAULT_REPO_SLUG = "fcimeson/agentic-config"


def _run_git_command(args: list[str], cwd: Path) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def detect_repo_slug(script_path: Optional[Path]) -> str:
    """Best-effort detection of the repo slug when running from a checkout."""
    explicit = os.environ.get("OPENCODE_REPO")
    if explicit:
        return explicit

    if script_path is None:
        return DEFAULT_REPO_SLUG

    if not script_path.exists():
        return DEFAULT_REPO_SLUG

    repo_dir = script_path.parent
    git_dir = _run_git_command(["rev-parse", "--show-toplevel"], repo_dir)
    if not git_dir:
        return DEFAULT_REPO_SLUG

    origin_url = _run_git_command(["config", "--get", "remote.origin.url"], Path(git_dir))
    if not origin_url:
        return DEFAULT_REPO_SLUG

    slug = _extract_slug(origin_url)
    return slug or DEFAULT_REPO_SLUG


def _extract_slug(origin_url: str) -> Optional[str]:
    origin_url = origin_url.strip()
    if origin_url.startswith("git@github.com:"):
        slug = origin_url.split(":", 1)[1]
    elif origin_url.startswith("ssh://git@github.com/"):
        slug = origin_url.split("github.com/", 1)[1]
    elif origin_url.startswith("https://github.com/"):
        slug = origin_url.split("github.com/", 1)[1]
    else:
        return None
    return slug.rstrip("/").removesuffix(".git")


@dataclass
class InstallerConfig:
    branch: str
    repo_slug: str
    install_dir: Path
    temp_dir: Path
    raw_url: str
    registry_url: str
    use_local_files: bool
    local_registry_path: Optional[Path]

    @property
    def repo_url(self) -> str:
        return f"https://github.com/{self.repo_slug}"


def build_config(
    *,
    branch: Optional[str] = None,
    install_dir: Optional[str] = None,
    repo_slug: Optional[str] = None,
    raw_url: Optional[str] = None,
    registry_url: Optional[str] = None,
    use_local_files: bool = False,
    local_registry_path: Optional[str] = None,
    script_path: Optional[Path] = None,
) -> InstallerConfig:
    resolved_branch = branch or os.environ.get("OPENCODE_BRANCH") or DEFAULT_BRANCH
    resolved_repo_slug = repo_slug or detect_repo_slug(script_path or Path.cwd())

    resolved_install_dir = Path(
        install_dir or os.environ.get("OPENCODE_INSTALL_DIR") or DEFAULT_INSTALL_DIR
    ).expanduser()

    resolved_raw_url = raw_url or os.environ.get("OPENCODE_RAW_URL")
    if not resolved_raw_url:
        resolved_raw_url = f"https://raw.githubusercontent.com/{resolved_repo_slug}/{resolved_branch}"

    resolved_registry_url = registry_url or os.environ.get("OPENCODE_REGISTRY_URL")
    if not resolved_registry_url:
        resolved_registry_url = (
            f"https://raw.githubusercontent.com/{DEFAULT_REPO_SLUG}/{resolved_branch}/registry.json"
        )

    temp_dir = Path(os.environ.get("TMPDIR", "/tmp")) / "opencode-installer"
    temp_dir.mkdir(parents=True, exist_ok=True)

    resolved_local_registry = Path(local_registry_path).expanduser() if local_registry_path else None

    return InstallerConfig(
        branch=resolved_branch,
        repo_slug=resolved_repo_slug,
        install_dir=resolved_install_dir,
        temp_dir=temp_dir,
        raw_url=resolved_raw_url,
        registry_url=resolved_registry_url,
        use_local_files=use_local_files,
        local_registry_path=resolved_local_registry,
    )
