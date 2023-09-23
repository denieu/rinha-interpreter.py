from rinha_interpreter.core.spec import SpecEvaluateReturn


class Environment:
    def __init__(self) -> None:
        self._scopes: list[dict[str, SpecEvaluateReturn]] = [{}]

    def start_scope(self) -> None:
        self._scopes.append({})

    def finish_scope(self) -> None:
        if len(self._scopes) > 1:
            self._scopes.pop()

    def set_variable(self, name: str, value: SpecEvaluateReturn) -> None:
        self._scopes[-1][name] = value

    def get_variable(self, name: str) -> SpecEvaluateReturn:
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]

        raise Exception(f"Variavel {name} não definida")
