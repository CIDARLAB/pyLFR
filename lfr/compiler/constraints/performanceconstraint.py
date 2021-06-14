class PerformanceConstraintData(dict):
    def __init__(self, operator) -> None:
        super().__init__()
        self.__operator = operator

    @property
    def operator(self) -> str:
        return self.__operator
