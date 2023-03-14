from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from pymint.mintlayer import MINTLayerType

from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.constructiongraph.constructionnode import ConstructionNode
from lfr.netlistgenerator.dafdadapter import DAFDAdapter
from lfr.netlistgenerator.gen_strategies.genstrategy import GenStrategy

if TYPE_CHECKING:
    from lfr.netlistgenerator.constructiongraph.constructiongraph import (
        ConstructionGraph,
    )

from typing import List

from parchmint import Target
from pymint.mintdevice import MINTDevice
from pymint.mintnode import MINTNode

from lfr.netlistgenerator.connectingoption import ConnectingOption


class MarsStrategy(GenStrategy):
    pass
