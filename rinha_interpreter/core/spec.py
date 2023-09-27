# pylint: disable=invalid-name, function-redefined
# mypy: disable-error-code="no-redef"
from typing import Literal, TypedDict


class SpecLocation(TypedDict):
    start: int
    end: int
    filename: str


class SpecParameter(TypedDict):
    text: str
    location: SpecLocation


class SpecVar(TypedDict):
    kind: Literal["Var"]
    text: str
    location: SpecLocation


class SpecFunction(TypedDict):
    kind: Literal["Function"]
    parameters: list[SpecParameter]
    value: "SpecTerm"
    location: SpecLocation


class SpecCall(TypedDict):
    kind: Literal["Call"]
    callee: "SpecTerm"
    arguments: list["SpecTerm"]
    location: SpecLocation


class SpecLet(TypedDict):
    kind: Literal["Let"]
    name: SpecParameter
    value: "SpecTerm"
    next: "SpecTerm"
    location: SpecLocation


class SpecStr(TypedDict):
    kind: Literal["Str"]
    value: str
    location: SpecLocation


class SpecInt(TypedDict):
    kind: Literal["Int"]
    value: float
    location: SpecLocation


SpecBinaryOp = Literal["Add", "Sub", "Mul", "Div", "Rem", "Eq", "Neq", "Lt", "Gt", "Lte", "Gte", "And", "Or"]


class SpecBool(TypedDict):
    kind: Literal["Bool"]
    value: bool
    location: SpecLocation


class SpecIf(TypedDict):
    kind: Literal["If"]
    condition: "SpecTerm"
    then: "SpecTerm"
    otherwise: "SpecTerm"
    location: SpecLocation


class SpecBinary(TypedDict):
    kind: Literal["Binary"]
    lhs: "SpecTerm"
    op: SpecBinaryOp
    rhs: "SpecTerm"
    location: SpecLocation


class SpecTuple(TypedDict):
    kind: Literal["Tuple"]
    first: "SpecTerm"
    second: "SpecTerm"
    location: SpecLocation


class SpecFirst(TypedDict):
    kind: Literal["First"]
    value: "SpecTerm"
    location: SpecLocation


class SpecSecond(TypedDict):
    kind: Literal["Second"]
    value: "SpecTerm"
    location: SpecLocation


class SpecPrint(TypedDict):
    kind: Literal["Print"]
    value: "SpecTerm"
    location: SpecLocation


SpecTerm = (
    SpecInt
    | SpecStr
    | SpecCall
    | SpecBinary
    | SpecFunction
    | SpecLet
    | SpecIf
    | SpecPrint
    | SpecFirst
    | SpecSecond
    | SpecBool
    | SpecTuple
    | SpecVar
)


class SpecFile(TypedDict):
    name: str
    expression: SpecTerm
    location: SpecLocation


class AuxSpecTerm(TypedDict):
    kind: Literal[
        "AuxSpecCallStart",
        "AuxSpecCallFinish",
        "AuxSpecBinaryFinish",
        "AuxSpecLetSet",
        "AuxSpecIfHandleCondition",
        "AuxSpecPrintFinish",
        "AuxSpecFirstFinish",
        "AuxSpecSecondFinish",
        "AuxSpecTupleFinish",
    ]


SpecEvaluateBasicReturn = int | float | str | bool
SpecEvaluateReturn = SpecEvaluateBasicReturn | SpecFunction | tuple["SpecEvaluateReturn", "SpecEvaluateReturn"]
