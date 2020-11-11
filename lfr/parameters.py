import lfr
import pathlib

# Global Variables
LFR_DIR = pathlib.Path(lfr.__file__).parent.parent.absolute()
LIB_DIR = LFR_DIR.joinpath("library")
OUTPUT_DIR = LFR_DIR.joinpath("output")
