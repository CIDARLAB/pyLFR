from enum import Enum

class ErrorType(Enum):
    MODULE_IO_NOT_FOUND = 10

class LFRError:
    def __init__(self, errortype: ErrorType, message: str):
        self.errortype = errortype
        self.message = message

    def __str__(self):
        return "Error Type: {0.errortype}, Message: {0.message}".format(self)

