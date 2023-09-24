from typing import Callable

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


binary_operators: dict[SpecBinaryOp, Callable[[SpecEvaluateReturn, SpecEvaluateReturn], bool]] = {
    SpecBinaryOp.Add: lambda _lhs, _rhs: f"{_lhs}{_rhs}" if isinstance(_lhs, str) or isinstance(_rhs, str) else _lhs + _rhs,
    SpecBinaryOp.Sub: lambda _lhs, _rhs: _lhs - _rhs,
    SpecBinaryOp.Mul: lambda _lhs, _rhs: _lhs * _rhs,
    SpecBinaryOp.Div: lambda _lhs, _rhs: _lhs / _rhs,
    SpecBinaryOp.Rem: lambda _lhs, _rhs: _lhs % _rhs,
    SpecBinaryOp.Eq: lambda _lhs, _rhs: _lhs == _rhs,
    SpecBinaryOp.Neq: lambda _lhs, _rhs: _lhs != _rhs,
    SpecBinaryOp.Lt: lambda _lhs, _rhs: _lhs < _rhs,
    SpecBinaryOp.Gt: lambda _lhs, _rhs: _lhs > _rhs,
    SpecBinaryOp.Lte: lambda _lhs, _rhs: _lhs <= _rhs,
    SpecBinaryOp.Gte: lambda _lhs, _rhs: _lhs >= _rhs,
    SpecBinaryOp.And: lambda _lhs, _rhs: _lhs and _rhs,
    SpecBinaryOp.Or: lambda _lhs, _rhs: _lhs or _rhs,
}


def evaluate_binary_operator(operator: SpecBinaryOp, lhs: SpecEvaluateReturn, rhs: SpecEvaluateReturn) -> bool:
    return binary_operators[operator](lhs, rhs)


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
        return evaluate_binary_operator(term.op, evaluate(term.lhs, environment), evaluate(term.rhs, environment))

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
