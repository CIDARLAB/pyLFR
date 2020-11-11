# The operator order has to be correct in the array, if any of the things are off,
# other things will go off
from lfr.fig.interaction import Interaction, InteractionType
from lfr.compiler.language.utils import is_number
from lfr.compiler.language.vector import Vector


OPERATOR_ORDER = [['*', '/'], ['%'], ['+', '-']]
NUMERIC_OPERATOR_ORDER = [['/', '*'], ['%'], ['+', '-']]


class FluidExpression:

    def __init__(self, module) -> None:
        self.currentmodule = module
        self.operatororder = OPERATOR_ORDER
        self.numericoperatororder = NUMERIC_OPERATOR_ORDER

    def process_expression(self, termlist, operatorlist):

        # In ste1, we go over and complete all the numeric operations in the precedence of
        # numeric operation order. It is possible that there are no numeric operations going
        # on in the expression. In that case we have the option to go to the next step. It
        # is also possible there are purely numeric operations and hence we only delete terms
        # if the numeric operation happens. In the second scenario, logic dictates that every
        # find will require us to delete the operator and the term.

        # First go over the numeric operator order
        for operatorset in self.numericoperatororder:
            # For each set we start the processing the individual thing
            for operator in operatorset:
                # search for operators in the operatorlist
                indices = [i for i, x in enumerate(operatorlist) if x is operator]
                # index = None
                # try:
                #     index = operatorlist.index(operator)
                # except ValueError:
                #     index = -1

                # Now go over all these indices
                while len(indices) > 0:
                    index = indices.pop(0)
                    operand1 = termlist[index]
                    operand2 = termlist[index+1]
                    operation = operatorlist[index]
                    result = None

                    if is_number(operand1) and is_number(operand2):
                        # If both the terms are numbers then actually do the operation
                        result = FluidExpression.evaluate_numeric_operator(
                            operand1, operand2, operator)

                        # Remove the operator
                        del operatorlist[index]
                        # Put the result back in there
                        termlist[index:index+2] = [result]
                        # Update the indices
                        indices = [i for i, x in enumerate(operatorlist) if x is operator]

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
                        result = self.__evaluate_fluid_numeric_operator(
                            operand2, operand1, operator)
                    elif is_number(operand2):
                        print("Performing the operation: \n Operator - {2} \n Number - {1} \n Fluid - {0}".format(
                            operand1, operand2, operator))
                        result = self.__evaluate_fluid_numeric_operator(
                            operand1, operand2, operator)
                    else:
                        # Perform the fig operation
                        print("Performing operation: {0} {1} {2}".format(
                            operand1, operation, operand2))
                        result = self.__evalute_fluid_fluid_operator(
                            operand1, operand2, operator)

                    # Delete the operator from the list
                    del operatorlist[index]
                    # Put the result back in there
                    termlist[index:index+2] = [result]

                    try:
                        index = operatorlist.index(operator)
                    except ValueError:
                        index = -1

        # At the end of the expression, there should only be 1 expression left
        return termlist[0]

    def process_unary_operation(self, term, operator):
        result = []
        interaction = None
        for element in term:
            if isinstance(element, Interaction):
                interaction = self.currentmodule.add_finteraction_custom_interaction(element, operator, InteractionType.TECHNOLOGY_PROCESS)
            else:
                interaction = self.currentmodule.add_fluid_custom_interaction(element, operator, InteractionType.TECHNOLOGY_PROCESS)

            result.append(interaction)

        v = Vector.create_from_list_things(operator, result)
        ret = v.get_range()
        return ret

    def __evalute_fluid_fluid_operator(self, operand1, operand2, operator):
        if len(operand1) is not len(operand2):
            # TODO - Implement Fluidic operators on non equal
            # dimensions of the operands
            raise Exception("Operand {0} and Operand {1} are of different Dimensions".format(operand1, operand2))

        operand1_element = None
        operand2_element = None
        interactiontype = None
        result = []
        vecname = operand1.id + "_" + operand2.id

        # TODO: Find out why the zip give a None item at the end
        # for operand1_element, operand2_element in zip(operand1, operand2):
        for i in range(len(operand1)):
            operand1_element = operand1[i]
            operand2_element = operand2[i]

            if operator == '*':
                raise Exception(
                    "Unsuppored operator on two fluid values: {0}".format(operator))
            elif operator == '/':
                raise Exception(
                    "Unsuppored operator on two fluid values: {0}".format(operator))
            elif operator == '%':
                raise Exception(
                    "Unsuppored operator on two fluid values: {0}".format(operator))
            elif operator == '+':
                # TODO: We need to return the operation node here that is generated by operating on the
                # two different operators
                interactiontype = InteractionType.MIX
            elif operator == '-':
                # TODO: In case of substraction, we need to return the operand1 back again,
                # since the subtracted node becomes an output, of whats given to the fluid
                interactiontype = InteractionType.SIEVE
            else:
                raise Exception(
                    "Unsuppored operator on two fluid values: {0}".format(operator))

            # TODO: Check if the operation here is between two different fluids or a fluid and an fluidinteraction
            if isinstance(operand1_element, Interaction) and isinstance(operand2_element, Interaction):
                result_element = self.currentmodule.add_finteraction_finteraction_interaction(operand1_element, operand2_element, interactiontype)
            elif isinstance(operand1_element, Interaction):
                result_element = self.currentmodule.add_fluid_finteraction_interaction(operand2_element, operand1_element, interactiontype)
            elif isinstance(operand2_element, Interaction):
                result_element = self.currentmodule.add_fluid_finteraction_interaction(operand1_element, operand2_element, interactiontype)
            else:
                result_element = self.currentmodule.add_fluid_fluid_interaction(operand1_element, operand2_element, interactiontype)

            result.append(result_element)

        v = Vector.create_from_list_things(vecname, result)
        return v.get_range()

    def __evaluate_fluid_numeric_operator(self, operand_fluidic, operand_numeric, operator):

        fluid = operand_fluidic[0]
        interactions = []
        for fluid in operand_fluidic:
            interaction = None
            if operator == '*':
                # TODO: Create interaction/operation node(s) on the FIG
                interaction = self.currentmodule.add_fluid_numeric_interaction(fluid, operand_numeric, InteractionType.DILUTE)
            elif operator == '/':
                # TODO: Create interaction/operation node(s) on the FIG
                interaction = self.currentmodule.add_fluid_numeric_interaction(fluid, operand_numeric, InteractionType.DIVIDE)
            elif operator == '%':
                # TODO: Create interaction/operation node(s) on the FIG
                interaction = self.currentmodule.add_fluid_numeric_interaction(fluid, operand_numeric, InteractionType.METER)
            elif operator == '+':
                raise Exception(
                    "Unsuppored operator on 1:fluidic 2:numeric values: {0}".format(operator))
            elif operator == '-':
                raise Exception(
                    "Unsuppored operator on 1:fluidic 2:numeric values: {0}".format(operator))
            else:
                raise Exception(
                    "Unsuppored operator on 1:fluidic 2:numeric values: {0}".format(operator))

            interactions.append(interaction)

        v = Vector.create_from_list_things("interaction_" + operand_fluidic.id, interactions)
        result = v.get_range()
        return result

    @staticmethod
    def evaluate_numeric_operator(operand1, operand2, operator):
        result = None
        if operator == '*':
            result = operand1 * operand2
        elif operator == '/':
            result = operand1 / operand2
        elif operator == '%':
            result = operand1 % operand2
        elif operator == '+':
            result = operand1 + operand2
        elif operator == '-':
            result = operand1 - operand2
        else:
            raise Exception(
                "Unsuppored operator on two numeric values: {0}".format(operator))

        return result
