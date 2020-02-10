

from enum import Enum
from netlistgenerator.explicitmapping import ExplicitMapping
from lfrCompiler import LFRCompiler
from compiler.module import Module
from antlr.lfrXParser import lfrXParser


class TechnologyMappingMODE(Enum):
    NO_MAPPING = 0
    OPERATOR_MAPPING = 1
    ASSIGN_MAPPING = 2


class MappingCompiler(LFRCompiler):

    def __init__(self):
        super().__init__()
        print("Initialing the Technology Mapper")
        self.mappingMode = TechnologyMappingMODE.NO_MAPPING
        self.currentMappingTechnology = ''
        self.mappingOperator = ''
        self.mappingDictionary = dict()


    def enterTechnologymappingdirective(self, ctx):
        #Clearing the mapping operator
        self.mappingOperator = ''
        self.currentMappingDictionary = dict()
        #Checking if the mapping is an operator or assign mapping
        if ctx.mappingoperator().getText() is '':
            self.mappingMode = TechnologyMappingMODE.ASSIGN_MAPPING
            print('Need to map for an assign statement and not an operator')
        else:
            self.mappingMode = TechnologyMappingMODE.OPERATOR_MAPPING
            operator = ctx.mappingoperator().getText()
            technology = ctx.ID().getText()
            self.mappingOperator = operator
            self.currentMappingTechnology = technology
            self.mappingDictionary[operator] = technology

    def exitAssignstat(self, ctx: lfrXParser.AssignstatContext):        


        if self.mappingMode is TechnologyMappingMODE.OPERATOR_MAPPING:
            # We need to do call super implementation first so that we can pull the correct vectorranges
            super().exitAssignstat(ctx)

            # Save the route from the start (rhs) to the end (lhs)
            if len(ctx.expression().children) == 1:
                lhs = []
                rhs = []
                lhsvectors = []
                rhsvectors = []
                expression_term = ctx.expression().children[0]
                if expression_term.unary_operator():
                    #Check if the operator is correct
                    if expression_term.unary_operator().getText() != self.mappingOperator:
                        return
                    #Search for the items
                    for variable in ctx.lhs().variables().children:
                        lhs.append(variable.ID().getText())
                    
                    for vector in lhs:
                        lhsvectors.append(self.vectors[vector])

                    for variable in expression_term.variables().children:
                        rhs.append(variable.ID().getText())
                    
                    for vector in rhs:
                        rhsvectors.append(self.vectors[vector])

                    startlist = [fluid.id for item in rhsvectors for  fluid in item.vec]
                    endlist = [fluid.id for item in lhsvectors for  fluid in item.vec]

                    if len(startlist) == len(endlist):
                        for start, end in zip(startlist, endlist):
                            mapping = ExplicitMapping()
                            mapping.startlist = start
                            mapping.endlist = end
                            mapping.technology = self.currentMappingTechnology
                            self.currentModule.add_mapping(mapping)
                    else:
                        if len(startlist) != 1 and len(endlist) != 1:
                            for start in startlist:
                                for end in endlist:
                                    mapping = ExplicitMapping()
                                    mapping.startlist = start
                                    mapping.endlist = end
                                    mapping.technology = self.currentMappingTechnology
                                    self.currentModule.add_mapping(mapping)
                        else:
                            mapping = ExplicitMapping()
                            mapping.startlist = startlist
                            mapping.endlist = endlist
                            mapping.technology = self.currentMappingTechnology
                            self.currentModule.add_mapping(mapping)

                else:
                    print("Cannot map in scerio where there are no unary operators found or the operator is not a unary operator")
            else:
                #TODO: We need to over ride the expression evaulation to effectively map all the things 
                # going on there, however its not going to be easy because we might not know what the exact 
                # graph might turn out to be. Perhaps the start end schema and traversals might do the job
                print("Cannot map in scenario where there are more than 1 expression terms that need to get" +
                    "mapped, we currently have no strategy for biary operators")

        elif self.mappingMode is TechnologyMappingMODE.ASSIGN_MAPPING:
            #TODO: When its assign mapping, we can ignore all the interactions and just make the connections between both the vector ranges
            lhs = self.stack[-2]
            rhs = self.stack[-1]

            startlist = [item.id for item in rhs]
            endlist = [item.id for item in lhs]

            mapping = ExplicitMapping()
            mapping.startlist = startlist
            mapping.endlist = endlist
            mapping.technology = self.currentMappingTechnology
            self.currentModule.add_mapping(mapping)

            # We need to do call super implementation last so that we can access the stack before its cleared
            super().exitAssignstat(ctx)

        else:
            #TODO: This just means that nothign happens
            pass

        
        

        
