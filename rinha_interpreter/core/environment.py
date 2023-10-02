from typing import Any

from rinha_interpreter.core.spec import AuxSpecTerm, SpecEvaluateReturn, SpecTerm


class Environment:
    def __init__(self) -> None:
        self._scopes: list[dict[str, SpecEvaluateReturn]] = []
        self._scope: dict[str, SpecEvaluateReturn] = {}

        self._terms: list[SpecTerm | AuxSpecTerm] = []
        self._results: list[Any] = []

        self._cache: dict[str, Any] = {}
        self._cache_stdout: dict[str, str] = {}

        self._scope_cache_keys: list[str] = []
        self._scope_cache_key: str | None = None

    def start_scope(self, scope: dict[str, SpecEvaluateReturn], cache_key: str) -> None:
        self._scopes.append(self._scope.copy())
        self._scope_cache_keys.append(self._scope_cache_key)

        self._scope.update(scope)
        self._scope_cache_key = cache_key

    def finish_scope(self) -> None:
        self._scope = self._scopes.pop()

        old_scope_cache_key = self._scope_cache_key
        self._scope_cache_key = self._scope_cache_keys.pop()

        if old_scope_cache_key and old_scope_cache_key in self._cache_stdout:
            self.append_to_stdout_cache(self._cache_stdout[old_scope_cache_key])

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

    def set_call_cache(self, value: Any) -> None:
        self._cache[self._scope_cache_key] = value

    def get_call_cache(self, key: str) -> Any:
        return self._cache.get(key)

    def append_to_stdout_cache(self, value: str) -> None:
        if self._scope_cache_key is None:
            return

        if self._scope_cache_key not in self._cache_stdout:
            self._cache_stdout[self._scope_cache_key] = value
        else:
            self._cache_stdout[self._scope_cache_key] += value

    def get_stdout_cache(self, key: str) -> str | None:
        return self._cache_stdout.get(key)
