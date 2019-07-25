from antlr.lfrXListener import lfrXListener
from antlr.lfrXParser import lfrXParser
from compiler.module import Module
from compiler.moduleio import ModuleIO, IOType
from compiler.lfrerror import ErrorType, LFRError


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

    def enterModuledefinition(self, ctx:lfrXParser.ModuledefinitionContext):
        m = Module(ctx.ID().getText())
        self.modules.append(m)
        self.currentModule = m

    def exitIoblock(self, ctx:lfrXParser.IoblockContext):
        for ID in ctx.ID():
            io = ModuleIO(ID.getText())
            self.currentModule.addio(io)

    def exitExplicitIOBlock(self, ctx:lfrXParser.ExplicitIOBlockContext):
        #  First check the type of the explicit io block
        decltype = ctx.start.text
        mode = None
        if decltype == 'finput':
            mode = IOType.FLOW_INPUT
        elif decltype == 'foutput':
            mode = IOType.FLOW_OUTPUT
        elif decltype == 'control':
            mode = IOType.CONTROL

        for ID in ctx.ID():
            name = ID.getText()
            io = self.currentModule.getio(name)
            if io is None:
                self.compilingErrors.append(LFRError(ErrorType.MODULE_IO_NOT_FOUND, " i/o:{0} not declared in module".format(name)))
            else:
                io.type = mode

    def exitTechnologymappingdirective(self, ctx:lfrXParser.TechnologymappingdirectiveContext):
        # print("Operator", ctx.operator.getText())
        technologystring = ""
        for ID in ctx.ID():
            technologystring += ID.getText()
        # print(technologystring)
        self.operatormap[ctx.operator.getText()] = technologystring

    def exitAssignstat(self, ctx:lfrXParser.AssignstatContext):
        # Right now, only the single assignment is available so just work with that
        # Check to see if LHS is temp variable or an io
        ret = self.currentModule.getfluid(ctx.lhs().getText())
        if ret is None:
            raise Exception("Could not assign because we could not map lhs to any known variable")
        elif ret is not None:
            print("LHS: ", ret)

            rvariable = self.expressionvariablestack.pop()
            while len(self.expressionoperatorstack) > 0:
                lvariable = self.expressionvariablestack.pop()
                op = self.expressionoperatorstack.pop()
                # Check if the operator is overridden
                if op in self.operatormap.keys():
                    # Now the Fluid Interaction is overriden
                    overridden_interaction = self.operatormap[op]
                    f1 = self.currentModule.getfluid(rvariable)
                    f2 = self.currentModule.getfluid(lvariable)
                    interaction = self.currentModule.addfluidcustominteraction(f2, f1, overridden_interaction)
                    # Create an edge from the interaction to the output
                    self.currentModule.addinteractionoutput(ret, interaction)
                else:
                    # TODO Figure out how we want to parse the expression, do we want to it here or internally
                    pass
                rvariable = lvariable



        # Final thing to do: clear the operator override
        self.__clearoperatormap()

    def exitExpression(self, ctx:lfrXParser.ExpressionContext):
        # print(ctx.variables())
        # print(ctx.binary_operator())
        # For now just store all the variables and operators and add them from reverse
        variables = [v.getText() for v in ctx.variables()]
        operators = [v.getText() for v in ctx.binary_operator()]

        # TODO - Split the expression where there are overridden operators
        self.expressionoperatorstack = operators
        self.expressionvariablestack = variables

    def exitSkeleton(self, ctx:lfrXParser.SkeletonContext):
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

