from rinha_interpreter.core.environment import Environment
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


def evaluate(term: SpecTerm, environment: Environment) -> SpecEvaluateReturn:
    term_type = type(term)

    if term_type == SpecInt:
        return int(term.value)

    if term_type == SpecStr:
        return str(term.value)

    if term_type == SpecCall:
        spec_call_callee = evaluate(term.callee, environment)
        if not isinstance(spec_call_callee, SpecFunction):
            raise Exception("Invalid callable")

        new_scope = {}
        for index, parameter in enumerate(spec_call_callee.parameters):
            argument = term.arguments[index]

            parameter_name = parameter.text
            parameter_value = evaluate(argument, environment)

            new_scope[parameter_name] = parameter_value

        environment.start_scope(new_scope)
        result = evaluate(spec_call_callee.value, environment)
        environment.finish_scope()

        return result

    if term_type == SpecBinary:
        spec_binary_lhs_result = evaluate(term.lhs, environment)
        spec_binary_rhs_result = evaluate(term.rhs, environment)

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

    if term_type == SpecFunction:
        return term

    if term_type == SpecLet:
        environment.set_variable(term.name.text, evaluate(term.value, environment))
        return evaluate(term.next, environment)

    if term_type == SpecIf:
        spec_if_condition_result = evaluate(term.condition, environment)

        if spec_if_condition_result:
            return evaluate(term.then, environment)

        return evaluate(term.otherwise, environment)

    if term_type == SpecPrint:
        spec_print_result = evaluate(term.value, environment)

        if isinstance(spec_print_result, str):
            print(spec_print_result)

        elif isinstance(spec_print_result, (int, float)):
            print(spec_print_result)

        elif isinstance(spec_print_result, bool):
            print(str(spec_print_result).lower())

        elif isinstance(spec_print_result, tuple):
            print(spec_print_result)

        elif isinstance(spec_print_result, SpecFunction):
            print("<#closure>")

        else:
            raise Exception("Tipo invalido no print")

        return spec_print_result

    if term_type == SpecFirst:
        spec_first_result = evaluate(term.value, environment)
        if not isinstance(spec_first_result, tuple):
            raise Exception("Esperava que isso fosse uma tupla")

        return spec_first_result[0]

    if term_type == SpecSecond:
        spec_second_result = evaluate(term.value, environment)
        if not isinstance(spec_second_result, tuple):
            raise Exception("Esperava que isso fosse uma tupla")

        return spec_second_result[1]

    if term_type == SpecBool:
        return bool(term.value)

    if term_type == SpecTuple:
        return evaluate(term.first, environment), evaluate(term.second, environment)

    if term_type == SpecVar:
        return environment.get_variable(term.text)

    raise Exception("Term invalido")
