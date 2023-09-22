# pylint: disable=invalid-name, function-redefined
# mypy: disable-error-code="no-redef"
from enum import Enum
from typing import Literal

from pydantic import BaseModel


class SpecLocation(BaseModel):
    start: int
    end: int
    filename: str


class SpecParameter(BaseModel):
    text: str
    location: SpecLocation


class SpecVar(BaseModel):
    kind: Literal["Var"]
    text: str
    location: SpecLocation


class SpecFunction(BaseModel):
    kind: Literal["Function"]
    parameters: list[SpecParameter]
    value: "SpecTerm"
    location: SpecLocation


class SpecCall(BaseModel):
    kind: Literal["Call"]
    calee: "SpecTerm"
    arguments: list["SpecTerm"]
    location: SpecLocation


class SpecLet(BaseModel):
    kind: Literal["Let"]
    name: SpecParameter
    value: "SpecTerm"
    next: "SpecTerm"
    location: SpecLocation


class SpecStr(BaseModel):
    kind: Literal["Str"]
    value: str
    location: SpecLocation


class SpecInt(BaseModel):
    kind: Literal["Int"]
    value: float
    location: SpecLocation


class SpecBinaryOp(Enum):
    Add = "Add"
    Sub = "Sub"
    Mul = "Mul"
    Div = "Div"
    Rem = "Rem"
    Eq = "Eq"
    Neq = "Neq"
    Lt = "Lt"
    Gt = "Gt"
    Lte = "Lte"
    Gte = "Gte"
    And = "And"
    Or = "Or"


class SpecBool(BaseModel):
    kind: Literal["Bool"]
    value: bool
    location: SpecLocation


class SpecIf(BaseModel):
    kind: Literal["If"]
    condition: "SpecTerm"
    then: "SpecTerm"
    otherwise: "SpecTerm"
    location: SpecLocation


class SpecBinary(BaseModel):
    kind: Literal["Binary"]
    lhs: "SpecTerm"
    op: SpecBinaryOp
    rhs: "SpecTerm"
    location: SpecLocation


class SpecTuple(BaseModel):
    kind: Literal["Tuple"]
    first: "SpecTerm"
    second: "SpecTerm"
    location: SpecLocation


class SpecFirst(BaseModel):
    kind: Literal["First"]
    value: "SpecTerm"
    location: SpecLocation


class SpecSecond(BaseModel):
    kind: Literal["Second"]
    value: "SpecTerm"
    location: SpecLocation


class SpecPrint(BaseModel):
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


class SpecFile(BaseModel):
    name: str
    expression: SpecTerm
    location: SpecLocation
