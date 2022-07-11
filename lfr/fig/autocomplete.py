from lfr.fig.fluidinteractiongraph import FluidInteractionGraph


def connect_orphan_IO(fig: FluidInteractionGraph) -> None:

    # Step 1 - Go through all the flow nodes and check to see if any of them have zero outputs.
    # Step 2 - If they do then generate a new IO node and connect it to the flow node.

    raise NotImplementedError()
