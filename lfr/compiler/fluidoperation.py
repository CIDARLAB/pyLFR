class FluidOperation(object):

    def __init__(self, operandid: str, operator: str) -> None:
        self.id = operandid + "_" + operator

    def __str__(self):
        return self.id

    def __eq__(self, o: object) -> bool:
        return self.id == o.id
