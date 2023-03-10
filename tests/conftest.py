from pathlib import Path
import networkx
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph

TEST_OUTPATH = Path(__file__).parent.joinpath("out").absolute()
TEST_DATA_FOLDER = Path(__file__).parent.joinpath("data")
LIBRARY_PATH = Path(__file__).parent.parent.joinpath("library").absolute()

def to_agraph(fig):
    fig_copy = fig.copy(as_view=False)
    ret = networkx.nx_agraph.to_agraph(fig_copy)
    return ret