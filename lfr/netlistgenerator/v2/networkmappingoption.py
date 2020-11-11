from lfr.netlistgenerator.primitive import NetworkPrimitive
from lfr.netlistgenerator.v2.mappingoption import MappingOption
from enum import Enum


class NetworkMappingOptionType(Enum):
    PASS_THROUGH = 0
    COMPONENT_REPLACEMENT = 1
    CHANNEL_NETWORK = 2


class NetworkMappingOption(MappingOption):

    def __init__(self, network_primitive: NetworkPrimitive, mapping_type: NetworkMappingOptionType, subgraph_view) -> None:
        super().__init__(primitive=network_primitive, subgraph_view=subgraph_view)
        self._mapping_type: NetworkMappingOptionType = mapping_type

        # Automatically Assign the Network/ProceduralPrimitive if its a channel network

    @property
    def mapping_type(self) -> NetworkMappingOptionType:
        return self._mapping_type
