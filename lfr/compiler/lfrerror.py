from enum import Enum


class ErrorType(Enum):
    COMPILER_NOT_IMPLEMENTED = 0
    MODULE_IO_NOT_FOUND = 10
    VECTOR_SIZE_MISMATCH = 20
    VARIABLE_NOT_RECOGNIZED = 30
    SIGNAL_NOT_FOUND = 40
    MODULE_NOT_FOUND = 50


class LFRError:
    def __init__(self, errortype: ErrorType, message: str):
        self.errortype = errortype
        self.message = message

    def __str__(self):
        return "Error Type: {0.errortype}, Message: {0.message}".format(self)
