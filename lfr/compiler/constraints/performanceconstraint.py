class PerformanceConstraintData(dict):
    
    def __init__(self, operator) -> None:
        self.__operator = operator

    @property
    def operator(self) -> str:
        return self.__operator

