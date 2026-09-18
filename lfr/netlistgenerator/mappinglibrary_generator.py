from typing import Dict, List

from lfr import parameters as lfr_parameters
from lfr.fig.interaction import InteractionType
from lfr.netlistgenerator.connectingoption import ConnectingOption
from lfr.netlistgenerator.connection_primitive import ConnectionPrimitive
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from lfr.netlistgenerator.primitive import Primitive, PrimitiveType
from lfr.netlistgenerator.procedural_component_algorithms.mux import MUX
from lfr.netlistgenerator.procedural_component_algorithms.ytree import YTREE


def _add_default_connection_primitives(library: MappingLibrary) -> None:
    """Register the LFR default channel type, plus square CHANNEL as a fallback.

    Square 3DuF CHANNEL rectangles leave a gap at 90° corners. The default is
    ``ROUNDED CHANNEL`` (override with ``NEPTUNE_DEFAULT_CHANNEL=CHANNEL``).
    """
    default_connection = ConnectionPrimitive(lfr_parameters.DEFAULT_CONNECTION_ENTITY)
    library.add_connection_entry(default_connection)
    if lfr_parameters.DEFAULT_CONNECTION_ENTITY.upper() != "CHANNEL":
        library.add_connection_entry(ConnectionPrimitive("CHANNEL"))


def generate_mlsi_library() -> MappingLibrary:
    library = MappingLibrary("mlsi")
    # PORT
    port_inputs: List[ConnectingOption] = []
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

    port_outputs: List[ConnectingOption] = []
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

    cf_mixer_inputs: List[ConnectingOption] = []

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

    cf_mixer_outputs: List[ConnectingOption] = []

    cf_mixer_outputs.append(ConnectingOption(None, ["2"]))

    cf_mixer_loadings: List[ConnectingOption] = []
    cf_mixer_carriers: List[ConnectingOption] = []

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
    # Fluid * numeric lowers to DILUTE on the FIG; primitives must advertise DILUTE, not MIX.
    dilute_cf_mixer = Primitive(
        "MIXER",
        PrimitiveType.COMPONENT,
        r"""{
            v1:DILUTE
        }""",
        False,
        False,
        cf_mixer_inputs,
        cf_mixer_outputs,
        cf_mixer_loadings,
        cf_mixer_carriers,
        None,
    )
    library.add_operator_entry(dilute_cf_mixer, InteractionType.DILUTE)

    # MUX2

    mux2_inputs: List[ConnectingOption] = []
    mux2_inputs.append(ConnectingOption(None, ["1"]))

    mux2_outputs: List[ConnectingOption] = []
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
    _add_default_connection_primitives(library)

    return library


def generate_mars_library() -> MappingLibrary:
    library = MappingLibrary("mars")

    # PORT
    port_inputs: List[ConnectingOption] = []
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

    port_outputs: List[ConnectingOption] = []
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

    mixer_inputs: List[ConnectingOption] = []

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

    mixer_outputs: List[ConnectingOption] = []

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

    mixer_loadings: List[ConnectingOption] = []
    mixer_carriers: List[ConnectingOption] = []

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
    dilute_mars_mixer = Primitive(
        "MIXER",
        PrimitiveType.COMPONENT,
        "DILUTE",
        False,
        False,
        mixer_inputs,
        mixer_outputs,
        mixer_loadings,
        mixer_carriers,
        None,
    )
    library.add_operator_entry(dilute_mars_mixer, InteractionType.DILUTE)

    # DIAMOND REACTION CHAMBER

    diamond_chamber_inputs: List[ConnectingOption] = []

    diamond_chamber_inputs.append(ConnectingOption("default_component", ["1"]))

    diamond_chamber_outputs: List[ConnectingOption] = []

    diamond_chamber_outputs.append(ConnectingOption("default_component", ["2"]))

    diamond_chamber_loadings: List[ConnectingOption] = []
    diamond_chamber_carriers: List[ConnectingOption] = []

    diamond_chamber = Primitive(
        "DIAMOND REACTION CHAMBER",
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

    meter_inputs: List[ConnectingOption] = []

    meter_outputs: List[ConnectingOption] = []

    meter_outputs.append(ConnectingOption("default_component", ["1"]))

    meter_loadings: List[ConnectingOption] = []

    meter_loadings.append(ConnectingOption("default_component", ["2"]))

    meter_carriers: List[ConnectingOption] = []

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

    incubator_inputs: List[ConnectingOption] = []

    incubator_inputs.append(ConnectingOption("default_component", ["1"]))

    incubator_outputs: List[ConnectingOption] = []

    incubator_outputs.append(ConnectingOption("default_component", ["1"]))

    incubator_loadings: List[ConnectingOption] = []
    incubator_carriers: List[ConnectingOption] = []

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

    sorter_inputs: List[ConnectingOption] = []

    sorter_inputs.append(ConnectingOption(None, ["1"]))

    sorter_outputs: List[ConnectingOption] = []

    sorter_outputs.append(ConnectingOption(None, ["2"]))
    sorter_outputs.append(ConnectingOption(None, ["3"]))

    sorter_loadings: List[ConnectingOption] = []
    sorter_carriers: List[ConnectingOption] = []

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
    _add_default_connection_primitives(library)

    return library


def generate_dropx_library() -> MappingLibrary:
    library = MappingLibrary("dropx")

    #BlackBox (legacy 4-port) — keep registered so existing MINT still maps
    black_box_inputs: List[ConnectingOption] = []
    black_box_inputs.append(ConnectingOption(None, ["1"]))
    black_box_inputs.append(ConnectingOption(None, ["2"]))

    black_box_outputs: List[ConnectingOption] = []
    black_box_outputs.append(ConnectingOption(None, ["3"]))
    black_box_outputs.append(ConnectingOption(None, ["4"]))

    black_box = Primitive(
        "BLACK BOX",
        PrimitiveType.COMPONENT,
        r"""{
            v1: BLACK BOX
        }""",
        False,
        False,
        black_box_inputs,
        black_box_outputs,
        None,
        None,
        None,
    )
    library.add_operator_entry(black_box, InteractionType.TECHNOLOGY_PROCESS)

    # DIYCOMPONENT — user black-box placeholder (length/width/height/componentSpacing).
    # Terminals: 1=up, 2=right, 3=down, 4=left. Instance DiyTerminalConstraint
    # selects which sides are used; defaults cover a simple up→down through-flow.
    diy_inputs: List[ConnectingOption] = []
    diy_inputs.append(ConnectingOption(None, ["1"]))
    diy_inputs.append(ConnectingOption(None, ["2"]))
    diy_inputs.append(ConnectingOption(None, ["3"]))
    diy_inputs.append(ConnectingOption(None, ["4"]))

    diy_outputs: List[ConnectingOption] = []
    diy_outputs.append(ConnectingOption(None, ["1"]))
    diy_outputs.append(ConnectingOption(None, ["2"]))
    diy_outputs.append(ConnectingOption(None, ["3"]))
    diy_outputs.append(ConnectingOption(None, ["4"]))

    diy_component = Primitive(
        "DIYCOMPONENT",
        PrimitiveType.COMPONENT,
        r"""{
            v1: DIYCOMPONENT
        }""",
        False,
        False,
        diy_inputs,
        diy_outputs,
        None,
        None,
        None,
    )
    library.add_operator_entry(diy_component, InteractionType.TECHNOLOGY_PROCESS)

    #Chamber
    chamber_inputs: List[ConnectingOption] = []
    chamber_inputs.append(ConnectingOption(None, ["1"]))
    chamber_inputs.append(ConnectingOption(None, ["2"]))

    chamber_outputs: List[ConnectingOption] = []
    chamber_outputs.append(ConnectingOption(None, ["3"]))
    chamber_outputs.append(ConnectingOption(None, ["4"]))

    chamber = Primitive(
        "REACTION CHAMBER",
        PrimitiveType.COMPONENT,
        r"""{
            v1: REACTION CHAMBER
        }""",
        False,
        False,
        chamber_inputs,
        chamber_outputs,
        None,
        None,
        None,
    )

    library.add_io_entry(chamber)

    # VIA — single-port junction (Nature test_device vias / LFR #MAP "VIA" "storage").
    # All connections share terminal 1 so a storage node can be a star hub.
    via_inputs: List[ConnectingOption] = []
    via_outputs: List[ConnectingOption] = []
    for _ in range(12):
        via_inputs.append(ConnectingOption(None, ["1"]))
        via_outputs.append(ConnectingOption(None, ["1"]))

    via = Primitive(
        "VIA",
        PrimitiveType.COMPONENT,
        r"""{
            v1: VIA
        }""",
        False,
        False,
        via_inputs,
        via_outputs,
        None,
        None,
        None,
    )
    library.add_io_entry(via)
    library.add_storage_entry(via)

    # PORT
    port_inputs: List[ConnectingOption] = []
    port_inputs.append(ConnectingOption(None, ["1"]))

    port_outputs: List[ConnectingOption] = []
    port_outputs.append(ConnectingOption(None, ["1"]))

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

    # NORMAL MIXER

    mixer_inputs: List[ConnectingOption] = []

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

    mixer_outputs: List[ConnectingOption] = []

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

    mixer_loadings: List[ConnectingOption] = []
    mixer_carriers: List[ConnectingOption] = []

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
    dilute_dropx_mixer = Primitive(
        "MIXER",
        PrimitiveType.COMPONENT,
        r"""{
            v1:DILUTE
        }""",
        False,
        False,
        mixer_inputs,
        mixer_outputs,
        mixer_loadings,
        mixer_carriers,
        None,
    )
    library.add_operator_entry(dilute_dropx_mixer, InteractionType.DILUTE)

    # PICO INJECTOR

    pico_injector_inputs: List[ConnectingOption] = []

    pico_injector_inputs.append(ConnectingOption(None, ["1"]))
    pico_injector_inputs.append(ConnectingOption(None, ["2"]))

    pico_injector_outputs: List[ConnectingOption] = []

    pico_injector_outputs.append(ConnectingOption(None, ["3"]))

    pico_injector_loadings: List[ConnectingOption] = []
    pico_injector_carriers: List[ConnectingOption] = []

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

    electrophoresis_merger_inputs: List[ConnectingOption] = []

    electrophoresis_merger_inputs.append(ConnectingOption(None, ["1"]))
    electrophoresis_merger_inputs.append(ConnectingOption(None, ["2"]))

    electrophoresis_merger_outputs: List[ConnectingOption] = []

    electrophoresis_merger_outputs.append(ConnectingOption(None, ["3"]))

    electrophoresis_merger_loadings: List[ConnectingOption] = []
    electrophoresis_merger_carriers: List[ConnectingOption] = []

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

    droplet_sorter_inputs: List[ConnectingOption] = []

    droplet_sorter_inputs.append(ConnectingOption(None, ["1"]))

    droplet_sorter_outputs: List[ConnectingOption] = []

    droplet_sorter_outputs.append(ConnectingOption(None, ["2"]))
    droplet_sorter_outputs.append(ConnectingOption(None, ["3"]))

    droplet_sorter_loadings: List[ConnectingOption] = []
    droplet_sorter_carriers: List[ConnectingOption] = []

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

    droplet_generator_inputs: List[ConnectingOption] = []

    droplet_generator_inputs.append(ConnectingOption("default_component", ["1"]))

    droplet_generator_outputs: List[ConnectingOption] = []

    droplet_generator_outputs.append(ConnectingOption("default_component", ["3"]))

    droplet_generator_loadings: List[ConnectingOption] = []
    droplet_generator_carriers: List[ConnectingOption] = []

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

    droplet_merger_junction_inputs: List[ConnectingOption] = []

    droplet_merger_junction_inputs.append(ConnectingOption(None, ["1"]))
    droplet_merger_junction_inputs.append(ConnectingOption(None, ["2"]))

    droplet_merger_junction_outputs: List[ConnectingOption] = []

    droplet_merger_junction_outputs.append(ConnectingOption(None, ["3"]))

    droplet_merger_junction_loadings: List[ConnectingOption] = []
    droplet_merger_junction_carriers: List[ConnectingOption] = []

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

    droplet_merger_channel_inputs: List[ConnectingOption] = []

    droplet_merger_channel_inputs.append(ConnectingOption(None, ["1"]))

    droplet_merger_channel_outputs: List[ConnectingOption] = []

    droplet_merger_channel_outputs.append(ConnectingOption(None, ["2"]))

    droplet_merger_channel_loadings: List[ConnectingOption] = []
    droplet_merger_channel_carriers: List[ConnectingOption] = []

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

    cf_mixer_inputs: List[ConnectingOption] = []

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

    cf_mixer_outputs: List[ConnectingOption] = []

    cf_mixer_outputs.append(ConnectingOption(None, ["2"]))

    cf_mixer_loadings: List[ConnectingOption] = []
    cf_mixer_carriers: List[ConnectingOption] = []

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

    droplet_splitter_inputs: List[ConnectingOption] = []

    droplet_splitter_inputs.append(ConnectingOption(None, ["1"]))

    droplet_splitter_outputs: List[ConnectingOption] = []

    droplet_splitter_outputs.append(ConnectingOption(None, ["2"]))
    droplet_splitter_outputs.append(ConnectingOption(None, ["3"]))

    droplet_splitter_loadings: List[ConnectingOption] = []
    droplet_splitter_carriers: List[ConnectingOption] = []

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

    # DROPLET CAPACITANCE SENSOR

    droplet_capacitance_sensor_inputs: List[ConnectingOption] = []

    droplet_capacitance_sensor_inputs.append(ConnectingOption(None, ["1"]))

    droplet_capacitance_sensor_outputs: List[ConnectingOption] = []

    droplet_capacitance_sensor_outputs.append(ConnectingOption(None, ["2"]))

    droplet_capacitance_sensor_loadings: List[ConnectingOption] = []
    droplet_capacitance_sensor_carriers: List[ConnectingOption] = []

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

    # Cell Trapper

    cell_trapper_inputs: List[ConnectingOption] = []

    cell_trapper_inputs.append(ConnectingOption(None, ["1"]))

    cell_trapper_outputs: List[ConnectingOption] = []

    cell_trapper_outputs.append(ConnectingOption(None, ["2"]))

    cell_trapper_loadings: List[ConnectingOption] = []
    cell_trapper_carriers: List[ConnectingOption] = []

    cell_trapper = Primitive(
        "SQUARE CELL TRAP",
        PrimitiveType.COMPONENT,
        r"""{
            v1:STORAGE
        }""",
        True,
        True,
        cell_trapper_inputs,
        cell_trapper_outputs,
        cell_trapper_loadings,
        cell_trapper_carriers,
        None,
    )

    library.add_operator_entry(
        cell_trapper, InteractionType.TECHNOLOGY_PROCESS
    )

    # Long Cell Trapper

    long_cell_trapper_inputs: List[ConnectingOption] = []

    long_cell_trapper_inputs.append(ConnectingOption(None, ["1"]))

    long_cell_trapper_outputs: List[ConnectingOption] = []

    long_cell_trapper_outputs.append(ConnectingOption(None, ["2"]))

    long_cell_trapper_loadings: List[ConnectingOption] = []
    long_cell_trapper_carriers: List[ConnectingOption] = []

    long_cell_trapper = Primitive(
        "LONG CELL TRAPPER",
        PrimitiveType.COMPONENT,
        r"""{
            v1:STORAGE
        }""",
        True,
        True,
        long_cell_trapper_inputs,
        long_cell_trapper_outputs,
        long_cell_trapper_loadings,
        long_cell_trapper_carriers,
        None,
    )

    library.add_operator_entry(
        long_cell_trapper, InteractionType.TECHNOLOGY_PROCESS
    )

    # FILTER

    filter_inputs: List[ConnectingOption] = []

    filter_inputs.append(ConnectingOption(None, ["1"]))

    filter_outputs: List[ConnectingOption] = []

    filter_outputs.append(ConnectingOption(None, ["2"]))

    filter_loadings: List[ConnectingOption] = []
    filter_carriers: List[ConnectingOption] = []

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

    droplet_fluorescence_sensor_inputs: List[ConnectingOption] = []

    droplet_fluorescence_sensor_inputs.append(ConnectingOption(None, ["1"]))

    droplet_fluorescence_sensor_outputs: List[ConnectingOption] = []

    droplet_fluorescence_sensor_outputs.append(ConnectingOption(None, ["2"]))

    droplet_fluorescence_sensor_loadings: List[ConnectingOption] = []
    droplet_fluorescence_sensor_carriers: List[ConnectingOption] = []

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
    droplet_luminescence_sensor_inputs: List[ConnectingOption] = []

    droplet_luminescence_sensor_inputs.append(ConnectingOption(None, ["1"]))

    droplet_luminescence_sensor_outputs: List[ConnectingOption] = []

    droplet_luminescence_sensor_outputs.append(ConnectingOption(None, ["2"]))

    droplet_luminescence_sensor_loadings: List[ConnectingOption] = []
    droplet_luminescence_sensor_carriers: List[ConnectingOption] = []

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

    droplet_spacer_inputs: List[ConnectingOption] = []

    droplet_spacer_inputs.append(ConnectingOption("default_component", ["1"]))

    droplet_spacer_outputs: List[ConnectingOption] = []

    droplet_spacer_outputs.append(ConnectingOption("default_component", ["2"]))

    droplet_spacer_loadings: List[ConnectingOption] = []
    droplet_spacer_carriers: List[ConnectingOption] = []

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

    # YTREE / MUX — procedural primitives for ``#MAP "YTREE"|"MUX" "assign"``
    library.add_procedural_entry(YTREE())
    library.add_procedural_entry(MUX())

    _add_default_connection_primitives(library)

    return library


# def generate_MARS_library() -> MappingLibrary:
#     # TODO - Programatically create each of the items necessary for the MARS
# primitive library,
#     # we shall serialize them after experimentation

#     # mix_primitive = MappingOption()


#     # mix_primitive.init_single_component(mint_component)

#     # mix_primitive.add
#     pass
