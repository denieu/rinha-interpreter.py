from rinha_interpreter.core.spec import AuxSpecTerm, SpecEvaluateReturn, SpecTerm


class Environment:
    def __init__(self) -> None:
        self._scopes: list[dict[str, SpecEvaluateReturn]] = [{}]
        self._terms: list[SpecTerm | AuxSpecTerm] = []
        self._results: list[SpecEvaluateReturn] = []

    def start_scope(self, scope: dict[str, SpecEvaluateReturn]) -> None:
        self._scopes.append(scope)

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

    def add_term_to_evaluate(self, term: SpecTerm | AuxSpecTerm) -> None:
        self._terms.append(term)

    def get_term_to_evaluate(self) -> SpecTerm | AuxSpecTerm:
        if self._terms:
            return self._terms.pop()
        return None

    def save_evaluate_result(self, result: SpecEvaluateReturn) -> None:
        self._results.append(result)

    def get_evaluate_result(self) -> SpecEvaluateReturn:
        return self._results.pop()
