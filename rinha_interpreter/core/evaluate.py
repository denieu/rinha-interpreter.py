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

spec_binary_ops: dict[SpecBinaryOp, Callable[[SpecEvaluateReturn, SpecEvaluateReturn], bool]] = {
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


def _eval_spec_int(_term: SpecInt, _environment: Environment) -> int:
    return int(_term.value)


def _eval_spec_str(_term: SpecStr, _environment: Environment) -> str:
    return str(_term.value)


def _eval_spec_call(_term: SpecCall, _environment: Environment) -> SpecEvaluateReturn:
    spec_call_callee = evaluate(_term.callee, _environment)
    if not isinstance(spec_call_callee, SpecFunction):
        raise Exception("Invalid callable")

    new_scope = {}
    for index, parameter in enumerate(spec_call_callee.parameters):
        argument = _term.arguments[index]

        parameter_name = parameter.text
        parameter_value = evaluate(argument, _environment)

        new_scope[parameter_name] = parameter_value

    _environment.start_scope(new_scope)
    result = evaluate(spec_call_callee.value, _environment)
    _environment.finish_scope()

    return result


def _eval_spec_binary(_term: SpecBinary, _environment: Environment) -> bool:
    return spec_binary_ops[_term.op](evaluate(_term.lhs, _environment), evaluate(_term.rhs, _environment))


def _eval_spec_function(_term: SpecFunction, _environment: Environment) -> SpecFunction:
    return _term


def _eval_spec_let(_term: SpecLet, _environment: Environment) -> SpecEvaluateReturn:
    _environment.set_variable(_term.name.text, evaluate(_term.value, _environment))
    return evaluate(_term.next, _environment)


def _eval_spec_if(_term: SpecIf, _environment: Environment) -> int:
    spec_if_condition_result = evaluate(_term.condition, _environment)

    if spec_if_condition_result:
        return evaluate(_term.then, _environment)

    return evaluate(_term.otherwise, _environment)


def _eval_spec_print(_term: SpecPrint, _environment: Environment) -> int:
    spec_print_result = evaluate(_term.value, _environment)

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


def _eval_spec_first(_term: SpecFirst, _environment: Environment) -> int:
    spec_first_result = evaluate(_term.value, _environment)
    if not isinstance(spec_first_result, tuple):
        raise Exception("Esperava que isso fosse uma tupla")

    return spec_first_result[0]


def _eval_spec_second(_term: SpecSecond, _environment: Environment) -> int:
    spec_second_result = evaluate(_term.value, _environment)
    if not isinstance(spec_second_result, tuple):
        raise Exception("Esperava que isso fosse uma tupla")

    return spec_second_result[1]


def _eval_spec_bool(_term: SpecBool, _environment: Environment) -> int:
    return bool(_term.value)


def _eval_spec_tuple(_term: SpecTuple, _environment: Environment) -> int:
    return evaluate(_term.first, _environment), evaluate(_term.second, _environment)


def _eval_spec_var(_term: SpecVar, _environment: Environment) -> int:
    return _environment.get_variable(_term.text)


spec_terms: dict[SpecTerm, Callable[[SpecTerm, Environment], SpecEvaluateReturn]] = {
    SpecInt: _eval_spec_int,
    SpecStr: _eval_spec_str,
    SpecCall: _eval_spec_call,
    SpecBinary: _eval_spec_binary,
    SpecFunction: _eval_spec_function,
    SpecLet: _eval_spec_let,
    SpecIf: _eval_spec_if,
    SpecPrint: _eval_spec_print,
    SpecFirst: _eval_spec_first,
    SpecSecond: _eval_spec_second,
    SpecBool: _eval_spec_bool,
    SpecTuple: _eval_spec_tuple,
    SpecVar: _eval_spec_var,
}


def evaluate(term: SpecTerm, environment: Environment) -> SpecEvaluateReturn:
    return spec_terms[type(term)](term, environment)
