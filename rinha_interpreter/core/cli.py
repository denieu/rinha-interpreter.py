from enum import Enum
from functools import lru_cache
from os import getenv

from rich.console import Console
from typer import Exit


class ExitCodesEnum(Enum):
    SUCCESS = 0
    GENERIC_ERROR = 1
    JSON_FILE_NOT_FOUND = 2
    INVALID_JSON_FILE = 3
    INVALID_PARSED_AST = 4


@lru_cache(maxsize=1)
def get_console() -> Console:
    rich_color_system: str = getenv("RICH_COLOR_SYSTEM", "auto")
    if rich_color_system not in ("auto", "standard", "256", "truecolor", "windows"):
        rich_color_system = "auto"

    rich_console_width: int | None = int(envvar) if (envvar := getenv("RICH_CONSOLE_WIDTH", None)) else None

    return Console(color_system=rich_color_system, width=rich_console_width)  # type: ignore


def typer_exit(code: ExitCodesEnum) -> Exit:
    if code != ExitCodesEnum.SUCCESS:
        color = "red"
        get_console().print(f"\n[{color} bold]Exit status {code.value} {code.name}[/]")

    return Exit(code.value)
