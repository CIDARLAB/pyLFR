# Generated from /Volumes/krishna/CIDAR/pylfr/lfrX.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .lfrXParser import lfrXParser
else:
    from lfrXParser import lfrXParser

# This class defines a complete generic visitor for a parse tree produced by lfrXParser.

class lfrXVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by lfrXParser#skeleton.
    def visitSkeleton(self, ctx:lfrXParser.SkeletonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#module.
    def visitModule(self, ctx:lfrXParser.ModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#moduledefinition.
    def visitModuledefinition(self, ctx:lfrXParser.ModuledefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#body.
    def visitBody(self, ctx:lfrXParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#ioblock.
    def visitIoblock(self, ctx:lfrXParser.IoblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#vectorvar.
    def visitVectorvar(self, ctx:lfrXParser.VectorvarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#explicitIOBlock.
    def visitExplicitIOBlock(self, ctx:lfrXParser.ExplicitIOBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#declvar.
    def visitDeclvar(self, ctx:lfrXParser.DeclvarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#distributionBlock.
    def visitDistributionBlock(self, ctx:lfrXParser.DistributionBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#distributionBody.
    def visitDistributionBody(self, ctx:lfrXParser.DistributionBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#distributeBodyStat.
    def visitDistributeBodyStat(self, ctx:lfrXParser.DistributeBodyStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#ifElseBlock.
    def visitIfElseBlock(self, ctx:lfrXParser.IfElseBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#ifBlock.
    def visitIfBlock(self, ctx:lfrXParser.IfBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#elseBlock.
    def visitElseBlock(self, ctx:lfrXParser.ElseBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#elseIfBlock.
    def visitElseIfBlock(self, ctx:lfrXParser.ElseIfBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#distributeCondition.
    def visitDistributeCondition(self, ctx:lfrXParser.DistributeConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#statementBlock.
    def visitStatementBlock(self, ctx:lfrXParser.StatementBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#caseBlock.
    def visitCaseBlock(self, ctx:lfrXParser.CaseBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#caseBlockHeader.
    def visitCaseBlockHeader(self, ctx:lfrXParser.CaseBlockHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#casestat.
    def visitCasestat(self, ctx:lfrXParser.CasestatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#defaultCaseStat.
    def visitDefaultCaseStat(self, ctx:lfrXParser.DefaultCaseStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#distvalue.
    def visitDistvalue(self, ctx:lfrXParser.DistvalueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#distributionassignstat.
    def visitDistributionassignstat(self, ctx:lfrXParser.DistributionassignstatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#sensitivitylist.
    def visitSensitivitylist(self, ctx:lfrXParser.SensitivitylistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#signal.
    def visitSignal(self, ctx:lfrXParser.SignalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#statements.
    def visitStatements(self, ctx:lfrXParser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#statement.
    def visitStatement(self, ctx:lfrXParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#moduleinstantiationstat.
    def visitModuleinstantiationstat(self, ctx:lfrXParser.ModuleinstantiationstatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#instanceioblock.
    def visitInstanceioblock(self, ctx:lfrXParser.InstanceioblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#orderedioblock.
    def visitOrderedioblock(self, ctx:lfrXParser.OrderedioblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#unorderedioblock.
    def visitUnorderedioblock(self, ctx:lfrXParser.UnorderedioblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#explicitinstanceiomapping.
    def visitExplicitinstanceiomapping(self, ctx:lfrXParser.ExplicitinstanceiomappingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#instancename.
    def visitInstancename(self, ctx:lfrXParser.InstancenameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#moduletype.
    def visitModuletype(self, ctx:lfrXParser.ModuletypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#tempvariablesstat.
    def visitTempvariablesstat(self, ctx:lfrXParser.TempvariablesstatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#signalvarstat.
    def visitSignalvarstat(self, ctx:lfrXParser.SignalvarstatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#fluiddeclstat.
    def visitFluiddeclstat(self, ctx:lfrXParser.FluiddeclstatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#storagestat.
    def visitStoragestat(self, ctx:lfrXParser.StoragestatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#pumpvarstat.
    def visitPumpvarstat(self, ctx:lfrXParser.PumpvarstatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#numvarstat.
    def visitNumvarstat(self, ctx:lfrXParser.NumvarstatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#assignstat.
    def visitAssignstat(self, ctx:lfrXParser.AssignstatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#literalassignstat.
    def visitLiteralassignstat(self, ctx:lfrXParser.LiteralassignstatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#bracketexpression.
    def visitBracketexpression(self, ctx:lfrXParser.BracketexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#expression.
    def visitExpression(self, ctx:lfrXParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#expressionterm.
    def visitExpressionterm(self, ctx:lfrXParser.ExpressiontermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#logiccondition_operand.
    def visitLogiccondition_operand(self, ctx:lfrXParser.Logiccondition_operandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#logiccondition.
    def visitLogiccondition(self, ctx:lfrXParser.LogicconditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#logic_value.
    def visitLogic_value(self, ctx:lfrXParser.Logic_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#vector.
    def visitVector(self, ctx:lfrXParser.VectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#variables.
    def visitVariables(self, ctx:lfrXParser.VariablesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#concatenation.
    def visitConcatenation(self, ctx:lfrXParser.ConcatenationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#lhs.
    def visitLhs(self, ctx:lfrXParser.LhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#ioassignstat.
    def visitIoassignstat(self, ctx:lfrXParser.IoassignstatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#technologydirectives.
    def visitTechnologydirectives(self, ctx:lfrXParser.TechnologydirectivesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#directive.
    def visitDirective(self, ctx:lfrXParser.DirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#technologymappingdirective.
    def visitTechnologymappingdirective(self, ctx:lfrXParser.TechnologymappingdirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#materialmappingdirective.
    def visitMaterialmappingdirective(self, ctx:lfrXParser.MaterialmappingdirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#mappingoperator.
    def visitMappingoperator(self, ctx:lfrXParser.MappingoperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#performancedirective.
    def visitPerformancedirective(self, ctx:lfrXParser.PerformancedirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#constraint.
    def visitConstraint(self, ctx:lfrXParser.ConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#unit.
    def visitUnit(self, ctx:lfrXParser.UnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#unary_operator.
    def visitUnary_operator(self, ctx:lfrXParser.Unary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#binary_operator.
    def visitBinary_operator(self, ctx:lfrXParser.Binary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#unary_module_path_operator.
    def visitUnary_module_path_operator(self, ctx:lfrXParser.Unary_module_path_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#binary_module_path_operator.
    def visitBinary_module_path_operator(self, ctx:lfrXParser.Binary_module_path_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lfrXParser#number.
    def visitNumber(self, ctx:lfrXParser.NumberContext):
        return self.visitChildren(ctx)



del lfrXParser