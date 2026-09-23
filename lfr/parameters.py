import os
import pathlib
from typing import Tuple

import lfr

# Global Variables
LFR_DIR = pathlib.Path(lfr.__file__).parent.parent.absolute()
LIB_DIR = LFR_DIR.joinpath("library")
OUTPUT_DIR = LFR_DIR.joinpath("output")
PREPROCESSOR_DUMP_FILE_NAME = "pre_processor_dump.lfr"
# Set during compile to module name (e.g. flow_only_demo) so each LFR gets its own output subfolder
CURRENT_MODULE_NAME = None
# When False, skip extra FIG/construction .dot and .pdf. The canonical
# ``*_fromLFR_topology.pdf`` is always written by compile_lfr.
PRINT_DEBUG_GRAPHS = False

# Default connection profile when LFR does not name a channel type.
# Square 3DuF CHANNEL rectangles stop on the centerline, so a 90° turn leaves
# a gap on the outer corner. Rounded (stadium) caps of radius channelWidth/2
# fill that corner. Override with NEPTUNE_DEFAULT_CHANNEL=CHANNEL for square.
def parse_default_connection_profile(raw: str) -> Tuple[str, int]:
    """Return (JSON/MINT entity, 3DuF crossSection) for synthesized channels.

    ``CHANNEL`` keeps square ends. Any rounded alias uses entity
    ``ROUNDED CHANNEL`` and JSON ``crossSection=1``. MINT still serializes the
    ``CHANNEL`` keyword plus ``RoundedChannel=1/0`` because
    ``ROUNDED CHANNEL name from ...`` is not a valid channelStat.
    """
    text = (raw or "").strip().upper().replace("-", " ").replace("_", " ")
    if text in ("CHANNEL", "SQUARE", "0", "RECT", "RECTANGULAR"):
        return "CHANNEL", 0
    return "ROUNDED CHANNEL", 1


DEFAULT_CONNECTION_ENTITY, DEFAULT_CONNECTION_CROSS_SECTION = parse_default_connection_profile(
    os.getenv("NEPTUNE_DEFAULT_CHANNEL", "ROUNDED CHANNEL")
)

# VALVE3D library defaults (µm). FLOW and CONTROL channelWidth match gap
# so pipes and the valve slit are the same width (square or rounded).
DEFAULT_VALVE3D_RADIUS_UM = 1200
DEFAULT_VALVE3D_GAP_UM = 600
DEFAULT_VALVE3D_WIDTH_UM = 2400
DEFAULT_VALVE3D_LENGTH_UM = 2400
DEFAULT_CHANNEL_WIDTH_UM = DEFAULT_VALVE3D_GAP_UM
DEFAULT_CONTROL_CHANNEL_WIDTH_UM = DEFAULT_CHANNEL_WIDTH_UM
# Minimum CHANNEL length (µm) between components joined by a channel.
# LFR compile writes this as CHANNEL ``length=`` / ``minChannelLength=``.
# Handwritten MINT may set either param per connection; values shorter
# than this floor are raised. Keep in sync with
# fluigi.parameters.MIN_CONNECTED_COMPONENT_DISTANCE_UM.
MIN_CONNECTED_COMPONENT_DISTANCE_UM = 1000.0
# Keepout halo written onto LFR-generated components as ``componentSpacing``.
# Keep in sync with fluigi.parameters.COMPONENT_SPACING.
DEFAULT_COMPONENT_SPACING_UM = 1000.0
