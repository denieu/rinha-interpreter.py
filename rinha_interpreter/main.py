from typing import Annotated, Optional

from typer import Argument, Exit, Option, Typer

from rinha_interpreter.__version__ import __version__
from rinha_interpreter.core.cli import ExitCodesEnum, get_console, typer_exit
from rinha_interpreter.core.environment import Environment
from rinha_interpreter.core.evaluate import evaluate
from rinha_interpreter.core.parser import parse_ast

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
    json_path: Annotated[str, Argument(help="Path to rinha AST JSON")],
    _: Annotated[Optional[bool], Option("--version", help="Show CLI version", callback=version_callback, is_eager=True)] = None,
) -> None:
    ast = parse_ast(json_path)

    environment = Environment()
    evaluate(ast.expression, environment)

    raise typer_exit(ExitCodesEnum.SUCCESS)


if __name__ == "__main__":
    app()
