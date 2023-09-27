from typing import Callable, Literal

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
    "Add": lambda _lhs, _rhs: f"{_lhs}{_rhs}" if isinstance(_lhs, str) or isinstance(_rhs, str) else _lhs + _rhs,
    "Sub": lambda _lhs, _rhs: _lhs - _rhs,
    "Mul": lambda _lhs, _rhs: _lhs * _rhs,
    "Div": lambda _lhs, _rhs: _lhs / _rhs,
    "Rem": lambda _lhs, _rhs: _lhs % _rhs,
    "Eq": lambda _lhs, _rhs: _lhs == _rhs,
    "Neq": lambda _lhs, _rhs: _lhs != _rhs,
    "Lt": lambda _lhs, _rhs: _lhs < _rhs,
    "Gt": lambda _lhs, _rhs: _lhs > _rhs,
    "Lte": lambda _lhs, _rhs: _lhs <= _rhs,
    "Gte": lambda _lhs, _rhs: _lhs >= _rhs,
    "And": lambda _lhs, _rhs: _lhs and _rhs,
    "Or": lambda _lhs, _rhs: _lhs or _rhs,
}


def _eval_spec_int(_term: SpecInt, _environment: Environment) -> None:
    _environment.save_evaluate_result(int(_term["value"]))


def _eval_spec_str(_term: SpecStr, _environment: Environment) -> None:
    _environment.save_evaluate_result(str(_term["value"]))


def _eval_spec_call(_term: SpecCall, _environment: Environment) -> None:
    _environment.add_term_to_evaluate({"kind": "AuxSpecCallStart"})

    _environment.add_term_to_evaluate(_term["callee"])
    for argument in _term["arguments"]:
        _environment.add_term_to_evaluate(argument)


def _eval_aux_spec_call_start(_term: Literal["AuxSpecCallStart"], _environment: Environment) -> None:
    spec_call_callee = _environment.get_evaluate_result()
    if not spec_call_callee.get("kind") == "Function":
        raise Exception("Invalid callable")

    new_scope = {}
    for parameter in spec_call_callee["parameters"]:
        parameter_name = parameter["text"]
        parameter_value = _environment.get_evaluate_result()

        new_scope[parameter_name] = parameter_value

    _environment.start_scope(new_scope)
    _environment.add_term_to_evaluate({"kind": "AuxSpecCallFinish"})

    _environment.add_term_to_evaluate(spec_call_callee["value"])


def _eval_aux_spec_call_finish(_term: Literal["AuxSpecCallFinish"], _environment: Environment) -> None:
    _environment.finish_scope()


def _eval_spec_binary(_term: SpecBinary, _environment: Environment) -> None:
    _environment.add_term_to_evaluate({"kind": "AuxSpecBinaryFinish"})

    _environment.save_evaluate_result(_term["op"])

    _environment.add_term_to_evaluate(_term["lhs"])
    _environment.add_term_to_evaluate(_term["rhs"])


def _eval_aux_spec_binary_finish(_term: Literal["AuxSpecBinaryFinish"], _environment: Environment) -> None:
    lhs_value = _environment.get_evaluate_result()
    rhs_value = _environment.get_evaluate_result()

    op_value = _environment.get_evaluate_result()

    _environment.save_evaluate_result(spec_binary_ops[op_value](lhs_value, rhs_value))


def _eval_spec_function(_term: SpecFunction, _environment: Environment) -> None:
    _environment.save_evaluate_result(_term)


def _eval_spec_let(_term: SpecLet, _environment: Environment) -> None:
    _environment.add_term_to_evaluate({"kind": "AuxSpecLetSet"})

    _environment.save_evaluate_result(_term["name"]["text"])
    _environment.save_evaluate_result(_term["next"])

    _environment.add_term_to_evaluate(_term["value"])


def _eval_aux_spec_let_set(_term: Literal["AuxSpecLetSet"], _environment: Environment) -> None:
    let_value = _environment.get_evaluate_result()
    let_next = _environment.get_evaluate_result()
    let_name = _environment.get_evaluate_result()

    _environment.set_variable(let_name, let_value)
    _environment.add_term_to_evaluate(let_next)


def _eval_spec_if(_term: SpecIf, _environment: Environment) -> None:
    _environment.add_term_to_evaluate({"kind": "AuxSpecIfHandleCondition"})

    _environment.save_evaluate_result(_term["otherwise"])
    _environment.save_evaluate_result(_term["then"])

    _environment.add_term_to_evaluate(_term["condition"])


def _eval_aux_spec_if_handle_condition(_term: Literal["AuxSpecIfHandleCondition"], _environment: Environment) -> None:
    condition_result = _environment.get_evaluate_result()

    spec_if_then = _environment.get_evaluate_result()
    spec_if_otherwise = _environment.get_evaluate_result()

    if condition_result:
        _environment.add_term_to_evaluate(spec_if_then)
    else:
        _environment.add_term_to_evaluate(spec_if_otherwise)


def _eval_spec_print(_term: SpecPrint, _environment: Environment) -> int:
    _environment.add_term_to_evaluate({"kind": "AuxSpecPrintFinish"})
    _environment.add_term_to_evaluate(_term["value"])


def _eval_aux_spec_print_finish(_term: Literal["AuxSpecPrintFinish"], _environment: Environment) -> None:
    spec_print_result = _environment.get_evaluate_result()

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

    _environment.save_evaluate_result(spec_print_result)


def _eval_spec_first(_term: SpecFirst, _environment: Environment) -> None:
    _environment.add_term_to_evaluate({"kind": "AuxSpecFirstFinish"})
    _environment.add_term_to_evaluate(_term["value"])


def _eval_aux_spec_first_finish(_term: Literal["AuxSpecFirstFinish"], _environment: Environment) -> None:
    tuple_to_first = _environment.get_evaluate_result()

    if not isinstance(tuple_to_first, tuple):
        raise Exception("Esperava que isso fosse uma tupla")

    _environment.save_evaluate_result(tuple_to_first[0])


def _eval_spec_second(_term: SpecSecond, _environment: Environment) -> None:
    _environment.add_term_to_evaluate({"kind": "AuxSpecSecondFinish"})
    _environment.add_term_to_evaluate(_term["value"])


def _eval_aux_spec_second_finish(_term: Literal["AuxSpecSecondFinish"], _environment: Environment) -> None:
    tuple_to_second = _environment.get_evaluate_result()

    if not isinstance(tuple_to_second, tuple):
        raise Exception("Esperava que isso fosse uma tupla")

    _environment.save_evaluate_result(tuple_to_second[1])


def _eval_spec_bool(_term: SpecBool, _environment: Environment) -> None:
    _environment.save_evaluate_result(_term["value"])


def _eval_spec_tuple(_term: SpecTuple, _environment: Environment) -> None:
    _environment.add_term_to_evaluate({"kind": "AuxSpecTupleFinish"})
    _environment.add_term_to_evaluate(_term["second"])
    _environment.add_term_to_evaluate(_term["first"])


def _eval_aux_spec_tuple_finish(_term: Literal["AuxSpecTupleFinish"], _environment: Environment) -> None:
    tuple_first = _environment.get_evaluate_result()
    tuple_second = _environment.get_evaluate_result()

    _environment.save_evaluate_result((tuple_first, tuple_second))


def _eval_spec_var(_term: SpecVar, _environment: Environment) -> None:
    _environment.save_evaluate_result(_environment.get_variable(_term["text"]))


spec_terms: dict[SpecTerm, Callable[[SpecTerm, Environment], SpecEvaluateReturn]] = {
    "Int": _eval_spec_int,
    "Str": _eval_spec_str,
    "Call": _eval_spec_call,
    "AuxSpecCallStart": _eval_aux_spec_call_start,
    "AuxSpecCallFinish": _eval_aux_spec_call_finish,
    "Binary": _eval_spec_binary,
    "AuxSpecBinaryFinish": _eval_aux_spec_binary_finish,
    "Function": _eval_spec_function,
    "Let": _eval_spec_let,
    "AuxSpecLetSet": _eval_aux_spec_let_set,
    "If": _eval_spec_if,
    "AuxSpecIfHandleCondition": _eval_aux_spec_if_handle_condition,
    "Print": _eval_spec_print,
    "AuxSpecPrintFinish": _eval_aux_spec_print_finish,
    "First": _eval_spec_first,
    "AuxSpecFirstFinish": _eval_aux_spec_first_finish,
    "Second": _eval_spec_second,
    "AuxSpecSecondFinish": _eval_aux_spec_second_finish,
    "Bool": _eval_spec_bool,
    "Tuple": _eval_spec_tuple,
    "AuxSpecTupleFinish": _eval_aux_spec_tuple_finish,
    "Var": _eval_spec_var,
}


def evaluate(environment: Environment) -> SpecEvaluateReturn:
    while (term := environment.get_term_to_evaluate()) is not None:
        spec_terms[term["kind"]](term, environment)
