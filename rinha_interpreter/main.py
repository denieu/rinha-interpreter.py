from typing import Annotated, Optional

from typer import Argument, Exit, Option, Typer

from rinha_interpreter.__version__ import __version__
from rinha_interpreter.core.cli import ExitCodesEnum, get_console, typer_exit

app = Typer(
    name="rinha-interpreter",
    help="",
)


def version_callback(value: bool) -> None:
    if value:
        get_console().print(f"[white bold]Rinha Interpreter {__version__}[/]")
        raise Exit(ExitCodesEnum.SUCCESS.value)


@app.command()
def main(
    ast_path: Annotated[str, Argument(help="Path to rinha AST JSON")],
    _: Annotated[Optional[bool], Option("--version", help="Show CLI version", callback=version_callback, is_eager=True)] = None,
) -> None:
    raise typer_exit(ExitCodesEnum.SUCCESS)


if __name__ == "__main__":
    app()
