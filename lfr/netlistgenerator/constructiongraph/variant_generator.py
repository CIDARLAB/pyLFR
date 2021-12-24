from lfr.netlistgenerator.gen_strategies.genstrategy import GenStrategy
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.constructiongraph.constructionnode import ConstructionNode
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from lfr.netlistgenerator.constructiongraph.constructiongraph import (
    ConstructionGraph,
)
from typing import Dict, List, Tuple
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph


def generate_match_variants(
    matches: List[Tuple[str, Dict[str, str]]],
    fig: FluidInteractionGraph,
    library: MappingLibrary,
    active_strategy: GenStrategy,
) -> List[ConstructionGraph]:
    """
    Generate all possible match variants of a given graph.

    Args:
        fig: The graph to generate match variants for.

    Returns:
        A list of all possible match variants of the graph.
    """

    def generate_match_subgraph(match):
        """Generate a fig subgraph view of a match."""
        nodes_list = list(match[1].keys())
        return fig.subgraph(nodes_list)

    variants: List[ConstructionGraph] = []
    cn_name_generator = NameGenerator()
    # sort the matches based on the size of the dict keys
    matches.sort(key=lambda x: len(x[1]))

    # TODO - take all the matches and start creating construction graphs and variants
    # Loop trhough each of the matches
    variant_index = 0

    # Create the first variant here
    seed_variant = ConstructionGraph(f"variant_{variant_index}", fig)
    variants.append(seed_variant)
    next_level_variants = []
    for match in matches:
        print(match)
        # For each match, create a construction node
        technology_string = match[0]
        node = ConstructionNode(
            cn_name_generator.generate_name(f"cn_{technology_string}"),
            library.get_primitive(technology_string),
            generate_match_subgraph(match),
        )

        # Check if the construction node satisfies the variant criteria for each of the variants
        for variant in variants:
            is_variant, variant_type = variant.check_variant_criteria(node)
            # IF YES:
            if is_variant:
                print(
                    "Generating new {} Variant for Match {} - Confict for fig node {}"
                    .format(variant_type, match, node.fig_cover)
                )
                # Create a new variant of the construction graph
                variant_index += 1
                new_variant = variant.generate_variant(f"variant_{variant_index}")
                # Add the new variant to the list of variants
                next_level_variants.append(new_variant)
                # Add node to the new the variant graphs(or just the substitution variant)
                new_variant.add_construction_node(node, variant_type)
                # TODO - Validate if this is the best way to do it
            # ELSE:
            else:
                # Add the node to the construction graph / leaves of the variant tree
                variant.add_construction_node(node, variant_type)

        # Update the variants list with the new variants and then clear the new variants array
        variants.extend(next_level_variants)
        next_level_variants.clear()

    # Prune all the variants
    # STEP 7 - Eliminate FLOW passthrough nodes by generating explicit matches for
    # those node subgraphs

    # Delete all the variants that dont fully cover the fig
    for variant in variants:
        # TODO - First Bridge channel networks
        if variant.is_fig_fully_covered() is not True:
            variants.remove(variant)

    # TODO - Prune variants using the plugins (Figre out how to use the generation
    # strategy next)
    # STEP 8 - Prune variants using the plugins
    active_strategy.prune_variants(variants)

    return variants
