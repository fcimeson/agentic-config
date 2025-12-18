from __future__ import annotations

import argparse
from typing import NamedTuple, Optional

PROFILES = ["essential", "developer", "business", "full", "advanced"]


class ParsedArgs(NamedTuple):
    profile: Optional[str]
    install_dir: Optional[str]
    local_files: Optional[str]
    list: bool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="OpenAgents Installer (Python version)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("profile", nargs="?", choices=PROFILES, help="Installation profile")
    parser.add_argument("--install-dir", help="Custom installation directory")
    parser.add_argument(
        "--local-files",
        nargs="?",
        const="registry.json",
        help="Use local files instead of downloading (optional path)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available components",
    )
    return parser


def parse_args() -> tuple[ParsedArgs, argparse.ArgumentParser]:
    parser = build_parser()
    args = parser.parse_args()
    parsed = ParsedArgs(
        profile=args.profile,
        install_dir=args.install_dir,
        local_files=args.local_files,
        list=args.list,
    )
    return parsed, parser
