from lfr.fig.fignode import IOType, Flow, IONode, Storage, Signal, Pump
from lfr.compiler.language.concatenation import Concatenation
from lfr.compiler.language.fluidexpression import FluidExpression
from lfr.compiler.language.utils import is_number
from lfr.compiler.language.vector import Vector
from lfr.compiler.language.vectorrange import VectorRange
from lfr.compiler.lfrerror import ErrorType, LFRError
from lfr.compiler.module import Module
from lfr.compiler.moduleio import ModuleIO
from enum import Enum
from typing import List, Optional
from lfr.compiler.distribute.BitVector import BitVector
import re
from lfr.antlrgen.lfrXListener import lfrXListener
from lfr.antlrgen.lfrXParser import lfrXParser


class ListenerMode(Enum):
    NONE = 0
    IO_DECLARATION_MODE = 1
    VARIABLE_DECLARATION_MODE = 2
    LHS_PARSING_MODE = 3
    EXPRESS_PARSING_MODE = 4
    FLUID_ASSIGN_STAT_MODE = 5
    DISTRIBUTE_ASSIGN_STAT_MODE = 6


class VariableTypes(Enum):
    FLUID = 0
    NUMBER = 1
    STORAGE = 3
    SIGNAL = 4


class LFRBaseListener(lfrXListener):

    def __init__(self):

        print("Initialized the lfrcompiler")
        self.modules = []
        self.currentModule: Optional[Module] = None
        self.lhs = None
        self.rhs = None
        self.operatormap = dict()
        self.expressionoperatorstack = []
        self.expressionvariablestack = None
        self.technologyOverride = None
        self.compilingErrors: List[LFRError] = []
        self.success = False
        self.vectors = dict()
        self.expressionresults = None
        self.listermode: ListenerMode = ListenerMode.NONE
        self.lastlistenermode: ListenerMode = ListenerMode.NONE
        self.EXPLICIT_MODULE_DECLARATION = None

        self.typeMap = dict()

        # This might be the new expression stack
        self.stack = []
        self.statestack = []
        self.binaryoperatorsstack = [[]]

    def enterModule(self, ctx: lfrXParser.ModuleContext):
        if self.currentModule is not None:
            self.modules.append(self.currentModule)
            self.currentModule = None

    def enterModuledefinition(self, ctx: lfrXParser.ModuledefinitionContext):
        m = Module(ctx.ID().getText())
        # self.modules.append(m)
        self.currentModule = m

    # def exitModuledefinition(self, ctx: lfrXParser.ModuledefinitionContext):
    #     self.modules.append(self.currentModule)

    def exitModule(self, ctx: lfrXParser.ModuleContext):
        self.operatormap = dict()
        self.expressionoperatorstack = []
        self.expressionvariablestack = None
        self.technologyOverride = None
        self.success = False
        self.vectors = dict()
        self.expressionresults = None
        self.listermode: ListenerMode = ListenerMode.NONE
        self.lastlistenermode: ListenerMode = ListenerMode.NONE

        self.stack = []
        self.statestack = []
        self.binaryoperatorsstack = [[]]


    def enterIoblock(self, ctx: lfrXParser.IoblockContext):
        # If io block has an explicit declaration set the flag
        if ctx.explicitIOBlock() is not None:
            self.EXPLICIT_MODULE_DECLARATION = True

        for vv in ctx.vectorvar():
            name = vv.ID().getText()
            startindex = 0
            endindex = 0

            if vv.vector() is not None:
                startindex = int(vv.vector().start.text)
                endindex = int(vv.vector().end.text)

            v = self.__createVector(name, IONode, startindex, endindex)

            self.vectors[name] = v
            self.typeMap[name] = VariableTypes.FLUID

            m = ModuleIO(name)
            m.vector_ref = v.get_range()
            self.currentModule.add_io(m)

    def exitExplicitIOBlock(self, ctx: lfrXParser.ExplicitIOBlockContext):
        #  First check the type of the explicit io block
        decltype = ctx.start.text
        mode = None
        if decltype == 'finput':
            mode = IOType.FLOW_INPUT
        elif decltype == 'foutput':
            mode = IOType.FLOW_OUTPUT
        elif decltype == 'control':
            mode = IOType.CONTROL

        for declvar in ctx.declvar():
            startindex = 0
            endindex = 0

            if declvar.vector() is not None:
                # Parse all the info regarding the vector
                # print("Parsing Vector:", declvar.vector().getText())
                startindex = int(declvar.vector().start.text)
                endindex = int(declvar.vector().end.text)

            name = declvar.ID().getText()
            # Check if the vector has been created
            if name in self.vectors:
                # Retrieve the vector to change the subitems
                vec = self.vectors[name]

                # First check if the size is the same or not, if not give an error
                if len(vec) is not (abs(startindex - endindex) + 1):
                    self.compilingErrors.append(
                        LFRError(ErrorType.VECTOR_SIZE_MISMATCH,
                                 "explicit i/o:{0} definition not same size as module definition".format(name)))

                # Go through each of the ios and modify the type
                for io in vec.get_items():
                    io.type = mode
            else:
                if self.EXPLICIT_MODULE_DECLARATION is True:
                    # This is the scenario where all the declaration is done explicitly
                    vec = self.__createVector(
                        name, IONode, startindex, endindex)
                    self.vectors[name] = vec
                    self.typeMap[name] = VariableTypes.FLUID

                    # Go through each of the ios and modify the type
                    for io in vec.get_items():
                        io.type = mode

                    # Create and add a ModuleIO reference
                    m = ModuleIO(name, mode)
                    m.vector_ref = vec.get_range()
                    self.currentModule.add_io(m)

                else:
                    self.compilingErrors.append(
                        LFRError(ErrorType.MODULE_IO_NOT_FOUND, "i/o:{0} not declared in module".format(name)))

    def enterFluiddeclstat(self, ctx: lfrXParser.FluiddeclstatContext):
        self.__updateMode(ListenerMode.VARIABLE_DECLARATION_MODE)
        for declvar in ctx.declvar():
            name = declvar.ID().getText()
            startindex = 0
            endindex = 0

            if declvar.vector() is not None:
                startindex = int(declvar.vector().start.text)
                endindex = int(declvar.vector().end.text)

            v = self.__createVector(name, Flow, startindex, endindex)

            for item in v.get_items():
                self.currentModule.add_fluid(item)

            # Now that the declaration is done, we are going to save it
            self.vectors[name] = v
            self.typeMap[name] = VariableTypes.FLUID

    def exitFluiddeclstat(self, ctx: lfrXParser.FluiddeclstatContext):
        self.__revertMode()

    def enterStoragestat(self, ctx: lfrXParser.StoragestatContext):
        self.__updateMode(ListenerMode.VARIABLE_DECLARATION_MODE)
        for declvar in ctx.declvar():
            name = declvar.ID().getText()
            startindex = 0
            endindex = 0

            if declvar.vector() is not None:
                startindex = int(declvar.vector().start.text)
                endindex = int(declvar.vector().end.text)

            v = self.__createVector(name, Storage, startindex, endindex)

            for item in v.get_items():
                self.currentModule.add_fluid(item)

            # Now that the declaration is done, we are going to save it
            self.vectors[name] = v
            self.typeMap[name] = VariableTypes.STORAGE

    def exitStoragestat(self, ctx: lfrXParser.StoragestatContext):
        self.__revertMode()

    def enterPumpvarstat(self, ctx: lfrXParser.PumpvarstatContext):
        self.__updateMode(ListenerMode.VARIABLE_DECLARATION_MODE)
        for declvar in ctx.declvar():
            name = declvar.ID().getText()
            startindex = 0
            endindex = 0

            if declvar.vector() is not None:
                startindex = int(declvar.vector().start.text)
                endindex = int(declvar.vector().end.text)

            v = self.__createVector(name, Pump, startindex, endindex)

            for item in v.get_items():
                self.currentModule.add_fluid(item)

            # Now that the declaration is done, we are going to save it
            self.vectors[name] = v
            self.typeMap[name] = VariableTypes.STORAGE

    def exitPumpvarstat(self, ctx: lfrXParser.PumpvarstatContext):
        self.__revertMode()

    def enterSignalvarstat(self, ctx: lfrXParser.SignalvarstatContext):
        self.__updateMode(ListenerMode.VARIABLE_DECLARATION_MODE)
        for declvar in ctx.declvar():
            name = declvar.ID().getText()
            startindex = 0
            endindex = 0

            if declvar.vector() is not None:
                startindex = int(declvar.vector().start.text)
                endindex = int(declvar.vector().end.text)

            v = self.__createVector(name, Signal, startindex, endindex)

            for item in v.get_items():
                self.currentModule.add_fluid(item)

            # Now that the declaration is done, we are going to save it
            self.vectors[name] = v
            self.typeMap[name] = VariableTypes.SIGNAL

    def exitSignalvarstat(self, ctx: lfrXParser.SignalvarstatContext):
        self.__revertMode()

    def exitVectorvar(self, ctx: lfrXParser.VectorvarContext):
        name = ctx.ID().getText()
        startindex = 0
        endindex = 0

        if name in self.vectors:
            v = self.vectors[name]
            startindex = v.startindex
            endindex = v.endindex
        else:
            raise Exception("Trying to parse vector variable {} and we couldn't find the vector in itself: Line - {}".format(name, ctx.start.line))

        # Check to see if the slice is present utilize the index
        if ctx.vector() is not None:
            startindex = int(ctx.vector().start.text)
            if ctx.vector().end is not None:
                endindex = int(ctx.vector().end.text)
            else:
                endindex = startindex

        vrange = VectorRange(v, startindex, endindex)

        self.stack.append(vrange)

    def exitConcatenation(self, ctx: lfrXParser.ConcatenationContext):
        if ctx.vectorvar() is not None:
            item_in_concatenation = len(ctx.vectorvar())
        else:
            # TODO - Check if this is right ?
            item_in_concatenation = 1
        # slice the items out of the stack
        stackslice = self.stack[-(item_in_concatenation):]
        del self.stack[-(item_in_concatenation):]

        c = Concatenation(stackslice)

        # TODO: Here the selector will determine the start and endindex for the vector
        # range
        startindex = 0
        endindex = len(c) - 1
        if ctx.vector() is not None:
            self.compilingErrors.append(
                LFRError(ErrorType.COMPILER_NOT_IMPLEMENTED,
                         "Selecting range from compiler has not been implemented, ignoring range for concatenation on line {0} column{1}".format(
                             ctx.start.getLine(), ctx.start.getCharPositionInLine())))

        v = c.get_range(startindex, endindex)
        self.stack.append(v)

    def enterNumber(self, ctx: lfrXParser.NumberContext):
        # if self.listermode is ListenerMode.VARIABLE_DECLARATION_MODE:
        #     return

        n = None
        # check to see what kind of a number it is to parse it correctly

        # TODO: Figure out to do the parsing for the binary, hex and octal
        # numbers. Need to cleave the header for this
        if ctx.Decimal_number() is not None:
            n = int(ctx.Decimal_number().getText())

        elif ctx.Octal_number() is not None:
            n = int(ctx.Octal_number().getText(), 8)

        elif ctx.Hex_number() is not None:
            n = int(ctx.Hex_number().getText(), 16)

        elif ctx.Binary_number() is not None:
            n = self.__parseBinaryNumber(ctx.Binary_number().getText())

        else:
            n = float(ctx.Real_number().getText())

        self.stack.append(n)

    def enterNumvarstat(self, ctx: lfrXParser.NumvarstatContext):
        self.__updateMode(ListenerMode.VARIABLE_DECLARATION_MODE)

        # Don't really need to do much here - If you need to go back in history
        # for this method implmentation - refer commit - bf24c90

    def exitNumvarstat(self, ctx):
        self.__revertMode()

    def exitExpressionterm(self, ctx: lfrXParser.ExpressiontermContext):
        # Check if this has a unary operator (we have to process this)
        if ctx.unary_operator() is not None:
            # Since we have the unary operator, we need to pop the last item
            # and perform the operation

            operator = ctx.unary_operator().getText()

            if ctx.variables().vectorvar() is not None:
                lastitem = self.stack.pop()
                output = self.__performUnaryOperation(operator, lastitem)

                # Attaching the output fluid/operator node vectors
                self.vectors[output.vector.id] = output
                self.typeMap[output.vector.id] = VariableTypes.FLUID

                self.stack.append(output)

            elif ctx.number() is not None:
                # TODO: Figure out how one needs to process the number with a unary operator
                raise Exception("Implement method to evaluate number with unary operator")

    def enterBinary_operator(self, ctx: lfrXParser.Binary_operatorContext):
        op = ctx.getText()
        self.binaryoperatorsstack[-1].append(op)

    def enterExpression(self, ctx: lfrXParser.ExpressionContext):
        self.__updateMode(ListenerMode.EXPRESS_PARSING_MODE)
        self.binaryoperatorsstack.append([])

    def exitExpression(self, ctx: lfrXParser.ExpressionContext):
        self.__revertMode()

        # TODO: Pull all the operators and expression terms
        stackslice = self.stack[-(len(self.binaryoperatorsstack[-1])+1):]
        del self.stack[-(len(self.binaryoperatorsstack[-1])+1):]

        fluidexpression = FluidExpression(self.currentModule)
        # TODO: Figure out how to pass the FIG after this
        result = fluidexpression.process_expression(stackslice, self.binaryoperatorsstack[-1])
        self.stack.append(result)

        self.binaryoperatorsstack.pop()

    def enterBracketexpression(self, ctx: lfrXParser.BracketexpressionContext):
        self.__updateMode(ListenerMode.EXPRESS_PARSING_MODE)

    def exitBracketexpression(self, ctx: lfrXParser.BracketexpressionContext):
        self.__revertMode()
        # Perform the unary operation if present
        if ctx.unary_operator() is not None:

            operator = ctx.unary_operator().getText()
            term = self.stack.pop()
            fluidexpession = FluidExpression(self.currentModule)
            result = fluidexpession.process_unary_operation(term, operator)
            self.stack.append(result)

    def exitAssignstat(self, ctx: lfrXParser.AssignstatContext):
        rhs = self.stack.pop()
        lhs = self.stack.pop()

        # Check if both the LHS and RHS are numbers
        if is_number(lhs) is True or is_number(rhs) is True:
            if is_number(lhs) is not True and is_number(rhs) is True:
                raise Exception("Cannot assign Fluid to Number Variable")
            elif is_number(lhs) is True and is_number(rhs) is not True:
                raise Exception("Cannot assign Number to Fluid Variable")
            else:
                self.vectors[lhs] = rhs

        # Perform the vector assignments
        if len(lhs) == len(rhs):
            print("LHS, RHS sizes are equal")
            # Make 1-1 connections
            for source, target in zip(rhs, lhs):
                print(source, target)
                sourceid = source.id
                targetid = target.id

                self.currentModule.add_fluid_connection(sourceid, targetid)

        elif len(lhs) != len(rhs):
            print("LHS not equal to RHS")
            for source in rhs:
                sourceid = source.id

                for target in lhs:
                    targetid = target.id
                    self.currentModule.add_fluid_connection(sourceid, targetid)

    def exitLiteralassignstat(self, ctx: lfrXParser.LiteralassignstatContext):
        rhs = self.stack.pop()
        lhs = ctx.ID().getText()
        # TODO: Check all error conditions and if the right kinds of variables are being assigned here
        # self.vectors[lhs] = rhs

        if self.listermode is ListenerMode.VARIABLE_DECLARATION_MODE:
            v = self.__createLiteralVector(lhs, rhs)
            self.vectors[lhs] = v
            self.typeMap[lhs] = VariableTypes.NUMBER
        else:
            # TODO - How to assign the data to this
            pass

    def exitSkeleton(self, ctx: lfrXParser.SkeletonContext):
        if len(self.compilingErrors) > 0:
            print("There were errors in the compilation process:")
            for error in self.compilingErrors:
                print(error)
        else:
            self.success = True
        print(self.currentModule)

    def __createVector(self, name: str, objecttype, startindex: int, endindex: int) -> Vector:
        v = Vector(name, objecttype, startindex, endindex)
        self.vectors[name] = v
        self.typeMap[name] = VariableTypes.FLUID

        return v

    def __createLiteralVector(self, name: str, values: List) -> Vector:

        objectype = None

        if isinstance(values, list):
            objectype = type(values[0])
        else:
            objectype = type(values)
            values = [values]

        v = Vector.create_from_list_things(name, values)

        self.vectors[name] = v
        self.typeMap[name] = VariableTypes.NUMBER

        return v

    def __performUnaryOperation(self, operator: str, operand: VectorRange) -> FluidExpression:
        print("Performing unary operation - Operator: {0} \n Operand: {1}".format(operator, operand))
        # TODO: Return the vector range result of unary operator
        fluidexpression = FluidExpression(self.currentModule)
        result = fluidexpression.process_unary_operation(operand, operator)

        return result

    def __updateMode(self, newmode):
        self.statestack.append(self.listermode)
        self.listermode = newmode

    def __revertMode(self):
        self.listermode = self.statestack.pop()

    def print_variables(self):
        for key in self.vectors.keys():
            print('{0} - {1}'.format(key, self.vectors[key]))

    def print_stack(self):
        print('---Top of Stack---')
        for item in self.stack:
            print(item)

        print('---Bottom of Stack---')

    def __parseBinaryNumber(self, text: str) -> BitVector:
        pattern = r"(\d+)'b(\d+)"
        matches = re.search(pattern, text)
        # size = int(matches.group(1))
        bit_pattern = matches.group(2)
        n = BitVector(bitstring=bit_pattern)
        return n
