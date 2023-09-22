from rinha_interpreter.core.spec import (
    SpecBinary,
    SpecBool,
    SpecCall,
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
    SpecVar, SpecBinaryOp,
)


def evaluate(term: SpecTerm) -> int | tuple | None:
    if isinstance(term, SpecInt):
        return int(term.value)

    elif isinstance(term, SpecStr):
        return str(term.value)

    elif isinstance(term, SpecCall):
        pass

    elif isinstance(term, SpecBinary):
        spec_binary_lhs_result = evaluate(term.lhs)
        spec_binary_rhs_result = evaluate(term.rhs)

        spec_binary_operator = term.op
        if spec_binary_operator == SpecBinaryOp.Add:
            if isinstance(spec_binary_lhs_result, str) or isinstance(spec_binary_rhs_result, str):
                return f"{spec_binary_lhs_result}{spec_binary_rhs_result}"

            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result + spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        elif spec_binary_operator == SpecBinaryOp.Sub:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result - spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        elif spec_binary_operator == SpecBinaryOp.Mul:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result * spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        elif spec_binary_operator == SpecBinaryOp.Div:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result / spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        elif spec_binary_operator == SpecBinaryOp.Rem:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result % spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        elif spec_binary_operator == SpecBinaryOp.Eq:
            return spec_binary_lhs_result == spec_binary_rhs_result

        elif spec_binary_operator == SpecBinaryOp.Neq:
            return spec_binary_lhs_result != spec_binary_rhs_result

        elif spec_binary_operator == SpecBinaryOp.Lt:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result < spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        elif spec_binary_operator == SpecBinaryOp.Gt:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result > spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        elif spec_binary_operator == SpecBinaryOp.Lte:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result <= spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        elif spec_binary_operator == SpecBinaryOp.Gte:
            if isinstance(spec_binary_lhs_result, (int, float)) and isinstance(spec_binary_rhs_result, (int, float)):
                return spec_binary_lhs_result >= spec_binary_rhs_result

            raise Exception("Operação binario invalida")

        elif spec_binary_operator == SpecBinaryOp.And:
            return spec_binary_lhs_result and spec_binary_rhs_result

        elif spec_binary_operator == SpecBinaryOp.Or:
            return spec_binary_lhs_result or spec_binary_rhs_result

    elif isinstance(term, SpecFunction):
        pass

    elif isinstance(term, SpecLet):
        pass

    elif isinstance(term, SpecIf):
        spec_if_condition_result = evaluate(term.condition)

        if spec_if_condition_result:
            return evaluate(term.then)

        return evaluate(term.otherwise)

    elif isinstance(term, SpecPrint):
        spec_print_result = evaluate(term.value)

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

    elif isinstance(term, SpecFirst):
        spec_first_result = evaluate(term.value)
        if not isinstance(spec_first_result, tuple):
            raise Exception("Esperava que isso fosse uma tupla")

        return spec_first_result[0]

    elif isinstance(term, SpecSecond):
        spec_second_result = evaluate(term.value)
        if not isinstance(spec_second_result, tuple):
            raise Exception("Esperava que isso fosse uma tupla")

        return spec_second_result[1]

    elif isinstance(term, SpecBool):
        return bool(term.value)

    elif isinstance(term, SpecTuple):
        return evaluate(term.first), evaluate(term.second)

    elif isinstance(term, SpecVar):
        pass

    else:
        raise Exception("Term invalido")
