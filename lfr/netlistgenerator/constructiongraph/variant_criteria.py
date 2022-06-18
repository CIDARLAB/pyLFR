from enum import Enum
from typing import Tuple
from lfr.netlistgenerator.constructiongraph.constructiongraph import ConstructionGraph
from lfr.netlistgenerator.constructiongraph.constructionnode import ConstructionNode


class VariantType(Enum):
    SUBSTITUTION = 1
    ADDITION = 2


def check_variant_criteria(
    variant: ConstructionGraph, node: ConstructionNode
) -> VariantType:
    # Check if the node's fig mapping overlaps with the fig cover of the
    # existing construction nodes according to the axioms definined. If it does
    # return ADDITION, else return SUBSTITUTION.
    for cn in variant._construction_nodes:
        if cn.fig_cover == node.fig_cover:
            return VariantType.SUBSTITUTION
        elif node.has_border_overlap(cn):
            return VariantType.ADDITION
    else:
        return VariantType.ADDITION
