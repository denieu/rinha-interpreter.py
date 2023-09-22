from rinha_interpreter.core.spec import (
    SpecBinary,
    SpecBinaryOp,
    SpecBool,
    SpecCall,
    SpecEvaluateReturn,
    SpecFirst,
    SpecFunction,
    SpecIf,
    SpecInt,
    SpecLet,
    SpecPrint,
    SpecSecond,
    SpecStr,
    SpecTerm,
    SpecTuple,
    SpecVar,
)


class Variables:
    def __init__(self) -> None:
        self._variables: list[dict[str, SpecEvaluateReturn]] = [{}]

    def start_scope(self) -> None:
        self._variables.append({})

    def finish_scope(self) -> None:
        if len(self._variables) > 1:
            self._variables.pop()

    def set_variable(self, name: str, value: SpecEvaluateReturn) -> None:
        self._variables[-1][name] = value

    def get_variable(self, name: str) -> SpecEvaluateReturn:
        for scope in reversed(self._variables):
            if name in scope:
                return scope[name]

        raise Exception(f"Variavel {name} não definida")


def evaluate(term: SpecTerm, variables: Variables) -> SpecEvaluateReturn:
    if isinstance(term, SpecInt):
        return int(term.value)

    if isinstance(term, SpecStr):
        return str(term.value)

    if isinstance(term, SpecCall):
        spec_call_args = [evaluate(argument, variables) for argument in term.arguments]
        spec_call_callee = evaluate(term.callee, variables)

        if callable(spec_call_callee):
            return spec_call_callee(spec_call_args)

        raise Exception("Invalid callable")

    if isinstance(term, SpecBinary):
        spec_binary_lhs_result = evaluate(term.lhs, variables)
        spec_binary_rhs_result = evaluate(term.rhs, variables)

        spec_binary_operator = term.op
        if spec_binary_operator == SpecBinaryOp.Add:
            if isinstance(spec_binary_lhs_result, str) or isinstance(spec_binary_rhs_result, str):
                return f"{spec_binary_lhs_result}{spec_binary_rhs_result}"

            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result + spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        if spec_binary_operator == SpecBinaryOp.Sub:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result - spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        if spec_binary_operator == SpecBinaryOp.Mul:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result * spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        if spec_binary_operator == SpecBinaryOp.Div:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result / spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        if spec_binary_operator == SpecBinaryOp.Rem:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result % spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        if spec_binary_operator == SpecBinaryOp.Eq:
            return spec_binary_lhs_result == spec_binary_rhs_result

        if spec_binary_operator == SpecBinaryOp.Neq:
            return spec_binary_lhs_result != spec_binary_rhs_result

        if spec_binary_operator == SpecBinaryOp.Lt:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result < spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        if spec_binary_operator == SpecBinaryOp.Gt:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result > spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        if spec_binary_operator == SpecBinaryOp.Lte:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result <= spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        if spec_binary_operator == SpecBinaryOp.Gte:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result >= spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        if spec_binary_operator == SpecBinaryOp.And:
            return spec_binary_lhs_result and spec_binary_rhs_result

        if spec_binary_operator == SpecBinaryOp.Or:
            return spec_binary_lhs_result or spec_binary_rhs_result

    if isinstance(term, SpecFunction):

        def closure(args: list[SpecEvaluateReturn]) -> SpecEvaluateReturn:
            variables.start_scope()

            for index, parameter in enumerate(term.parameters):
                parameter_name = parameter.text
                parameter_value = args[index]

                variables.set_variable(parameter_name, parameter_value)

            result = evaluate(term.value, variables)
            variables.finish_scope()

            return result

        return closure

    if isinstance(term, SpecLet):
        variables.set_variable(term.name.text, evaluate(term.value, variables))
        return evaluate(term.next, variables)

    if isinstance(term, SpecIf):
        spec_if_condition_result = evaluate(term.condition, variables)

        if spec_if_condition_result:
            return evaluate(term.then, variables)

        return evaluate(term.otherwise, variables)

    if isinstance(term, SpecPrint):
        spec_print_result = evaluate(term.value, variables)

        if isinstance(spec_print_result, str):
            print(spec_print_result)

        elif isinstance(spec_print_result, (int, float)):
            print(spec_print_result)

        elif isinstance(spec_print_result, bool):
            print(str(spec_print_result).lower())

        elif isinstance(spec_print_result, tuple):
            print(spec_print_result)

        elif callable(spec_print_result):
            print("<#closure>")

        else:
            raise Exception("Tipo invalido no print")

        return None

    if isinstance(term, SpecFirst):
        spec_first_result = evaluate(term.value, variables)
        if not isinstance(spec_first_result, tuple):
            raise Exception("Esperava que isso fosse uma tupla")

        return spec_first_result[0]

    if isinstance(term, SpecSecond):
        spec_second_result = evaluate(term.value, variables)
        if not isinstance(spec_second_result, tuple):
            raise Exception("Esperava que isso fosse uma tupla")

        return spec_second_result[1]

    if isinstance(term, SpecBool):
        return bool(term.value)

    if isinstance(term, SpecTuple):
        return evaluate(term.first, variables), evaluate(term.second, variables)

    if isinstance(term, SpecVar):
        return variables.get_variable(term.text)

    raise Exception("Term invalido")
