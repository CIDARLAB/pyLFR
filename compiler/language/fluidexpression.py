# The operator order has to be correct in the array, if any of the things are off,
# other things will go off
from compiler.language.utils import is_number
from compiler.fluid import Fluid
from compiler.language.vectorrange import VectorRange


OPERATOR_ORDER = [['*', '/'], ['%'], ['+', '-']]
NUMERIC_OPERATOR_ORDER = [['/', '*'], ['%'], ['+', '-']]

class FluidExpression:

    def __init__(self) -> None:
        self.operatororder = OPERATOR_ORDER
        self.numericoperatororder = NUMERIC_OPERATOR_ORDER

    def processexpression(self, termlist, operatorlist, fig):

        # First go over the numeric operator order
        for operatorset in self.numericoperatororder:
            # For each set we start the processing the individual thing
            for operator in operatorset:
                # search for operators in the operatorlist
                # indices = [i for i, x in enumerate(operatorlist) if x == operator]
                index = None
                try:
                    index = operatorlist.index(operator)
                except ValueError:
                    index = -1

                # Now go over all these indices
                while index >= 0:
                    operand1 = termlist[index]
                    operand2 = termlist[index+1]
                    operation = operatorlist[index]
                    result = None

                    if is_number(operand1) and is_number(operand2):
                        # If both the terms are numbers then actually do the operation
                        result = FluidExpression.evaluateNumericValues(
                            operand1, operand2, operator)

                    # Remove the operator
                    del operatorlist[index]
                    # Put the result back in there
                    termlist[index:index+2] = [result]

                    try:
                        index = operatorlist.index(operator)
                    except ValueError:
                        index = -1

        # Second go over the fluidic operator order
        for operatorset in self.operatororder:
            # For each set we start the processing the individual thing
            for operator in operatorset:
                # search for operators in the operatorlist
                index = None
                try:
                    index = operatorlist.index(operator)
                except ValueError:
                    index = -1

                # Now go over all these indices
                while index >= 0:
                    operand1 = termlist[index]
                    operand2 = termlist[index+1]
                    operation = operatorlist[index]
                    result = None

                    if is_number(operand1) and is_number(operand2):
                        # If both the terms are numbers then actually do the operation
                        raise Exception(
                            "Cannot do fluidic operation on two numbers")
                    elif is_number(operand1):
                        print("Performing the operation: \n Operator - {2} \n Number - {0} \n Fluid - {1}".format(
                            operand1, operand2, operator))
                    elif is_number(operand2):
                        print("Performing the operation: \n Operator - {2} \n Number - {1} \n Fluid - {0}".format(
                            operand1, operand2, operator))
                    else:
                        # Perform the fig operation
                        print("Performing operation: {0} {1} {2}".format(
                            operand1, operation, operand2))
                        result = VectorRange(Fluid("TEST"), 0, 5)

                    # Put the result back in there
                    termlist[index:index+2] = [result]

                    try:
                        index = operatorlist.index(operator)
                    except ValueError:
                        index = -1
        
        return termlist


    @staticmethod
    def evaluateNumericValues(operand1, operand2, operator):
        result = None
        if operator is '*':
            result = operand1 * operand2
        elif operator is '/':
            result = operand1 / operand2
        elif operator is '%':
            result = operand1 % operand2
        elif operator is '+':
            result = operand1 + operand2
        elif operator is '-':
            result = operand1 - operand2
        else:
            raise Exception("Unsuppored operator on two numeric values: {0}".format(operator))

        return result

