from typing import Dict
from networkx.algorithms.isomorphism import DiGraphMatcher
from networkx.classes import digraph
from lfr.graphmatch.nodefilter import NodeFilter
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph


class FIGMappingMatcher(DiGraphMatcher):
    """Implementation of VF2 algorithm for matching undirected graphs.

    Suitable for Graph and MultiGraph instances.
    """

    def __init__(
        self,
        G1: FluidInteractionGraph,
        G2: digraph.DiGraph,
        semantic_information: Dict[str, NodeFilter],
    ):
        self._fig = G1
        self._semantic_information = semantic_information
        super(FIGMappingMatcher, self).__init__(G1, G2)

    def semantic_feasibility(self, G1_node, G2_node):
        """Returns True if adding (G1_node, G2_node) is symantically feasible.

        The semantic feasibility function should return True if it is
        acceptable to add the candidate pair (G1_node, G2_node) to the current
        partial isomorphism mapping.   The logic should focus on semantic
        information contained in the edge data or a formalized node class.

        By acceptable, we mean that the subsequent mapping can still become a
        complete isomorphism mapping.  Thus, if adding the candidate pair
        definitely makes it so that the subsequent mapping cannot become a
        complete isomorphism mapping, then this function must return False.

        The default semantic feasibility function always returns True. The
        effect is that semantics are not considered in the matching of G1
        and G2.

        The semantic checks might differ based on the what type of test is
        being performed.  A keyword description of the test is stored in
        self.test.  Here is a quick description of the currently implemented
        tests::

          test='graph'
            Indicates that the graph matcher is looking for a graph-graph
            isomorphism.

          test='subgraph'
            Indicates that the graph matcher is looking for a subgraph-graph
            isomorphism such that a subgraph of G1 is isomorphic to G2.

        Any subclass which redefines semantic_feasibility() must maintain
        the above form to keep the match() method functional. Implementations
        should consider multigraphs.
        """

        # Get the semantic information from here and then use it to figure out if
        # its right type of node or not

        # Figure out if G1 or G2 is the pattern graph
        g1_fig_info = self._fig.get_fignode(G1_node)
        g2_semantic_info = self._semantic_information[G2_node]

        if g2_semantic_info.is_valid_node_type(g1_fig_info.match_string):
            return True
        else:
            return False
