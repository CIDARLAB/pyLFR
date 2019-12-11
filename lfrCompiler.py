from enum import Enum

from antlr.lfrXListener import lfrXListener
from antlr.lfrXParser import lfrXParser
from compiler.fluid import Fluid
from compiler.language.concatenation import Concatenation
from compiler.language.fluidexpression import FluidExpression
from compiler.language.vector import Vector
from compiler.language.vectorrange import VectorRange
from compiler.lfrerror import ErrorType, LFRError
from compiler.module import Module
from compiler.moduleio import IOType, ModuleIO


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

class LFRCompiler(lfrXListener):

    def __init__(self):

        print("Initialized the lfrcompiler")
        self.modules = []
        self.currentModule: Module
        self.lhs = None
        self.rhs = None
        self.operatormap = dict()
        self.expressionoperatorstack = []
        self.expressionvariablestack = None
        self.technologyOverride = None
        self.compilingErrors = []
        self.success = False
        self.vectors = dict()
        self.expressionresults = None
        self.listermode: ListenerMode = ListenerMode.NONE
        self.lastlistenermode: ListenerMode = ListenerMode.NONE
        self.EXPLICIT_MODULE_DECLARATION = None

        # Temp Store
        self.currentVectorVars = []
        self.currentconcatenations = []
        self.currentexpressionterms = []

        # This might be the new expression stack
        self.stack = []
        self.statestack = []
        self.binaryoperatorsstack = []

    def enterModuledefinition(self, ctx: lfrXParser.ModuledefinitionContext):
        m = Module(ctx.ID().getText())
        self.modules.append(m)
        self.currentModule = m

    def exitModuledefinition(self, ctx: lfrXParser.ModuledefinitionContext):
        self.modules.append(self.currentModule)

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

            v = self.__createVector(name, ModuleIO, startindex, endindex)

            self.vectors[name] = v

            for item in v.get_items():
                self.currentModule.add_io(item)

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

        startindex = 0
        endindex = 0

        for declvar in ctx.declvar():
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
                        name, ModuleIO, startindex, endindex)
                    self.vectors[name] = vec

                    # Add the declared IO as the module's IO
                    for item in vec.get_items():
                        self.currentModule.add_io(item)

                    # Go through each of the ios and modify the type
                    for io in vec.get_items():
                        io.type = mode

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

            v = self.__createVector(name, Fluid, startindex, endindex)

            for item in v.get_items():
                self.currentModule.add_fluid(item)

            # Now that the declaration is done, we are going to save it
            self.vectors[name] = v

    def exitFluiddeclstat(self, ctx: lfrXParser.FluiddeclstatContext):
        self.__revertMode()

    def exitVectorvar(self, ctx: lfrXParser.VectorvarContext):
        name = ctx.ID().getText()
        startindex = 0
        endindex = 0

        if ctx.vector() is not None:
            startindex = int(ctx.vector().start.text)
            endindex = int(ctx.vector().end.text)

        if name in self.vectors:
            v = self.vectors[name]
        else:
            raise Exception(
                "Trying to parse vector var and we couldn't find the vector in itself")

        vrange = VectorRange(v, startindex, endindex)

        self.stack.append(vrange)

    def exitConcatenation(self, ctx: lfrXParser.ConcatenationContext):
        if ctx.vector() is not None:
            self.compilingErrors.append(
                LFRError(ErrorType.COMPILER_NOT_IMPLEMENTED,
                         "Selecting range from compiler has not been implemented, ignoring range for concatenation on line {0} column{1}".format(
                             ctx.start.getLine(), ctx.start.getCharPositionInLine())))

        ranges = []
        for vv in ctx.vectorvar():
            name = vv.ID().getText()
            vec = self.vectors[name]
            startindex = int(vv.vector().start.text)
            endindex = int(vv.vector().end.text)
            vrange = vec.get_range(startindex, endindex)
            ranges.append(vrange)

        c = Concatenation(ranges)

        self.stack.append(c)

    def enterNumber(self, ctx: lfrXParser.NumberContext):
        if self.listermode is ListenerMode.VARIABLE_DECLARATION_MODE:
            return

        n = None
        # check to see what kind of a number it is to parse it correctly

        # TODO: Figure out to do the parsing for the binary, hex and octal numbers. Need to cleave the header for this

        if ctx.Decimal_number() is not None:
            n = int(ctx.Decimal_number().getText())

        elif ctx.Octal_number() is not None:
            n = int(ctx.Octal_number().getText(), 8)

        elif ctx.Hex_number() is not None:
            n = int(ctx.Hex_number().getText(), 16)

        elif ctx.Binary_number() is not None:
            n = int(ctx.Binary_number().getText(), 2)

        else:
            n = float(ctx.Real_number().getText())

        self.stack.append(n)

    def enterNumvarstat(self, ctx: lfrXParser.NumvarstatContext):
        self.__updateMode(ListenerMode.VARIABLE_DECLARATION_MODE)

        names = ctx.ID()
        numbers = ctx.number()

        for name, number in zip(names, numbers):
            varname = name.getText()
            n = None
            if number.Decimal_number() is not None:
                n = int(number.Decimal_number().getText())

            elif number.Octal_number() is not None:
                n = int(number.Octal_number().getText(), 8)

            elif number.Hex_number() is not None:
                n = int(number.Hex_number().getText(), 16)

            elif number.Binary_number() is not None:
                n = int(number.Binary_number().getText(), 2)

            else:
                n = float(number.Real_number().getText())

            self.vectors[varname] = n

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
                
                #Attaching the output fluid/operator node vectors
                self.vectors[output.vector.id] = output
                self.stack.append(output)

            elif ctx.number() is not None:
                # TODO: Figure out how one needs to process the number with a unary operator
                raise Exception("Implement method to evaluate number with unary operator")
    
    def enterBinary_operator(self, ctx: lfrXParser.Binary_operatorContext):
        op = ctx.getText()
        self.binaryoperatorsstack.append(op)

    def enterExpression(self, ctx: lfrXParser.ExpressionContext):
        self.__updateMode(ListenerMode.EXPRESS_PARSING_MODE)
        self.binaryoperatorstack = []
    
    def exitExpression(self, ctx: lfrXParser.ExpressionContext):
        self.__revertMode()

        #TODO: Pull all the operators and expression terms
        stackslice = self.stack[-(len(self.binaryoperatorsstack)+1):]
        del self.stack[-(len(self.binaryoperatorsstack)+1):]

        fluidexpression = FluidExpression(self.currentModule)
        #TODO: Figure out how to pass the FIG after this
        result = fluidexpression.process_expression(stackslice, self.binaryoperatorsstack)
        self.stack.append(result)

    def enterBracketexpression(self, ctx: lfrXParser.BracketexpressionContext):
        self.__updateMode(ListenerMode.EXPRESS_PARSING_MODE)
        self.binaryoperatorstack = []

    def exitBracketexpression(self, ctx: lfrXParser.BracketexpressionContext):
        self.__revertMode()

        # Perform the unary operation if present
        if ctx.unary_operator() is not None:

            operator = ctx.unary_operator().getText()
            term = self.stack.pop()
            fluidexpession = FluidExpression(self.currentModule)
            result = fluidexpession.process_unary_operation(term, operator)
            # TODO: Write how one should be doing the unary operation
            print("Performing the unary operation on the single term")
            self.stack.append(result)

    
    def exitAssignstat(self, ctx: lfrXParser.AssignstatContext):
        rhs = self.stack.pop()
        lhs = self.stack.pop()
        
        # TODO: Finish the entire vector implementatinon (?)
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


    # def exitTechnologymappingdirective(self, ctx: lfrXParser.TechnologymappingdirectiveContext):
    #     # print("Operator", ctx.operator.getText())
    #     technologystring = ""
    #     for ID in ctx.ID():
    #         technologystring += ID.getText()
    #     # print(technologystring)
    #     self.operatormap[ctx.operator.getText()] = technologystring
    #
    #

    def exitSkeleton(self, ctx: lfrXParser.SkeletonContext):
        if len(self.compilingErrors) > 0:
            print("There were errors in the compilation process:")
            for error in self.compilingErrors:
                print(error)
        else:
            self.success = True
        print(self.currentModule)

    def __validatevariable(self, variable):
        if variable in self.currentModule.intermediates:
            return True
        else:
            ret = self.currentModule.get_io(variable)
            if ret is not None:
                return True

        return False

    def __clearoperatormap(self):
        self.operatormap.clear()

    def __createVector(self, name: str, objecttype, startindex: int, endindex: int) -> Vector:
        v = Vector(name, objecttype, startindex, endindex)
        self.vectors[name] = v
        return v

    def __performUnaryOperation(self, operator: str, operand: VectorRange):      
        print("Performing unary operation - Operator: {0} \n Operand: {1}".format(operator, operand))
        # TODO: Return the vector range result of unary operator
        return operand

    def __updateMode(self, newmode):
        self.statestack.append(self.listermode)
        self.listermode = newmode

    def __revertMode(self):
        self.listermode = self.statestack.pop()
