from typing import Dict, FrozenSet, List, Optional, Set, Tuple

from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator import LibraryPrimitivesEntry
from lfr.netlistgenerator.constructiongraph.constructiongraph import ConstructionGraph
from lfr.netlistgenerator.constructiongraph.constructionnode import ConstructionNode
from lfr.netlistgenerator.constructiongraph.variant_criteria import (
    VariantType,
    check_variant_criteria,
)
from lfr.netlistgenerator.constructiongraph.varianttree import VariantTree
from lfr.netlistgenerator.gen_strategies.genstrategy import GenStrategy
from lfr.netlistgenerator.mappinglibrary import MappingLibrary, MatchPatternEntry
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.postprocessor.mapping import NodeMappingTemplate


def generate_match_variants(
    matches: List[LibraryPrimitivesEntry],
    fig: FluidInteractionGraph,
    library: MappingLibrary,
    active_strategy: GenStrategy,
    explicit_mapping_covers: Optional[List[Set[str]]] = None,
) -> List[ConstructionGraph]:
    """
    Generate all possible match variants of a given graph.

    Args:
        fig: The graph to generate match variants for.

    Returns:
       A tree view of the matches
    """

    def find_index_of_match_entry(
        fig_cover_set: Set[str],
        matches: List[LibraryPrimitivesEntry],
    ) -> int:
        """Find the index of a match entry in a list of matches."""
        for index, entry in enumerate(matches):
            if fig_cover_set == set(list(entry[2].keys())):
                return index
        raise Exception("Could not find the index of the match entry")

    def move_entry_to_front(
        entries_list: List[LibraryPrimitivesEntry],
        index: int,
    ) -> None:
        """Move an entry to the front of a list."""
        entries_list.insert(0, entries_list.pop(index))

    def generate_match_subgraph(match: LibraryPrimitivesEntry):
        """Generate a fig subgraph view of a match."""
        nodes_list = list(match[2].keys())
        return fig.subgraph(nodes_list)

    def create_variant(
        node: ConstructionNode,
        variant: ConstructionGraph,
        fig_node_cover: FrozenSet[str],
    ):
        print(f"Generating new variant for substitution {node.ID}")
        new_variant = variant.generate_variant(f"variant_{variant_index}")

        # TODO - Substitute the node with the new node
        new_variant.remove_node_for_exact_fig_cover(fig_node_cover)
        new_variant.add_construction_node(node)
        # Creates a new variant branch and add it to the variant tree
        print(f"Adding node {node.ID} to variant {variant.ID}")

        variant_tree.add_variant(variant, new_variant)

    variant_tree: VariantTree[ConstructionGraph] = VariantTree[ConstructionGraph]()
    cn_name_generator = NameGenerator()
    # sort the matches based on the size of the dict keys
    matches.sort(key=lambda x: len(x[1]))

    # Step 1 - First group all the matches with the same node mapping
    # Step 2 - Sort earch group by the size of the dict keys (i.e. the number of nodes)
    # Step 3 - Start with the smallest and find all the non overlapping matches sets.
    # This, allows us to reduce the number of variants generated.
    # there.
    # Step 4 - We create a Variant Tree for each of the non overlapping match sets.
    # We can use a greedy set packing problem to solve this.
    # Step 5 - We create a Variant Tree for each of the non overlapping match sets.

    # TODO - take all the matches and start creating construction graphs and variants
    # Loop trhough each of the matches
    variant_index = 0

    # Create the first variant here
    seed_variant = ConstructionGraph(f"variant_{variant_index}", fig)
    variant_tree.add_variant(seed_variant, None)

    # Find the set of matches that are non overlapping using a greedy cover algorithm
    subsets = []
    universe = set()

    for match in matches:
        nodes_set = set(list(match[2].keys()))
        if nodes_set not in subsets:
            subsets.append(nodes_set)
        universe.union(nodes_set)

    # Group all the matches based on the node mappings

    # Order all the matches based on:
    # 1. Explicit Matches
    # 2. Set Cover Matches
    # 3. Smallest Cover Matches
    cover = generate_set_cover(universe, subsets)
    print("Moving Max Set Cover to the front:", cover)
    for cover_set_entry in cover:
        move_entry_to_front(
            matches, find_index_of_match_entry(cover_set_entry, matches)
        )

    if explicit_mapping_covers is not None:
        # Moving all the explicit matches to the front
        print("Moving Explicit Matches to the front:", explicit_mapping_covers)
        for explicit_mapping_cover in explicit_mapping_covers:
            move_entry_to_front(
                matches, find_index_of_match_entry(explicit_mapping_cover, matches)
            )

    # Loop through every match
    for match in matches:
        print("Checking Match:", match)
        # For each match, create a construction node
        primitive_uid = match[0]
        primitive_technology = match[1]
        node = ConstructionNode(
            cn_name_generator.generate_name(f"cn_{primitive_technology}"),
            library.get_primitive(primitive_uid),
            generate_match_subgraph(match),
        )

        fig_nodes_set = frozenset(list(match[2].keys()))

        # Check if Variant Tree has a saved divergence for this node, we do a new
        # divergence branch and create a new variant.
        divergence_node_payload = variant_tree.get_divergence(fig_nodes_set)
        if divergence_node_payload is not None:
            # Create the new variant and continue with the next match
            variant_index += 1
            create_variant(node, divergence_node_payload, fig_nodes_set)
            continue

        # Check if the construction node satisfies the variant criteria for each of the
        # variants
        for variant in variant_tree.walk_tree():
            variant_type = check_variant_criteria(variant, node)

            # VARIANT_TYPE.SUBSTITUTION
            if variant_type is VariantType.ADDITION:
                # Just add the node to the variant
                print(f"Adding node {node.ID} to variant {variant.ID}")
                variant.add_construction_node(node)
            elif variant_type is VariantType.SUBSTITUTION:
                # Create a new variant and add the node to it
                variant_index += 1
                create_variant(node, variant, fig_nodes_set)
                # Save Divergence in the Variant Tree for the corresponding delta
                variant_tree.save_divergence(fig_nodes_set, variant)
            else:
                raise ValueError(f"Unknown variant type {variant_type}")

    # Next steps:
    # 1. Find ways to map the flow elements to the construction nodes
    # 2. Do the pruning of the variant tree utilizing the active strategy
    # 3. Eliminate all the undercovered variants

    # Print out all the nodes in each of the variants
    ret = variant_tree.walk_tree()
    for variant in ret:
        print(f"Variant {variant.ID}:")
        for node in variant.nodes:
            print(node)
    return ret


def generate_set_cover(universe: Set[str], subsets: List[Set[str]]) -> List[Set[str]]:
    """Find a family of subsets that covers the universal set

    Code replicated from:
    http://www.martinbroadhurst.com/greedy-set-cover-in-python.html
    """
    elements = set(e for s in subsets for e in s)
    # Check the subsets cover the universe
    # if elements != universe:
    #     return None
    covered = set()
    cover = []
    # Greedily add the subsets with the most uncovered points
    while covered != elements:
        subset = max(subsets, key=lambda s: len(s - covered))
        cover.append(subset)
        covered |= subset

    return cover


# def add_construction_node(
#     self, construction_node: ConstructionNode, variant_type: VariantType
# ) -> None:

#     # TODO - Just add the construction node into the graph
#     if variant_type == VariantType.SUBSTITUTION:
#         # Remove the existing construction node that has an intersecting fig cover
#         # with the new construction node
#         for cn in self._construction_nodes:
#             if cn.fig_cover.intersection(construction_node.fig_cover):
#                 self.remove_construction_node(cn)
#                 break
#         else:
#             raise ValueError(
#                 "No construction node found with an intersecting fig cover"
#             )
#         self._construction_nodes.append(construction_node)
#         self.add_node(construction_node.ID)
#     elif variant_type == VariantType.ADDITION:
#         self._construction_nodes.append(construction_node)
#         self.add_node(construction_node.ID)
#     else:
#         raise ValueError("Invalid variant type")
