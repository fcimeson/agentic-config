from __future__ import annotations

from dataclasses import dataclass
import os
import sys
from typing import Optional


class Colors:
    RED = "[0;31m"
    GREEN = "[0;32m"
    YELLOW = "[1;33m"
    BLUE = "[0;34m"
    MAGENTA = "[0;35m"
    CYAN = "[0;36m"
    BOLD = "[1m"
    RESET = "[0m"


@dataclass
class Console:
    enable_color: bool = True

    def color(self, text: str, color: str) -> str:
        if not self.enable_color:
            return text
        return f"{color}{text}{Colors.RESET}"

    def print(self, message: str = "") -> None:
        print(message)

    def print_success(self, message: str) -> None:
        self.print(self.color(f"✓ {message}", Colors.GREEN))

    def print_error(self, message: str) -> None:
        self.print(self.color(f"✗ {message}", Colors.RED))

    def print_info(self, message: str) -> None:
        self.print(self.color(f"ℹ {message}", Colors.BLUE))

    def print_warning(self, message: str) -> None:
        self.print(self.color(f"⚠ {message}", Colors.YELLOW))

    def print_step(self, message: str) -> None:
        bar = self.color("▶", Colors.MAGENTA)
        self.print(f"\n{bar} {message}\n")

    def print_header(self) -> None:
        title = self.color("OpenAgents Installer v2 (Python)", Colors.CYAN)
        bar = self.color("=" * len("OpenAgents Installer v2 (Python)"), Colors.CYAN)
        self.print(bar)
        self.print(title)
        self.print(bar)


_default_console: Optional[Console] = None


def get_console() -> Console:
    global _default_console
    if _default_console is None:
        enable_color = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
        _default_console = Console(enable_color=enable_color)
    return _default_console


def is_interactive() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


# Export module-level functions for convenience
def print_header() -> None:
    get_console().print_header()


def print_step(message: str) -> None:
    get_console().print_step(message)


def print_success(message: str) -> None:
    get_console().print_success(message)


def print_error(message: str) -> None:
    get_console().print_error(message)


def print_info(message: str) -> None:
    get_console().print_info(message)


def print_warning(message: str) -> None:
    get_console().print_warning(message)


def colorize(text: str, color: str) -> str:
    return get_console().color(text, color)


def clear_screen() -> None:
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")
