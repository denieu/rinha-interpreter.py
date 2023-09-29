from typing import Any

from rinha_interpreter.core.spec import AuxSpecTerm, SpecEvaluateReturn, SpecTerm


class Environment:
    def __init__(self) -> None:
        self._scopes: list[dict[str, SpecEvaluateReturn]] = []
        self._scope: dict[str, SpecEvaluateReturn] = {}
        self._terms: list[SpecTerm | AuxSpecTerm] = []
        self._results: list[Any] = []
        self._cache: dict[str, Any] = {}

    def start_scope(self, scope: dict[str, SpecEvaluateReturn]) -> None:
        self._scopes.append(self._scope.copy())
        self._scope.update(scope)

    def finish_scope(self) -> None:
        self._scope = self._scopes.pop()

    def set_variable(self, name: str, value: SpecEvaluateReturn) -> None:
        self._scope[name] = value

    def get_variable(self, name: str) -> SpecEvaluateReturn:
        return self._scope[name]

    def add_term_to_evaluate(self, term: SpecTerm | AuxSpecTerm) -> None:
        self._terms.append(term)

    def get_term_to_evaluate(self) -> SpecTerm | AuxSpecTerm | None:
        try:
            return self._terms.pop()
        except IndexError:
            return None

    def save_evaluate_result(self, result: Any) -> None:
        self._results.append(result)

    def get_evaluate_result(self) -> Any:
        return self._results.pop()

    def set_cache(self, key: str, value: Any) -> None:
        self._cache[key] = value

    def get_cache(self, key: str) -> Any:
        return self._cache.get(key)
