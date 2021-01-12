from typing import List, Optional
from pymint.mintdevice import MINTDevice
from pymint.mintparams import MINTParams
from enum import Enum

from pymint.mintlayer import MINTLayer
from lfr.netlistgenerator.v2.gen_strategies.genstrategy import GenStrategy
from lfr.netlistgenerator.v2.connectingoption import ConnectingOption
from lfr import parameters
from lfr.netlistgenerator.namegenerator import NameGenerator
from pymint.mintcomponent import MINTComponent


class PrimitiveType(Enum):
    COMPONENT = 0
    NETLIST = 1
    PROCEDURAL = 2


class Primitive:
    def __init__(
        self,
        mint: str = "",
        component_type: PrimitiveType = PrimitiveType.COMPONENT,
        match_string: str = "",
        is_storage: bool = False,
        has_storage_control: bool = False,
        inputs: List[ConnectingOption] = [],
        outputs: List[ConnectingOption] = [],
        loadings: Optional[List[ConnectingOption]] = [],
        carriers: Optional[List[ConnectingOption]] = [],
        default_netlist: Optional[str] = None,
        functional_input_params: List[str] = [],
        output_params: List[str] = [],
        user_defined_params: MINTParams = MINTParams({}),
    ) -> None:

        self._component_type: PrimitiveType = component_type
        self._match_string: str = match_string
        if mint == "":
            raise Exception(
                "Cannot instantiate an Primitive type object if mint sting is not present"
            )
        self._mint: str = mint
        self._is_storage: bool = is_storage
        self._has_storage_control: bool = has_storage_control
        self._inputs: List[ConnectingOption] = inputs
        self._outputs: List[ConnectingOption] = outputs
        self._loadings: Optional[List[ConnectingOption]] = loadings
        self._carriers: Optional[List[ConnectingOption]] = carriers
        self._default_netlist: Optional[str] = default_netlist

        self._functional_input_params = functional_input_params
        self._output_params = output_params

        self._user_defined_params: MINTParams = user_defined_params

    @property
    def type(self) -> PrimitiveType:
        return self._component_type

    @property
    def mint(self) -> str:
        return self._mint

    @property
    def inputs(self) -> List[ConnectingOption]:
        return self._inputs

    @property
    def outputs(self) -> List[ConnectingOption]:
        return self._outputs

    @property
    def loadings(self) -> List[ConnectingOption]:
        return self._loadings

    @property
    def carriers(self) -> List[ConnectingOption]:
        return self._carriers

    @property
    def default_netlist_location(self):
        return self._default_netlist

    @property
    def inverse_design_query_params(self):
        return self._functional_input_params

    @property
    def output_params(self):
        return self._output_params

    def get_default_component(
        self, name_gen: NameGenerator, layer: MINTLayer
    ) -> MINTComponent:
        if self.type is not PrimitiveType.COMPONENT:
            raise Exception("Cannot execute this method for this kind of a primitive")
        name = name_gen.generate_name(self.mint)
        mc = MINTComponent(name, self.mint, dict(), [layer])
        return mc

    def get_default_netlist(self, cn_id: str, name_gen: NameGenerator) -> MINTDevice:
        if self.type is not PrimitiveType.NETLIST:
            raise Exception("Cannot execute this method for this kind of a  primitive")

        default_mint_file = parameters.LIB_DIR.joinpath(self._default_netlist).resolve()

        device = MINTDevice.from_mint_file(str(default_mint_file))

        if device is None:
            raise Exception(
                "Unable to parse MINT file: {} for construction node {}".format(
                    str(default_mint_file), cn_id
                )
            )
        name_gen.rename_netlist(cn_id, device)
        # Return the default netlist
        return device


class NetworkPrimitive(Primitive):
    def __init__(self, fig_subgraph_view, gen_strategy: GenStrategy) -> None:
        super().__init__(component_type=PrimitiveType.PROCEDURAL)

        self._gen_strategy = gen_strategy
        # Write methods that will utilize the subgraph view to generate the
        # netlist
        self._fig_subgraph_view = fig_subgraph_view
        self._netlist: MINTDevice = None

    def generate_netlist(self) -> None:
        self._netlist = self._gen_strategy.generate_flow_network(
            self._fig_subgraph_view
        )
        self._inputs = self._gen_strategy.generate_input_connectingoptions(
            self._fig_subgraph_view
        )
        self._outputs = self._gen_strategy.generate_output_connectingoptions(
            self._fig_subgraph_view
        )
        self._carriers = self._gen_strategy.generate_carrier_connectingoptions(
            self._fig_subgraph_view
        )
        self._loadings = self._gen_strategy.generate_loading_connectingoptions(
            self._fig_subgraph_view
        )

    def get_default_netlist(self, cn_id: str, name_gen: NameGenerator) -> MINTDevice:
        # Utilise the subgraph view to decide how you want to generate a netlist
        # Load all the inputs and outputs based on that information
        name_gen.rename_netlist(cn_id, self._netlist)
        return self._netlist
