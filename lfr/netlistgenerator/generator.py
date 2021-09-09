from lfr.netlistgenerator.constructiongraph.constructiongraphv2 import (
    ConstructionGraphV2,
)
from lfr.netlistgenerator.constructiongraph.variant_generator import (
    generate_match_variants,
)
import sys
from copy import deepcopy
from typing import Dict, FrozenSet, List, Set, Tuple
import networkx as nx

from pymint.mintdevice import MINTDevice
from lfr.graphmatch.interface import get_fig_matches

from lfr.netlistgenerator.procedural_component_algorithms.ytree import YTREE
from lfr.netlistgenerator.gen_strategies.dropxstrategy import DropXStrategy
from lfr.netlistgenerator.gen_strategies.marsstrategy import MarsStrategy
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.postprocessor.mapping import (
    FluidicOperatorMapping,
    NetworkMapping,
    NodeMappingInstance,
    NodeMappingTemplate,
    PumpMapping,
    StorageMapping,
)
from pymint.mintlayer import MINTLayerType
from lfr.netlistgenerator.primitive import NetworkPrimitive, Primitive, PrimitiveType
from lfr.netlistgenerator.connectingoption import ConnectingOption
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from lfr.netlistgenerator.networkmappingoption import (
    NetworkMappingOption,
    NetworkMappingOptionType,
)
from lfr.netlistgenerator.gen_strategies.genstrategy import GenStrategy
from lfr.fig.fignode import IOType, Pump, Storage, ValueNode
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.gen_strategies.dummy import DummyStrategy
from lfr.netlistgenerator.constructionnode import ConstructionNode

# from lfr.netlistgenerator.constructiongraph import ConstructionGraph
from lfr.fig.interaction import (
    FluidIntegerInteraction,
    FluidNumberInteraction,
    InteractionType,
)
from lfr.netlistgenerator.mappingoption import MappingOption
from lfr.compiler.module import Module
import itertools

# def generate_MARS_library() -> MappingLibrary:
#     # TODO - Programatically create each of the items necessary for the MARS
# primitive library,
#     # we shall serialize them after experimentation

#     # mix_primitive = MappingOption()


#     # mix_primitive.init_single_component(mint_component)

#     # mix_primitive.add
#     pass


def generate_mlsi_library() -> MappingLibrary:

    library = MappingLibrary("mlsi")
    # PORT
    port_inputs = []
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))

    port_outputs = []
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))

    port = Primitive(
        "PORT",
        PrimitiveType.COMPONENT,
        r"""{
            v1:IO
        }""",
        False,
        False,
        port_inputs,
        port_outputs,
        None,
        None,
        None,
    )

    library.add_io_entry(port)

    # MIXER - CONTINOUS FLOW ONE

    cf_mixer_inputs = []

    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))

    cf_mixer_outputs = []

    cf_mixer_outputs.append(ConnectingOption(None, ["2"]))

    cf_mixer_loadings = []
    cf_mixer_carriers = []

    cf_mixer = Primitive(
        "MIXER",
        PrimitiveType.COMPONENT,
        r"""{
            v1:MIX
        }""",
        False,
        False,
        cf_mixer_inputs,
        cf_mixer_outputs,
        cf_mixer_loadings,
        cf_mixer_carriers,
        None,
    )

    library.add_operator_entry(cf_mixer, InteractionType.MIX)

    # MUX2

    mux2_inputs = []
    mux2_inputs.append(ConnectingOption(None, ["1"]))

    mux2_outputs = []
    mux2_outputs.append(ConnectingOption(None, ["2"]))
    mux2_outputs.append(ConnectingOption(None, ["3"]))

    mux2 = Primitive(
        "MUX",
        PrimitiveType.COMPONENT,
        r"""{
            v1 { "DISTRIBUTE_OR", "or_1" },
            v1 -> vo1 { "DISTRIBUTE_OR", "or_1" },
            v1 -> vo2 { "DISTRIBUTE_OR", "or_1" }
        }
        """,
        False,
        False,
        mux2_inputs,
        mux2_outputs,
        None,
        None,
        None,
    )

    library.add_entry(mux2)

    return library


def generate_mars_library() -> MappingLibrary:

    library = MappingLibrary("mars")

    # PORT
    port_inputs = []
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))

    port_outputs = []
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))

    port = Primitive(
        "PORT",
        PrimitiveType.COMPONENT,
        "IO",
        False,
        False,
        port_inputs,
        port_outputs,
        None,
        None,
        None,
    )

    library.add_io_entry(port)

    # NORMAL MIXER

    mixer_inputs = []

    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))

    mixer_outputs = []

    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))

    mixer_loadings = []
    mixer_carriers = []

    mixer = Primitive(
        "MIXER",
        PrimitiveType.COMPONENT,
        "MIX",
        False,
        False,
        mixer_inputs,
        mixer_outputs,
        mixer_loadings,
        mixer_carriers,
        None,
    )

    library.add_operator_entry(mixer, InteractionType.MIX)

    # DIAMOND CHAMBER

    diamond_chamber_inputs = []

    diamond_chamber_inputs.append(ConnectingOption("default_component", ["1"]))

    diamond_chamber_outputs = []

    diamond_chamber_outputs.append(ConnectingOption("default_component", ["2"]))

    diamond_chamber_loadings = []
    diamond_chamber_carriers = []

    diamond_chamber = Primitive(
        "DIAMOND CHAMBER",
        PrimitiveType.COMPONENT,
        "PROCESS",
        False,
        False,
        diamond_chamber_inputs,
        diamond_chamber_outputs,
        diamond_chamber_loadings,
        diamond_chamber_carriers,
        None,
    )

    library.add_operator_entry(diamond_chamber, InteractionType.TECHNOLOGY_PROCESS)

    # METER

    meter_inputs = []

    meter_outputs = []

    meter_outputs.append(ConnectingOption("default_component", ["1"]))

    meter_loadings = []

    meter_loadings.append(ConnectingOption("default_component", ["2"]))

    meter_carriers = []

    meter_carriers.append(ConnectingOption("default_component", ["3"]))

    meter = Primitive(
        "METER",
        PrimitiveType.NETLIST,
        "METER",
        False,
        False,
        meter_inputs,
        meter_outputs,
        meter_loadings,
        meter_carriers,
        "default-netlists/dropletgenerator.mint",
        ["droplet_size", "generation_rate"],
        [
            "orifice_size",
            "aspect_ratio",
            "capillary_number",
            "expansion_ratio",
            "flow_rate_ratio",
            "normalized_oil_inlet",
            "normalized_orifice_length",
            "normalized_water_inlet",
        ],
    )

    library.add_operator_entry(meter, InteractionType.METER)

    # Incubator

    incubator_inputs = []

    incubator_inputs.append(ConnectingOption("default_component", ["1"]))

    incubator_outputs = []

    incubator_outputs.append(ConnectingOption("default_component", ["1"]))

    incubator_loadings = []
    incubator_carriers = []

    incubator = Primitive(
        "INCUBATOR",
        PrimitiveType.COMPONENT,
        "PROCESS",
        False,
        False,
        incubator_inputs,
        incubator_outputs,
        incubator_loadings,
        incubator_carriers,
    )

    library.add_operator_entry(incubator, InteractionType.TECHNOLOGY_PROCESS)

    # SORTER

    sorter_inputs = []

    sorter_inputs.append(ConnectingOption(None, ["1"]))

    sorter_outputs = []

    sorter_outputs.append(ConnectingOption(None, ["2"]))
    sorter_outputs.append(ConnectingOption(None, ["3"]))

    sorter_loadings = []
    sorter_carriers = []

    # TODO - Modify this later on
    sorter = Primitive(
        "DROPLET SORTER",
        PrimitiveType.COMPONENT,
        "SIEVE",
        False,
        False,
        sorter_inputs,
        sorter_outputs,
        sorter_loadings,
        sorter_carriers,
        None,
    )

    library.add_operator_entry(sorter, InteractionType.SIEVE)

    return library


def generate_dropx_library() -> MappingLibrary:

    library = MappingLibrary("dropx")

    # PORT
    port_inputs = []
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))

    port_outputs = []
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))

    port = Primitive(
        "PORT",
        PrimitiveType.COMPONENT,
        r"""{
            v1:IO
        }""",
        False,
        False,
        port_inputs,
        port_outputs,
        None,
        None,
        None,
    )

    library.add_io_entry(port)

    # PICO INJECTOR

    pico_injector_inputs = []

    pico_injector_inputs.append(ConnectingOption(None, ["1"]))
    pico_injector_inputs.append(ConnectingOption(None, ["2"]))

    pico_injector_outputs = []

    pico_injector_outputs.append(ConnectingOption(None, ["3"]))

    pico_injector_loadings = []
    pico_injector_carriers = []

    pico_injector = Primitive(
        "PICOINJECTOR",
        PrimitiveType.COMPONENT,
        r"""{
            v1:MIX
        }""",
        False,
        False,
        pico_injector_inputs,
        pico_injector_outputs,
        pico_injector_loadings,
        pico_injector_carriers,
        None,
    )

    library.add_operator_entry(pico_injector, InteractionType.MIX)

    # DROPLET ELECTROPHORESIS MERGER

    electrophoresis_merger_inputs = []

    electrophoresis_merger_inputs.append(ConnectingOption(None, ["1"]))
    electrophoresis_merger_inputs.append(ConnectingOption(None, ["2"]))

    electrophoresis_merger_outputs = []

    electrophoresis_merger_outputs.append(ConnectingOption(None, ["3"]))

    electrophoresis_merger_loadings = []
    electrophoresis_merger_carriers = []

    # TODO - Modify this later on
    electrophoresis_merger = Primitive(
        "DROPLET MERGER",
        PrimitiveType.COMPONENT,
        r"""{
            v1:MIX
        }""",
        False,
        False,
        electrophoresis_merger_inputs,
        electrophoresis_merger_outputs,
        electrophoresis_merger_loadings,
        electrophoresis_merger_carriers,
        None,
    )

    library.add_operator_entry(electrophoresis_merger, InteractionType.MIX)

    # DROPLET SORTER

    droplet_sorter_inputs = []

    droplet_sorter_inputs.append(ConnectingOption(None, ["1"]))

    droplet_sorter_outputs = []

    droplet_sorter_outputs.append(ConnectingOption(None, ["2"]))
    droplet_sorter_outputs.append(ConnectingOption(None, ["3"]))

    droplet_sorter_loadings = []
    droplet_sorter_carriers = []

    # TODO - Modify this later on
    droplet_sorter = Primitive(
        "DROPLET SORTER",
        PrimitiveType.COMPONENT,
        r"""{
            v1:SIEVE
        }""",
        False,
        False,
        droplet_sorter_inputs,
        droplet_sorter_outputs,
        droplet_sorter_loadings,
        droplet_sorter_carriers,
        None,
    )

    library.add_operator_entry(droplet_sorter, InteractionType.SIEVE)

    # DROPLET GENERATOR

    droplet_generator_inputs = []

    droplet_generator_inputs.append(ConnectingOption("default_component", ["1"]))

    droplet_generator_outputs = []

    droplet_generator_outputs.append(ConnectingOption("default_component", ["3"]))

    droplet_generator_loadings = []
    droplet_generator_carriers = []

    droplet_generator = Primitive(
        "NOZZLE DROPLET GENERATOR",
        PrimitiveType.NETLIST,
        r"""{
            v1:METER
        }""",
        False,
        False,
        droplet_generator_inputs,
        droplet_generator_outputs,
        droplet_generator_loadings,
        droplet_generator_carriers,
        "default-netlists/dropletgenerator.mint",
        ["droplet_size", "generation_rate"],
        [
            "orifice_size",
            "aspect_ratio",
            "capillary_number",
            "expansion_ratio",
            "flow_rate_ratio",
            "normalized_oil_inlet",
            "normalized_orifice_length",
            "normalized_water_inlet",
        ],
    )

    library.add_operator_entry(droplet_generator, InteractionType.METER)

    droplet_merger_junction_inputs = []

    droplet_merger_junction_inputs.append(ConnectingOption(None, ["1"]))
    droplet_merger_junction_inputs.append(ConnectingOption(None, ["2"]))

    droplet_merger_junction_outputs = []

    droplet_merger_junction_outputs.append(ConnectingOption(None, ["3"]))

    droplet_merger_junction_loadings = []
    droplet_merger_junction_carriers = []

    droplet_merger_junction = Primitive(
        "DROPLET MERGER JUNCTION",
        PrimitiveType.COMPONENT,
        r"""{
            v1:MIX
        }""",
        False,
        False,
        droplet_merger_junction_inputs,
        droplet_merger_junction_outputs,
        droplet_merger_junction_loadings,
        droplet_merger_junction_carriers,
        None,
    )

    library.add_operator_entry(droplet_merger_junction, InteractionType.MIX)

    # DROPLET MERGER CHANNEL

    droplet_merger_channel_inputs = []

    droplet_merger_channel_inputs.append(ConnectingOption(None, ["1"]))

    droplet_merger_channel_outputs = []

    droplet_merger_channel_outputs.append(ConnectingOption(None, ["2"]))

    droplet_merger_channel_loadings = []
    droplet_merger_channel_carriers = []

    droplet_merger_channel = Primitive(
        "DROPLET MERGER CHANNEL",
        PrimitiveType.COMPONENT,
        r"""{
            v1:MIX
        }""",
        False,
        False,
        droplet_merger_channel_inputs,
        droplet_merger_channel_outputs,
        droplet_merger_channel_loadings,
        droplet_merger_channel_carriers,
        None,
    )

    library.add_operator_entry(droplet_merger_channel, InteractionType.MIX)

    # MIXER - CONTINOUS FLOW ONE

    cf_mixer_inputs = []

    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))

    cf_mixer_outputs = []

    cf_mixer_outputs.append(ConnectingOption(None, ["2"]))

    cf_mixer_loadings = []
    cf_mixer_carriers = []

    cf_mixer = Primitive(
        "MIXER",
        PrimitiveType.COMPONENT,
        r"""{
            v1:MIX
        }""",
        False,
        False,
        cf_mixer_inputs,
        cf_mixer_outputs,
        cf_mixer_loadings,
        cf_mixer_carriers,
        None,
    )

    library.add_operator_entry(cf_mixer, InteractionType.MIX)

    # DROPLET SPLITTER

    droplet_splitter_inputs = []

    droplet_splitter_inputs.append(ConnectingOption(None, ["1"]))

    droplet_splitter_outputs = []

    droplet_splitter_outputs.append(ConnectingOption(None, ["2"]))
    droplet_splitter_outputs.append(ConnectingOption(None, ["3"]))

    droplet_splitter_loadings = []
    droplet_splitter_carriers = []

    droplet_splitter = Primitive(
        "DROPLET SPLITTER",
        PrimitiveType.COMPONENT,
        r"""{
            v1:DIVIDE
        }""",
        False,
        False,
        droplet_splitter_inputs,
        droplet_splitter_outputs,
        droplet_splitter_loadings,
        droplet_splitter_carriers,
        None,
    )

    library.add_operator_entry(droplet_splitter, InteractionType.DIVIDE)

    # NORMAL MIXER

    mixer_inputs = []

    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))
    mixer_inputs.append(ConnectingOption(None, ["1"]))

    mixer_outputs = []

    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))
    mixer_outputs.append(ConnectingOption(None, ["2"]))

    mixer_loadings = []
    mixer_carriers = []

    mixer = Primitive(
        "MIXER",
        PrimitiveType.COMPONENT,
        r"""{
            v1:MIX
        }""",
        False,
        False,
        mixer_inputs,
        mixer_outputs,
        mixer_loadings,
        mixer_carriers,
        None,
    )

    library.add_operator_entry(mixer, InteractionType.MIX)

    # DROPLET CAPACITANCE SENSOR

    droplet_capacitance_sensor_inputs = []

    droplet_capacitance_sensor_inputs.append(ConnectingOption(None, ["1"]))

    droplet_capacitance_sensor_outputs = []

    droplet_capacitance_sensor_outputs.append(ConnectingOption(None, ["2"]))

    droplet_capacitance_sensor_loadings = []
    droplet_capacitance_sensor_carriers = []

    droplet_capacitance_sensor = Primitive(
        "DROPLET CAPACITANCE SENSOR",
        PrimitiveType.COMPONENT,
        r"""{
            v1:PROCESS
        }""",
        False,
        False,
        droplet_capacitance_sensor_inputs,
        droplet_capacitance_sensor_outputs,
        droplet_capacitance_sensor_loadings,
        droplet_capacitance_sensor_carriers,
        None,
    )

    library.add_operator_entry(
        droplet_capacitance_sensor, InteractionType.TECHNOLOGY_PROCESS
    )

    # FILTER

    filter_inputs = []

    filter_inputs.append(ConnectingOption(None, ["1"]))

    filter_outputs = []

    filter_outputs.append(ConnectingOption(None, ["2"]))

    filter_loadings = []
    filter_carriers = []

    filter = Primitive(
        "FILTER",
        PrimitiveType.COMPONENT,
        r"""{
            v1:PROCESS
        }""",
        False,
        False,
        filter_inputs,
        filter_outputs,
        filter_loadings,
        filter_carriers,
        None,
    )

    library.add_operator_entry(filter, InteractionType.TECHNOLOGY_PROCESS)

    # DROPLET FLUORESCENCE SENSOR

    droplet_fluorescence_sensor_inputs = []

    droplet_fluorescence_sensor_inputs.append(ConnectingOption(None, ["1"]))

    droplet_fluorescence_sensor_outputs = []

    droplet_fluorescence_sensor_outputs.append(ConnectingOption(None, ["2"]))

    droplet_fluorescence_sensor_loadings = []
    droplet_fluorescence_sensor_carriers = []

    droplet_fluorescence_sensor = Primitive(
        "DROPLET FLUORESCENCE SENSOR",
        PrimitiveType.COMPONENT,
        r"""{
            v1:PROCESS
        }""",
        False,
        False,
        droplet_fluorescence_sensor_inputs,
        droplet_fluorescence_sensor_outputs,
        droplet_fluorescence_sensor_loadings,
        droplet_fluorescence_sensor_carriers,
        None,
    )

    library.add_operator_entry(
        droplet_fluorescence_sensor, InteractionType.TECHNOLOGY_PROCESS
    )

    # DROPLET LUMINESCENCE SENSOR
    droplet_luminescence_sensor_inputs = []

    droplet_luminescence_sensor_inputs.append(ConnectingOption(None, ["1"]))

    droplet_luminescence_sensor_outputs = []

    droplet_luminescence_sensor_outputs.append(ConnectingOption(None, ["2"]))

    droplet_luminescence_sensor_loadings = []
    droplet_luminescence_sensor_carriers = []

    droplet_luminescence_sensor = Primitive(
        "DROPLET LUMINESCENCE SENSOR",
        PrimitiveType.COMPONENT,
        r"""{
            v1:PROCESS
        }""",
        False,
        False,
        droplet_luminescence_sensor_inputs,
        droplet_luminescence_sensor_outputs,
        droplet_luminescence_sensor_loadings,
        droplet_luminescence_sensor_carriers,
        None,
    )

    library.add_operator_entry(
        droplet_luminescence_sensor, InteractionType.TECHNOLOGY_PROCESS
    )

    # DROPLET SPACER

    droplet_spacer_inputs = []

    droplet_spacer_inputs.append(ConnectingOption("default_component", ["1"]))

    droplet_spacer_outputs = []

    droplet_spacer_outputs.append(ConnectingOption("default_component", ["2"]))

    droplet_spacer_loadings = []
    droplet_spacer_carriers = []

    droplet_spacer = Primitive(
        "DROPLET SPACER",
        PrimitiveType.NETLIST,
        r"""{
            v1:PROCESS
        }""",
        False,
        False,
        droplet_spacer_inputs,
        droplet_spacer_outputs,
        droplet_spacer_loadings,
        droplet_spacer_carriers,
        "default-netlists/dropletspacer.mint",
    )

    library.add_operator_entry(droplet_spacer, InteractionType.TECHNOLOGY_PROCESS)

    # YTREE - This is a procedural primitives

    ytree = YTREE()

    library.add_procedural_entry(ytree)

    return library


def generate(module: Module, library: MappingLibrary) -> List[MINTDevice]:

    # In order to create the device, we do the following
    # STEP 1 -
    # STEP 2 - Initialize the active strategy
    # STEP 3 - Get all the technology mapping matches for the FIG
    # STEP 4 - Eliminate the matches that are exactly the same as the explicit matches
    # STEP 5 - Generate the waste outputs
    # STEP 6 - Generate the mapping variants
    # STEP 7 - Generate the control logic network
    # STEP 8 - Generate the connections
    # STEP 9 - Size the components
    # STEP 10 - Size the connections

    # construction_graph = ConstructionGraph()

    # Step 1 -

    # STEP 2 - Initialize the active strategy
    # TODO - I need to change this DummyStrategy later on
    # if library.name == "dropx":
    #     active_strategy = DropXStrategy(construction_graph, module.FIG)
    # elif library.name == "mars":
    #     # raise NotImplementedError()
    #     active_strategy = MarsStrategy(construction_graph, module.FIG)
    # elif library.name == "hmlp":
    #     raise NotImplementedError()
    # else:
    #     active_strategy = DummyStrategy(construction_graph, module.FIG)

    # STEP 3 - Get all the technology mapping matches for the FIG
    # Do the reggie matching to find the mapping options
    # This means that we might need to have a forest of construction of graphs
    # as there would be alternatives for each type of mapping
    matches = get_fig_matches(module.FIG, library)
    print("Total Matches against library : {}".format(len(matches)))
    for match in matches:
        # Generate an object that is usable going forward (mapping template perhaps)
        print(match)

    # STEP 4 - Eliminate the matches that are exactly the same as the explicit matches
    # Get the explicit mapping and find the explicit mappings here
    explicit_mappings = module.get_explicit_mappings()
    matches = eliminate_explicit_match_alternates(matches, explicit_mappings)

    print(
        "Total matches against library after explicit mapping eliminations: {}".format(
            len(matches)
        )
    )
    for match in matches:
        print(match)

    # STEP 5 - Generate the waste outputs
    # TODO - Add fignodes to all the orphaned flow nodes for this to function
    # connect_orphan_IO()

    # STEP 6 - Generate the mapping variants
    variants = generate_match_variants(matches, module.FIG, library)

    # Now generate the devices for each of the variants
    generated_devices = []
    for variant in variants:
        # Create the device for each of the variants
        name_generator = NameGenerator()

        cur_device = MINTDevice(module.name)

        # Add a MINT Layer so that the device has something to work with
        cur_device.create_mint_layer("0", "0", 0, MINTLayerType.FLOW)

        generate_device(variant, cur_device, name_generator)
        # STEP 7 - Generate the control logic network
        # TODO - Whatever this entails (put in the implementation)

        # STEP 8 - Generate the connections
        # TODO - Generate connections between all the outputs and the inputs of the
        # construction nodes
        # TODO - write the algorithm for carriers and optimize the flows
        # Generate all the unaccounted carriers and waste output lines necessary

        # STEP 9 - Size the components
        # Size the component netlist
        # active_strategy.size_netlist(cur_device)

        generated_devices.append(cur_device)

    return generated_devices


def eliminate_explicit_match_alternates(
    matches: List[Tuple[str, Dict[str, str]]],
    explict_mappings: List[NodeMappingTemplate],
) -> List[Tuple[str, Dict[str, str]]]:

    # extract the fignode ID set from matches
    match_node_set_dict: Dict[FrozenSet, List[Tuple[str, Dict[str, str]]]] = {}
    for match in matches:
        frozen_set = frozenset(match[1].keys())
        if frozen_set not in match_node_set_dict:
            match_node_set_dict[frozen_set] = []
            match_node_set_dict[frozen_set].append(match)
        else:
            match_node_set_dict[frozen_set].append(match)

    # Go through each of the explict matches, generate a subgraph and compare against
    # all the matches
    for explicit_mapping in explict_mappings:
        # Only do the explicit mapping if the the mapping object has a technology
        # associated with it else skip it
        if explicit_mapping.technology_string is None:
            continue

        # Generate a subgraph for each of the mapping instance fig
        for instance in explicit_mapping.instances:

            node_set = set()

            # Check what kind of an instance this is
            if isinstance(instance, NodeMappingInstance):
                # This is a single node scenario
                node_set.add(instance.node.ID)
            elif isinstance(instance, FluidicOperatorMapping):
                node_set.add(instance.node.ID)

            elif isinstance(instance, StorageMapping):
                node_set.add(instance.node.ID)

            elif isinstance(instance, PumpMapping):
                node_set.add(instance.node.ID)

            elif isinstance(instance, NetworkMapping):
                node_set = set()
                node_set.union(set([node.ID for node in instance.input_nodes]))
                node_set.union(set([node.ID for node in instance.output_nodes]))

            if frozenset(node_set) in match_node_set_dict:
                # This is an explicit match
                # Remove the explicit match from the list of matches
                print(
                    "Eliminating match: {}".format(
                        match_node_set_dict[frozenset(node_set)]
                    )
                )
                match_node_set_dict[frozenset(node_set)].clear()

            # Now generate a match tuple for this instance
            match_tuple = (
                explicit_mapping.technology_string,
                {},
            )

            # TODO - Retouch this part if we ever go into modifying how the matches are
            # generated if we use the match string coordinates (use the match interface
            # for this) (function - generate_single_match)

            # Check what kind of an instance this is
            if isinstance(instance, NodeMappingInstance):
                # This is a single node scenario
                match_tuple[1][instance.node.ID] = "v1"
            elif isinstance(instance, FluidicOperatorMapping):
                match_tuple[1][instance.node.ID] = "v1"

            elif isinstance(instance, StorageMapping):
                match_tuple[1][instance.node.ID] = "v1"

            elif isinstance(instance, PumpMapping):
                match_tuple[1][instance.node.ID] = "v1"

            elif isinstance(instance, NetworkMapping):
                for i in range(len(instance.input_nodes)):
                    node = instance.input_nodes[i]
                    match_tuple[1][node.ID] = f"vi{i}"
                for i in range(len(instance.output_nodes)):
                    node = instance.output_nodes[i]
                    match_tuple[1][node.ID] = f"vo{i}"

            # Add this match tuple to the list of matches
            if frozenset(node_set) in match_node_set_dict:
                match_node_set_dict[frozenset(node_set)].append(match_tuple)
            else:
                match_node_set_dict[frozenset(node_set)] = [match_tuple]

    # Modify the matches list
    eliminated_matches = []
    for match_tuple_list in match_node_set_dict.values():
        for match_tuple in match_tuple_list:
            eliminated_matches.append(match_tuple)

    return eliminated_matches


def generate_device(
    construction_graph: ConstructionGraphV2,
    scaffhold_device: MINTDevice,
    name_generator: NameGenerator,
) -> None:
    # TODO - Generate the device
    # Step 1 - go though each of the construction nodes and genrate the corresponding
    # components
    # Step 2 - generate the connections between the outputs to input on the connected
    # construction nodes
    # Step 3 - TODO - Generate the control network
    pass


def connect_orphan_IO():
    print("Implement the orphan io generation system")


def __check_if_passthrough(sub) -> bool:
    """Checks if its a passthrough chain

    Args:
        sub (subgraph): subgraph

    Returns:
        bool: Return true if its a single chain of flow channels
    """
    in_count = 0
    out_count = 0
    for node in list(sub.nodes):
        inedges = list(sub.in_edges(node))
        outedges = list(sub.out_edges(node))
        if len(inedges) == 0:
            in_count += 1
        if len(outedges) == 0:
            out_count += 1

    if in_count == 1 and out_count == 1:
        return True
    else:
        return False