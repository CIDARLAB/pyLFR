import pathlib

import lfr

# Global Variables
LFR_DIR = pathlib.Path(lfr.__file__).parent.parent.absolute()
LIB_DIR = LFR_DIR.joinpath("library")
OUTPUT_DIR = LFR_DIR.joinpath("output")
PREPROCESSOR_DUMP_FILE_NAME = "pre_processor_dump.lfr"
