from enum import Enum
from typing import overload
from lfr.netlistgenerator.v2.gen_strategies.genstrategy import GenStrategy

from networkx.classes.function import subgraph
from lfr.netlistgenerator.explicitmapping import ExplicitMapping
from lfr.netlistgenerator.namegenerator import NameGenerator
from pymint.mintdevice import MINTDevice
from lfr.fig.interaction import InteractionType
from lfr.netlistgenerator.mappinglibrary import MappingLibrary, Primitive, PrimitiveType
from networkx import nx


class MappingOption():

    def __init__(self, primitive: Primitive, subgraph_view=None) -> None:

        self._primitive: Primitive = primitive

        self.fig_subgraph: nx.DiGraph = subgraph_view

        # Figure out what computation needs to get done with this
        self._interaction_type: InteractionType = None

    @property
    def interaction_type(self):
        return self._interaction_type

    @property
    def primitive(self):
        return self._primitive

    def add_subgraph(self, subgraph_view) -> None:
        self.fig_subgraph = subgraph_view

    def generate_netlist(self, name_generator: NameGenerator) -> MINTDevice:
        # Generate a netlist for this mapping option that takes into account
        # the type of primitive this is, whether it has a default netlist or not.
        ret = None
        if self._primitive.type is PrimitiveType.COMPONENT:
            ret = MINTDevice("doesn't really matter what the name is")
        elif self._primitive.type is PrimitiveType.NETLIST:
            ret = self._primitive.get_default_netlist()

            # Rename the netlist
            name_generator.rename_netlist(ret)
        else:
            raise Exception("So Primitive Associated with this !")

        return ret

    @staticmethod
    def from_explicit_mapping(explicit_mapping: ExplicitMapping, mapping_library: MappingLibrary):
        primitive = mapping_library.get_primitive(explicit_mapping.technology)
        # TODO - Figure out how to get the subgraph from the explicit mapping
        sub_graph = explicit_mapping.get_subgraph()
        ret = MappingOption(primitive, sub_graph)
        return ret


class ExplicitMappingOption(MappingOption):

    def __init__(self, mapping: ExplicitMapping) -> None:
        # TODO - Generate this from the Explicit Mapping
        pass


class NetworkMappingOptionType(Enum):
    PASS_THROUGH = 0
    COMPONENT_REPLACEMENT = 1
    CHANNEL_NETWORK = 2


# TODO - this would be the class we want to use for network / connection type mappin
class NetworkMappingOption(MappingOption):

    def __init__(self, gen_strategy: GenStrategy, mapping_type: NetworkMappingOptionType, subgraph_view) -> None:
        super().__init__()
        self._mapping_strategy: NetworkMappingOptionType = mapping_type
        self._gen_strategy: GenStrategy = gen_strategy
        self.fig_subgraph = subgraph_view

    def generate_netlist(self, name_generator: NameGenerator) -> MINTDevice:
        # TODO - Go through netlist and then figure out what needs to get done
        # based on the strategy we need to do different things

        if self._gen_strategy is NetworkMappingOptionType.PASS_THROUGH:
            # TODO - In this case it needs to be an empty netlist
            pass
        elif self._gen_strategy is NetworkMappingOptionType.COMPONENT_REPLACEMENT:
            # TODO - In this case it needs to be an component with the corresponding
            # input and output options loaded into the placeholder primitive
            pass
        elif self._gen_strategy is NetworkMappingOptionType.CHANNEL_NETWORK:
            # TODO - This would be a netlist but I'll need to enable terminals/nodes
            # where the network will connect through. Most likely we will not need to 
            # use this
            pass

    

