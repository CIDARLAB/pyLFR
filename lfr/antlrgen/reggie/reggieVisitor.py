# Generated from ./reggie.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .reggieParser import reggieParser
else:
    from reggieParser import reggieParser

# This class defines a complete generic visitor for a parse tree produced by reggieParser.

class reggieVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by reggieParser#graph.
    def visitGraph(self, ctx:reggieParser.GraphContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#graphstatement.
    def visitGraphstatement(self, ctx:reggieParser.GraphstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#statementmodifier.
    def visitStatementmodifier(self, ctx:reggieParser.StatementmodifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#basestatement.
    def visitBasestatement(self, ctx:reggieParser.BasestatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#subgraph.
    def visitSubgraph(self, ctx:reggieParser.SubgraphContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#vertex.
    def visitVertex(self, ctx:reggieParser.VertexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#coloringfilter.
    def visitColoringfilter(self, ctx:reggieParser.ColoringfilterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#structuralvertexpattern.
    def visitStructuralvertexpattern(self, ctx:reggieParser.StructuralvertexpatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#intmodifier.
    def visitIntmodifier(self, ctx:reggieParser.IntmodifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#starmodifier.
    def visitStarmodifier(self, ctx:reggieParser.StarmodifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#plusmodifier.
    def visitPlusmodifier(self, ctx:reggieParser.PlusmodifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#structuralid.
    def visitStructuralid(self, ctx:reggieParser.StructuralidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#labelfilter.
    def visitLabelfilter(self, ctx:reggieParser.LabelfilterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#label.
    def visitLabel(self, ctx:reggieParser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#vertex2vertex.
    def visitVertex2vertex(self, ctx:reggieParser.Vertex2vertexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by reggieParser#edge.
    def visitEdge(self, ctx:reggieParser.EdgeContext):
        return self.visitChildren(ctx)



del reggieParser