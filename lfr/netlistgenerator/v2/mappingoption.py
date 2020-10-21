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
            ret = self._primitive.default_netlist
        else:
            raise Exception("So Primitive Associated with this !")

        name_generator.rename_netlist(ret)

        return ret

    @staticmethod
    def from_explicit_mapping(explicit_mapping: ExplicitMapping, mapping_library: MappingLibrary):
        primitive = mapping_library.get_primitive(explicit_mapping.technology)
        # TODO - Figure out how to get the subgraph from the explicit mapping
        sub_graph = explicit_mapping.get_subgraph()
        ret = MappingOption(primitive, sub_graph)
        return ret
