# The operator order has to be correct in the array, if any of the things are off,
# other things will go off
from compiler.fluid import Fluid
from compiler.language.vectorrange import VectorRange


OPERATOR_ORDER = [['*', '/'], ['%'], ['+', '-']]

class FluidExpression:

    def __init__(self) -> None:
        self.operatororder = OPERATOR_ORDER

    def processexpression(self, termlist, operatorlist, fig):        
        #First go over the operator order
        for operatorset in self.operatororder:
            #For each set we start the processing the individual thing
            for operator in operatorset:
                #search for operators in the operator list
                indices = [i for i, x in enumerate(operatorlist) if x == operator]

                #Now go over all these indices
                for index in indices:
                    operand1 = termlist[index]
                    operand2 = termlist[index+1]
                    operation = operatorlist[index]

                    #Perform the fig operation
                    print("Performing operation: {0} {1} {2}".format(operand1, operation, operand2))
                    result = VectorRange(Fluid("TEST"),0, 5)
                    
                    #Put the result back in there
                    termlist[index:index+2] = [result]

        print("Final Termlist: ", termlist)
        
        return termlist
