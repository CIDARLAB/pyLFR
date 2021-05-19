import copy
from typing import List, Optional

from lfr.fig.fignode import FIGNode
from lfr.postprocessor.constraints import Constraint


class NodeMappingInstance:
    def __init__(self) -> None:
        super().__init__()
        self._node: Optional[FIGNode] = None

    @property
    def node(self) -> FIGNode:
        if self._node is not None:
            return self._node
        else:
            raise Exception("No node assigned to the mapping")

    @node.setter
    def node(self, value) -> None:
        self._node = value


class FluidicOperatorMapping(NodeMappingInstance):
    def __init__(self) -> None:
        super().__init__()
        self._operator: str = ""

    @property
    def operator(self) -> str:
        return self._operator

    @operator.setter
    def operator(self, value: str) -> None:
        self._operator = value


class StorageMapping(NodeMappingInstance):
    def __init__(self) -> None:
        super().__init__()

    @property
    def storage_node(self) -> FIGNode:
        if self._node is not None:
            return self._node
        else:
            raise Exception("No Storage FIGNode assigned to mapping")

    @storage_node.setter
    def storage_node(self, value) -> None:
        self._node = value


class PumpMapping(NodeMappingInstance):
    def __init__(self) -> None:
        super().__init__()

    @property
    def pump_node(self) -> FIGNode:
        if self._node is not None:
            return self._node
        else:
            raise Exception("No Storage FIGNode assigned to mapping")

    @pump_node.setter
    def pump_node(self, value) -> None:
        self._node = value


class NetworkMapping(NodeMappingInstance):
    def __init__(self) -> None:
        super().__init__()
        self._input_nodes: List[FIGNode] = []
        self._output_nodes: List[FIGNode] = []

    @property
    def input_nodes(self) -> List[FIGNode]:
        return self._input_nodes

    @input_nodes.setter
    def input_nodes(self, values: List[FIGNode]) -> None:
        self._input_nodes = values

    @property
    def output_nodes(self) -> List[FIGNode]:
        return self._output_nodes

    @output_nodes.setter
    def output_nodes(self, values: List[FIGNode]) -> None:
        self._output_nodes = values


class NodeMappingTemplate:
    def __init__(self) -> None:
        super().__init__()
        self._technology_string: Optional[str] = None
        self._constraints: List[Constraint] = []
        self._mapping_instances: List[NodeMappingInstance] = []

    @property
    def instances(self) -> List[NodeMappingInstance]:
        return self._mapping_instances

    @instances.setter
    def instances(self, vals: List[NodeMappingInstance]) -> None:
        self._mapping_instances = vals

    @property
    def constraints(self) -> List[Constraint]:
        return self._constraints

    @property
    def technology_string(self) -> Optional[str]:
        return self._technology_string

    @technology_string.setter
    def technology_string(self, value):
        self._technology_string = value

    def __deepcopy__(self, memo={}):
        # TODO - Check this again later to ensure that the deep
        # copy is acting correctly. Potentially switch this to a
        # normal copy
        not_there = []
        existing = memo.get(self, not_there)
        if existing is not not_there:
            print("ALREADY COPIED TO", repr(existing))
            return existing
        # instances_copy = copy.deepcopy(
        #     [self._mapping_instances[key] for key in self._fignodes.keys()], memo
        # )
        instances_copy = [
            copy.deepcopy(instance, memo=memo) for instance in self.instances
        ]
        mapping_copy = copy.copy(self)
        # mapping_copy.__class__ = NodeMappingTemplate
        mapping_copy.instances = instances_copy
        return mapping_copy
