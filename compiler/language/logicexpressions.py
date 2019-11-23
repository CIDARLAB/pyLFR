# The operator order has to be correct in the array, if any of the things are off,
# other things will go off
OPERATOR_ORDER = [['*', '/'], ['%'], ['+', '-']]


class LogicExpression:

    def __init__(self, terms, operators) -> None:
        self.operators = operators
        self.terms = terms
