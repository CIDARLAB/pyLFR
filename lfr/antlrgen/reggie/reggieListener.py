# Generated from ./reggie.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .reggieParser import reggieParser
else:
    from reggieParser import reggieParser

# This class defines a complete listener for a parse tree produced by reggieParser.
class reggieListener(ParseTreeListener):

    # Enter a parse tree produced by reggieParser#graph.
    def enterGraph(self, ctx:reggieParser.GraphContext):
        pass

    # Exit a parse tree produced by reggieParser#graph.
    def exitGraph(self, ctx:reggieParser.GraphContext):
        pass


    # Enter a parse tree produced by reggieParser#graphstatement.
    def enterGraphstatement(self, ctx:reggieParser.GraphstatementContext):
        pass

    # Exit a parse tree produced by reggieParser#graphstatement.
    def exitGraphstatement(self, ctx:reggieParser.GraphstatementContext):
        pass


    # Enter a parse tree produced by reggieParser#statementmodifier.
    def enterStatementmodifier(self, ctx:reggieParser.StatementmodifierContext):
        pass

    # Exit a parse tree produced by reggieParser#statementmodifier.
    def exitStatementmodifier(self, ctx:reggieParser.StatementmodifierContext):
        pass


    # Enter a parse tree produced by reggieParser#basestatement.
    def enterBasestatement(self, ctx:reggieParser.BasestatementContext):
        pass

    # Exit a parse tree produced by reggieParser#basestatement.
    def exitBasestatement(self, ctx:reggieParser.BasestatementContext):
        pass


    # Enter a parse tree produced by reggieParser#subgraph.
    def enterSubgraph(self, ctx:reggieParser.SubgraphContext):
        pass

    # Exit a parse tree produced by reggieParser#subgraph.
    def exitSubgraph(self, ctx:reggieParser.SubgraphContext):
        pass


    # Enter a parse tree produced by reggieParser#vertex.
    def enterVertex(self, ctx:reggieParser.VertexContext):
        pass

    # Exit a parse tree produced by reggieParser#vertex.
    def exitVertex(self, ctx:reggieParser.VertexContext):
        pass


    # Enter a parse tree produced by reggieParser#coloringfilter.
    def enterColoringfilter(self, ctx:reggieParser.ColoringfilterContext):
        pass

    # Exit a parse tree produced by reggieParser#coloringfilter.
    def exitColoringfilter(self, ctx:reggieParser.ColoringfilterContext):
        pass


    # Enter a parse tree produced by reggieParser#structuralvertexpattern.
    def enterStructuralvertexpattern(self, ctx:reggieParser.StructuralvertexpatternContext):
        pass

    # Exit a parse tree produced by reggieParser#structuralvertexpattern.
    def exitStructuralvertexpattern(self, ctx:reggieParser.StructuralvertexpatternContext):
        pass


    # Enter a parse tree produced by reggieParser#intmodifier.
    def enterIntmodifier(self, ctx:reggieParser.IntmodifierContext):
        pass

    # Exit a parse tree produced by reggieParser#intmodifier.
    def exitIntmodifier(self, ctx:reggieParser.IntmodifierContext):
        pass


    # Enter a parse tree produced by reggieParser#starmodifier.
    def enterStarmodifier(self, ctx:reggieParser.StarmodifierContext):
        pass

    # Exit a parse tree produced by reggieParser#starmodifier.
    def exitStarmodifier(self, ctx:reggieParser.StarmodifierContext):
        pass


    # Enter a parse tree produced by reggieParser#plusmodifier.
    def enterPlusmodifier(self, ctx:reggieParser.PlusmodifierContext):
        pass

    # Exit a parse tree produced by reggieParser#plusmodifier.
    def exitPlusmodifier(self, ctx:reggieParser.PlusmodifierContext):
        pass


    # Enter a parse tree produced by reggieParser#structuralid.
    def enterStructuralid(self, ctx:reggieParser.StructuralidContext):
        pass

    # Exit a parse tree produced by reggieParser#structuralid.
    def exitStructuralid(self, ctx:reggieParser.StructuralidContext):
        pass


    # Enter a parse tree produced by reggieParser#labelfilter.
    def enterLabelfilter(self, ctx:reggieParser.LabelfilterContext):
        pass

    # Exit a parse tree produced by reggieParser#labelfilter.
    def exitLabelfilter(self, ctx:reggieParser.LabelfilterContext):
        pass


    # Enter a parse tree produced by reggieParser#label.
    def enterLabel(self, ctx:reggieParser.LabelContext):
        pass

    # Exit a parse tree produced by reggieParser#label.
    def exitLabel(self, ctx:reggieParser.LabelContext):
        pass


    # Enter a parse tree produced by reggieParser#vertex2vertex.
    def enterVertex2vertex(self, ctx:reggieParser.Vertex2vertexContext):
        pass

    # Exit a parse tree produced by reggieParser#vertex2vertex.
    def exitVertex2vertex(self, ctx:reggieParser.Vertex2vertexContext):
        pass


    # Enter a parse tree produced by reggieParser#edge.
    def enterEdge(self, ctx:reggieParser.EdgeContext):
        pass

    # Exit a parse tree produced by reggieParser#edge.
    def exitEdge(self, ctx:reggieParser.EdgeContext):
        pass



del reggieParser