from typing import List

from lfr.netlistgenerator.v2.mappingoption import MappingOption
from lfr.netlistgenerator.v2.networkmappingoption import NetworkMappingOption
from lfr.postprocessor.constraints import Constraint


class ExplicitMappingOption:
    # def __init__(self, mapping: ) -> None:
    #     # TODO - Generate this from the Explicit Mapping
    #     pass

    @staticmethod
    def generate_fluidic_operation_mapping_option(
        technology: str, constraints: List[Constraint]
    ) -> MappingOption:
        ret = MappingOption()
        return ret

    @staticmethod
    def generate_storage_mapping_option(
        technology: str, constraints: List[Constraint]
    ) -> MappingOption:
        ret = MappingOption()
        return ret

    @staticmethod
    def generate_network_mapping_option(
        technology: str, constraints: List[Constraint]
    ) -> NetworkMappingOption:
        ret = NetworkMappingOption()
        return ret
