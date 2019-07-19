from compiler.fluidinteractiongraph import FluidInteractionGraph

PASS1_DICT = dict()
PASS2_DICT = dict()


def mapTechnologies(graph: FluidInteractionGraph):
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

        for key in PASS1_DICT.keys():
            nodes = PASS1_DICT[key]

            if len(nodes) > 1:
                graph.mergeinteractions(nodes)
                repeat = True
                break
        
        if repeat:
            continue

        breakflag = False

    print("Finished the STEP 1 of operator merging")
    print("PASS1 Reduced Graph:", graph.G.edges())
    #print(graph.fluidinteractions)

    # TODO Step 2-
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