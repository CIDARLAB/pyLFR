from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from lfr.netlistgenerator.v2.mappingoption import MappingOption
from typing import List
from lfr.netlistgenerator.explicitmapping import ExplicitMapping


class ConstructionNode():

    def __init__(self, node_id: str) -> None:
        self._id = node_id
        self._mapping_options: List[MappingOption] = []
        self._explict_mapping_flag = False

    @property
    def id(self) -> str:
        return self._id

    @property
    def mapping_options(self) -> List[MappingOption]:
        return self._mapping_options

    @mapping_options.setter
    def mapping_options(self, options: List[MappingOption]):
        self._mapping_options = options

    def use_explicit_mapping(self, mapping: ExplicitMapping, mapping_library: MappingLibrary) -> None:
        # Set the flag for explicit mapping
        self._explict_mapping_flag = True
        # Delete all the existing mapping options
        self._mapping_options.clear()
        # Now that we have overwritten all the netlist options here
        # we basically cherry pick the one little bit that we want to attach here
        self._mapping_options.append(MappingOption.from_explicit_mapping(mapping, mapping_library))

    def add_mapping_option(self, mapping_option: MappingOption) -> None:
        if self._explict_mapping_flag is True:
            # TODO - Add user flag for overwriting explicit mappings
            print("Warning, cannot update construction graph node {}, since explicit mapping is present")
        else:
            self._mapping_options.append(mapping_option)
