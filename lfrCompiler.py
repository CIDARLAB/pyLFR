from enum import Enum

from antlr.lfrXListener import lfrXListener
from antlr.lfrXParser import lfrXParser
from compiler.fluid import Fluid
from compiler.language.concatenation import Concatenation
from compiler.language.vectorrange import VectorRange
from compiler.module import Module
from compiler.moduleio import ModuleIO, IOType
from compiler.lfrerror import ErrorType, LFRError
from compiler.language.vector import Vector


class ListenerMode(Enum):
    IO_DECLARATION_MODE = 0
    VARIABLE_DECLARATION_MODE = 1
    LHS_PARSING_MODE = 2
    EXPRESS_PARSING_MODE = 3


class LFRCompiler(lfrXListener):

    def __init__(self):

        print("Initialized the lfrcompiler")
        self.modules = []
        self.currentModule = None
        self.lhs = None
        self.rhs = None
        self.operatormap = dict()
        self.expressionoperatorstack = []
        self.expressionvariablestack = None
        self.technologyOverride = None
        self.compilingErrors = []
        self.success = False
        self.lhsmode = False
        self.vectors = dict()
        self.expressionresult = None
        self.assignmode = False

    def enterModuledefinition(self, ctx: lfrXParser.ModuledefinitionContext):
        m = Module(ctx.ID().getText())
        self.modules.append(m)
        self.currentModule = m

    def exitModuledefinition(self, ctx: lfrXParser.ModuledefinitionContext):
        self.modules.append(self.currentModule)

    def enterIoblock(self, ctx: lfrXParser.IoblockContext):
        # for ID in ctx.ID():
        #     io = ModuleIO(ID.getText())
        #     self.currentModule.addio(io)
        for vv in ctx.vectorvar():
            name = vv.ID().getText()
            startindex = 0
            endindex = 0

            if vv.vector() is not None:
                startindex = int(vv.vector().start.text)
                endindex = int(vv.vector().end.text)

            v = self.__createVector(name, ModuleIO, startindex, endindex)

            for item in v.get_items():
                self.currentModule.addio(item)

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
                        LFRError(ErrorType.VECTOR_SIZE_MISMATCH, "explicit i/o:{0} definition not same size as module definition".format(name)))

                # Go through each of the ios and modify the type
                for io in vec.get_items():
                    io.type = mode
            else:
                self.compilingErrors.append(
                    LFRError(ErrorType.MODULE_IO_NOT_FOUND, "i/o:{0} not declared in module".format(name)))

    def enterFluiddeclstat(self, ctx: lfrXParser.FluiddeclstatContext):
        for declvar in ctx.declvar():
            name = declvar.ID().getText()
            startindex = 0
            endindex = 0

            if declvar.vector() is not None:
                startindex = int(declvar.vector().start.text)
                endindex = int(declvar.vector().end.text)

            v = self.__createVector(name, Fluid, startindex, endindex)

            for item in v.get_items():
                self.currentModule.addfluid(item)

    def enterLhs(self, ctx: lfrXParser.LhsContext):
        self.lhsmode = True

    def exitLhs(self, ctx: lfrXParser.LhsContext):
        self.lhsmode = False

    # def exitVariables(self, ctx:lfrXParser.VariablesContext):
    #     if self.lhsmode:
    #

    def exitConcatenation(self, ctx: lfrXParser.ConcatenationContext):
        if ctx.vector() is not None:
            self.compilingErrors.append(
                LFRError(ErrorType.COMPILER_NOT_IMPLEMENTED, "selecting range from compiler has not been implemented, ignoring range for concatenation on line {0} column{1}".format(ctx.start.getLine(), ctx.start.getCharPositionInLine())))

        ranges = []
        for vv in ctx.vectorvar():
            name = vv.ID().getText()
            vec = self.vectors[name]
            startindex = int(vv.vector().start.text)
            endindex = int(vv.vector().end.text)
            vrange = vec.get_range(startindex, endindex)
            ranges.append(vrange)

        c = Concatenation(ranges)

        if self.lhsmode:
            self.lhs = c
        else:
            self.expressionvariablestack.append(c)

    def exitVectorvar(self, ctx: lfrXParser.VectorvarContext):
        if self.assignmode is False:
            return

        name = ctx.ID().getText()
        if name not in self.vectors:
            self.compilingErrors.append(
                LFRError(ErrorType.VARIABLE_NOT_RECOGNIZED,
                         "Variable:{0} was not recognized, check to see if this was declared earlier".format(name)))

        vec = self.vectors[name]

        startindex = 0
        endindex = 0

        if ctx.vector() is not None:
            startindex = int(ctx.vector().start.text)
            endindex = int(ctx.vector().end.text)

        vrange = VectorRange(vec, startindex, endindex)

        if self.lhsmode:
            self.lhs = vrange
        else:
            if self.expressionvariablestack is not None:
                self.expressionvariablestack.append(vrange)
            else:
                self.expressionresult = vrange

    def enterAssignstat(self, ctx: lfrXParser.AssignstatContext):
        self.assignmode = True

    def exitAssignstat(self, ctx: lfrXParser.AssignstatContext):
        # TODO: Finish the entire vector implementatinon
        # Check if LHS contains storage, if so figure out what to do
        # perform the vector operations necessary for the what we have here
        # TODO: Evaluate the entire expression an get the final range/concatenation that we want to map
        v = self.expressionresult
        if len(self.lhs) == len(v):
            print("Both sizes are equal")
            # Make 1-1 connections
            for source, target in zip(v, self.lhs):
                print(source, target)
                if isinstance(source, ModuleIO):
                    sourceid = source.name
                else:
                    sourceid = source.id

                if isinstance(target, ModuleIO):
                    targetid = target.name
                else:
                    targetid = target.id

                self.currentModule.addfluidconnection(sourceid, targetid)

        elif len(self.lhs) != len(v):
            print("LHS dim smaller than RHS")
            for source in v:
                if isinstance(source, ModuleIO):
                    sourceid = source.name
                else:
                    sourceid = source.id

                for target in self.lhs:
                    if isinstance(target, ModuleIO):
                        targetid = target.name
                    else:
                        targetid = target.id

                    self.currentModule.addfluidconnection(sourceid, targetid)

        self.assignmode = False

    def enterExpression(self, ctx: lfrXParser.ExpressionContext):
        self.expressionvariablestack = []
        self.expressionoperatorstack = []

    def exitExpression(self, ctx: lfrXParser.ExpressionContext):
        self.expressionvariablestack = None
        self.expressionoperatorstack = None

        # for vector in ctx.vector():
        #     print(vector)
        #
        # for ID in ctx.ID():
        #     name = ID.getText()
        #     io = self.currentModule.getio(name)
        #     if io is None:
        #         self.compilingErrors.append(LFRError(ErrorType.MODULE_IO_NOT_FOUND, " i/o:{0} not declared in module".format(name)))
        #     else:
        #         io.type = mode

    # def exitTechnologymappingdirective(self, ctx: lfrXParser.TechnologymappingdirectiveContext):
    #     # print("Operator", ctx.operator.getText())
    #     technologystring = ""
    #     for ID in ctx.ID():
    #         technologystring += ID.getText()
    #     # print(technologystring)
    #     self.operatormap[ctx.operator.getText()] = technologystring
    #
    # def exitAssignstat(self, ctx: lfrXParser.AssignstatContext):
    #     # Right now, only the single assignment is available so just work with that
    #     # Check to see if LHS is temp variable or an io
    #     ret = self.currentModule.getfluid(ctx.lhs().getText())
    #     if ret is None:
    #         #In case we cant find what the LHS is we basically check if its an i/o
    #         ret = self.currentModule.getio(ctx.lhs().getText())
    #     print("TEST %:",ctx.lhs().getText(), ret)
    #     if ret is None:
    #         raise Exception("Could not assign because we could not map lhs to any known variable")
    #     elif ret is not None:
    #         print("LHS: ", ret)
    #
    #         rvariable = self.expressionvariablestack.pop()
    #         while len(self.expressionoperatorstack) > 0:
    #             lvariable = self.expressionvariablestack.pop()
    #             op = self.expressionoperatorstack.pop()
    #             # Check if the operator is overridden
    #             if op in self.operatormap.keys():
    #                 # Now the Fluid Interaction is overriden
    #                 overridden_interaction = self.operatormap[op]
    #                 f1 = self.currentModule.getfluid(rvariable)
    #                 f2 = self.currentModule.getfluid(lvariable)
    #                 interaction = self.currentModule.addfluidcustominteraction(f2, f1, overridden_interaction)
    #                 # Create an edge from the interaction to the output
    #                 self.currentModule.addinteractionoutput(ret, interaction)
    #             else:
    #                 # TODO Figure out how we want to parse the expression, do we want to it here or internally
    #                 pass
    #             rvariable = lvariable
    #
    #
    #
    #     # Final thing to do: clear the operator override
    #     self.__clearoperatormap()
    #
    # def exitExpression(self, ctx: lfrXParser.ExpressionContext):
    #     # print(ctx.variables())
    #     # print(ctx.binary_operator())
    #     # For now just store all the variables and operators and add them from reverse
    #     variables = [v.getText() for v in ctx.variables()]
    #     operators = [v.getText() for v in ctx.binary_operator()]
    #
    #     # TODO - Split the expression where there are overridden operators
    #     self.expressionoperatorstack = operators
    #     self.expressionvariablestack = variables

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
            ret = self.currentModule.getio(variable)
            if ret is not None:
                return True

        return False

    def __clearoperatormap(self):
        self.operatormap.clear()

    def __createVector(self, name: str, objecttype, startindex: int, endindex: int) -> Vector:
        v = Vector(name, objecttype, startindex, endindex)
        self.vectors[name] = v
        return v
