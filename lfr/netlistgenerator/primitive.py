import copy
from enum import Enum
import hashlib
from typing import List, Optional
from parchmint import Component, Layer, Params
from pymint.mintdevice import MINTDevice

from lfr.netlistgenerator.gen_strategies.genstrategy import GenStrategy
from lfr.netlistgenerator.connectingoption import ConnectingOption
from lfr import parameters
from lfr.netlistgenerator.namegenerator import NameGenerator


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
        inputs: Optional[List[ConnectingOption]] = None,
        outputs: Optional[List[ConnectingOption]] = None,
        loadings: Optional[List[ConnectingOption]] = None,
        carriers: Optional[List[ConnectingOption]] = None,
        default_netlist: Optional[str] = None,
        functional_input_params: Optional[List[str]] = None,
        output_params: Optional[List[str]] = None,
        user_defined_params: Params = Params({}),
    ) -> None:
        if inputs is None:
            inputs = []
        if outputs is None:
            outputs = []
        if loadings is None:
            loadings = []
        if carriers is None:
            carriers = []
        if functional_input_params is None:
            functional_input_params = []
        if output_params is None:
            output_params = []

        self._component_type: PrimitiveType = component_type
        self._match_string: str = match_string
        # TODO - Cleanup the logic for this later
        if mint == "" and component_type is not PrimitiveType.PROCEDURAL:
            raise Exception(
                "Cannot instantiate an Primitive type object if mint sting is not"
                " present"
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

        self._user_defined_params: Params = user_defined_params

        # Generate the UID for the primitive
        self._uid = hashlib.md5(
            "{}_{}".format(self._mint, self._match_string).encode("utf-8")
        ).hexdigest()

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def type(self) -> PrimitiveType:
        return self._component_type

    @property
    def mint(self) -> str:
        return self._mint

    @property
    def match_string(self) -> str:
        return self._match_string

    def export_inputs(self, subgraph) -> List[ConnectingOption]:
        # TODO - Figure out how to map connecting options to match string nodes
        print(
            "Warning: Implment how the connecting option is mapped to match string node"
        )
        return [copy.copy(c) for c in self._inputs]

    def export_outputs(self, subgraph) -> List[ConnectingOption]:
        # TODO - Figure out how to map connecting options to match string nodes
        print(
            "Warning: Implment how the connecting option is mapped to match string node"
        )
        return [copy.copy(c) for c in self._outputs]

    def export_loadings(self, subgraph) -> Optional[List[ConnectingOption]]:
        # TODO - Figure out how to map connecting options to match string nodes
        print(
            "Warning: Implment how the connecting option is mapped to match string node"
        )
        if self._loadings is None:
            return None
        return [copy.copy(c) for c in self._loadings]

    def export_carriers(self, subgraph) -> Optional[List[ConnectingOption]]:
        # TODO - Figure out how to map connecting options to match string nodes
        print(
            "Warning: Implment how the connecting option is mapped to match string node"
        )
        if self._carriers is None:
            return None
        return [copy.copy(c) for c in self._carriers]

    @property
    def default_netlist_location(self):
        return self._default_netlist

    @property
    def inverse_design_query_params(self):
        return self._functional_input_params

    @property
    def output_params(self):
        return self._output_params

    def get_default_component(self, name_gen: NameGenerator, layer: Layer) -> Component:
        """Gets the default component for the primitive

        Utilizes the NameGenerator instance to generate a new component instance of
        the corresponding MINT type

        Args:
            name_gen (NameGenerator): NameGenerator instance that will generate the
                new name for the component
            layer (Layer): Layer object in which the component exists

        Raises:
            Exception: Raises an exception when the entry is not of the type COMPONENT

        Returns:
            Component: New component object
        """
        if self.type is not PrimitiveType.COMPONENT:
            raise Exception("Cannot execute this method for this kind of a primitive")
        name = name_gen.generate_name(self.mint)
        mc = Component(
            name=name, ID=name, entity=self.mint, params=Params({}), layers=[layer]
        )
        return mc

    def get_default_netlist(self, cn_id: str, name_gen: NameGenerator) -> MINTDevice:
        """Returns the default netlist for the primitive

        Args:
            cn_id (str): ID of the construction node so that we can prefix the id's of
                all the components that are part of the default netlist
            name_gen (NameGenerator): A namegenerator instance that is used for the
                globally for synthesizing the design

        Returns:
            MINTDevice: Default netlist of whatever the primitive is
        """
        if self.type is not PrimitiveType.NETLIST:
            raise Exception("Cannot execute this method for this kind of a  primitive")
        if self._default_netlist is None:
            raise Exception(
                "Cannot parse MINT file for primitive {} since default netlist"
                " parameter is set to None".format(self.mint)
            )
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

    def __hash__(self) -> int:
        return hash("{}_{}".format(self.mint, self.match_string))


class ProceduralPrimitive(Primitive):
    def __init__(
        self,
        mint: str,
        match_string: str,
        is_storage: bool,
        has_storage_control: bool,
        # inputs: List[ConnectingOption],
        # outputs: List[ConnectingOption],
        # loadings: Optional[List[ConnectingOption]],
        # carriers: Optional[List[ConnectingOption]],
        default_netlist: Optional[str],
        functional_input_params: List[str],
        output_params: List[str],
        user_defined_params: Params = Params({}),
    ) -> None:
        super().__init__(
            mint=mint,
            component_type=PrimitiveType.PROCEDURAL,
            match_string=match_string,
            is_storage=is_storage,
            has_storage_control=has_storage_control,
            # inputs=inputs,
            # outputs=outputs,
            # loadings=loadings,
            # carriers=carriers,
            default_netlist=default_netlist,
            functional_input_params=functional_input_params,
            output_params=output_params,
            user_defined_params=user_defined_params,
        )

    def export_inputs(self, subgraph) -> List[ConnectingOption]:
        raise NotImplementedError()

    def export_outputs(self, subgraph) -> List[ConnectingOption]:
        raise NotImplementedError()

    def export_loadings(self, subgraph) -> Optional[List[ConnectingOption]]:
        raise NotImplementedError()

    def export_carriers(self, subgraph) -> Optional[List[ConnectingOption]]:
        raise NotImplementedError()

    def get_default_component(self, name_gen: NameGenerator, layer: Layer) -> Component:
        raise NotImplementedError()

    def get_procedural_component(
        self, name_gen: NameGenerator, layer: Layer
    ) -> Component:
        raise NotImplementedError()

    def generate_input_connectingoptions(self, subgraph_view) -> List[ConnectingOption]:
        """Generates a list of connection options that represent where the inputs can
        be connected to the primitive

        Args:
            subgraph_view (networkx.Graph.subgraph): A subgraph view of the Fluid
            Interaction Graph

        Raises:
            NotImplementedError: Raised when its not implemented

        Returns:
            List[ConnectingOption]: List of options where we can attach connections
        """
        raise NotImplementedError()

    def generate_output_connectingoptions(
        self, subgraph_view
    ) -> List[ConnectingOption]:
        """Generates a list of connection options that represent where the outputs can
        be connected to the primitive

        Args:
            subgraph_view (networkx.Graph.subgraph): A subgraph view of the Fluid
            Interaction Graph

        Raises:
            NotImplementedError: Raised when its not implemented

        Returns:
            List[ConnectingOption]: List of options where we can attach connections
        """
        raise NotImplementedError()

    def generate_carrier_connectingoptions(
        self, subgraph_view
    ) -> List[ConnectingOption]:
        """Generates a list of connection options that represent where the carrier inputs can
        be connected to the primitive

        Args:
            subgraph_view (networkx.Graph.subgraph): A subgraph view of the Fluid
            Interaction Graph

        Raises:
            NotImplementedError: Raised when its not implemented

        Returns:
            List[ConnectingOption]: List of options where we can attach connections
        """
        raise NotImplementedError()

    def generate_loading_connectingoptions(
        self, subgraph_view
    ) -> List[ConnectingOption]:
        """Generates a list of connection options that represent where the loading inputs can
        be connected to the primitive

        Args:
            subgraph_view (networkx.Graph.subgraph): A subgraph view of the Fluid
            Interaction Graph

        Raises:
            NotImplementedError: Raised when its not implemented

        Returns:
            List[ConnectingOption]: List of options where we can attach connections
        """
        raise NotImplementedError()


class NetworkPrimitive(Primitive):
    def __init__(self, fig_subgraph_view, gen_strategy: GenStrategy) -> None:
        """A Procedural type primtive that can be used only for representing
        a network, this is usually used when we want the Generation Strategy
        needs to be used.

        Args:
            fig_subgraph_view (networkx.Graph.subgraph): Subgraph for which we
            need to generate the network for
            gen_strategy (GenStrategy): This is user defined strategy / algorithm
            that we use for generating the design
        """
        super().__init__(component_type=PrimitiveType.PROCEDURAL)

        self._gen_strategy = gen_strategy
        # Write methods that will utilize the subgraph view to generate the
        # netlist
        self._fig_subgraph_view = fig_subgraph_view
        self._netlist: Optional[MINTDevice] = None

    def generate_netlist(self) -> None:
        """Generates the netlist for the given network primitive, this method generates
        the flow network, input , output, carriers and loadings into the primitve
        properties
        """
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
        """Returns the default netlist for the primitive

        Args:
            cn_id (str): ID of the construction node so that we can prefix the id's of
            all the components that are part of the default netlist
            name_gen (NameGenerator): A namegenerator instance that is used for the
            globally for synthesizing the design

        Raises:
            Exception: Raised when there is no defualt netlist is generated

        Returns:
            MINTDevice: Default netlist of whatever the primitive is
        """
        if self._netlist is None:
            raise Exception("No default netlist present for the primitive")

        # Utilise the subgraph view to decide how you want to generate a netlist
        # Load all the inputs and outputs based on that information
        name_gen.rename_netlist(cn_id, self._netlist)
        return self._netlist
