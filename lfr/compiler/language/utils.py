from lfr.compiler.language.vectorrange import VectorRange


def is_number(n) -> bool:
    # TODO - Revisit this logic yet again
    if isinstance(n, VectorRange):
        return isinstance(n[0], (float, int))
    else:
        return isinstance(n, (float, int))
