import json

from pydantic import ValidationError

from rinha_interpreter.core.cli import ExitCodesEnum, typer_exit
from rinha_interpreter.core.spec import SpecFile


def parse_ast(json_path: str) -> SpecFile:
    try:
        with open(json_path, "r", encoding="utf-8") as file_handler:
            json_result = json.load(file_handler)
    except FileNotFoundError as error:
        raise typer_exit(ExitCodesEnum.JSON_FILE_NOT_FOUND) from error
    except json.JSONDecodeError as error:
        raise typer_exit(ExitCodesEnum.INVALID_JSON_FILE) from error
    except Exception as error:
        raise typer_exit(ExitCodesEnum.GENERIC_ERROR) from error

    try:
        ast = SpecFile(**json_result)
    except ValidationError as error:
        raise typer_exit(ExitCodesEnum.INVALID_PARSED_AST) from error
    except Exception as error:
        raise typer_exit(ExitCodesEnum.GENERIC_ERROR) from error

    return ast
