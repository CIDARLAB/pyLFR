from lfr.fig.fluidinteractiongraph import FluidInteractionGraph

PASS1_DICT = dict()
PASS2_DICT = dict()


def map_technologies(graph: FluidInteractionGraph):
    print("Running the direct technology mapper:")
    print(graph.G.edges())
    # Iterate through all the custom mapping interactions
    # Step 1-
    #   Clump all the graph nodes by common outputs, this way we try to combine the interactions
    #   based on the common outputs. so if its a dictionary <output, [interactions]> then we just
    #   need to merge the arrays of interactions in the first pass. Need to keep in mind that we
    #   need keep reconstructing the dictionary after every merge because we might have merged
    #   interactions in the algorithm
    #
    # print(graph.fluids)
    # print(graph.fluidinteractions)
    # Create all the indexes in STEP 1
    breakflag = True
    while breakflag:
        repeat = False
        PASS1_DICT = dict()
        for interaction in list(graph.fluidinteractions):
            print(interaction)
            neighbors = list(graph.G.neighbors(interaction))
            for output in neighbors:
                if output in PASS1_DICT.keys():
                    print("Added entry :", interaction)
                    PASS1_DICT[output].append(interaction)
                else:
                    print("Created entry for pass1 :", output)
                    print("Added entry :", interaction)
                    PASS1_DICT[output] = [interaction]

        for interaction in PASS1_DICT.keys():
            nodes = PASS1_DICT[interaction]

            if len(nodes) > 1:
                graph.merge_interactions(nodes)
                repeat = True
                break

        if repeat:
            continue

        breakflag = False

    print("Finished the STEP 1 of operator merging")
    print("PASS1 Reduced Graph:", graph.G.edges())
    # print(graph.fluidinteractions)

    # Step 2-
    #   The second pass we construct dictionary <interactions, set(inputs)> and then we
    #   basically merge all the interactions with duplicating inputs
    #
    print("Starting the STEP 2 of operator merging")

    for interaction in list(graph.fluidinteractions):
        # print("Interaction:", interaction)

        # This comprehension generates the list inputs
        neighbors = [i[0] for i in list(graph.G.in_edges(interaction))]
        # print("neighbours:", neighbors)
        for neighbor in neighbors:
            if interaction in PASS2_DICT.keys():
                # Since interaction already exists in the dictionary, we just add it to it and the
                # set datastructure will ensure that its unique
                PASS2_DICT[interaction].add(neighbor)
            else:
                # Since interaction does not exist in dictionary, we create a new entry to it
                foo = set()
                foo.add(neighbor)
                PASS2_DICT[interaction] = foo

    print("PASS 2 DICTIONARY: ", PASS2_DICT)

    #   Now that the dictionary has been built, the fluidic interactions with the
    #   same sets of inputs need to merged. To do that that, create anoter dictionary
    #   that will have the sets as keys

    MERGE_DICT = dict()

    for interaction in PASS2_DICT.keys():
        inputset = frozenset(PASS2_DICT[interaction])
        if inputset in MERGE_DICT.keys():
            MERGE_DICT[inputset].append(interaction)
        else:
            foo = []
            foo.append(interaction)
            MERGE_DICT[inputset] = foo

    # print("MERGE_DICT: ", MERGE_DICT)

    # Now to merge each of these list of fluid interactions

    for key in MERGE_DICT.keys():
        interactions = MERGE_DICT[key]
        if len(interactions) > 1:
            graph.merge_interactions(interactions)

    print("PASS2 Reduced Graph:", graph.G.edges())
