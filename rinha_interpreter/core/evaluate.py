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
    SpecVar,
)


def evaluate(term: SpecTerm) -> int | tuple | None:
    if isinstance(term, SpecInt):
        return int(term.value)

    elif isinstance(term, SpecStr):
        return str(term.value)

    elif isinstance(term, SpecCall):
        pass

    elif isinstance(term, SpecBinary):
        pass

    elif isinstance(term, SpecFunction):
        pass

    elif isinstance(term, SpecLet):
        pass

    elif isinstance(term, SpecIf):
        pass

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
