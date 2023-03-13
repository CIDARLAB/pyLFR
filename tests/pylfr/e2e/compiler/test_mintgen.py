from pathlib import Path

import networkx
from networkx import is_isomorphic
from tests.conftest import LIBRARY_PATH, TEST_DATA_FOLDER, TEST_OUTPATH

from lfr import api
from lfr.utils import printgraph

TEST_CASES_FOLDER = TEST_DATA_FOLDER.joinpath("DropX")
REF_DATA_FIG_FOLDER = TEST_CASES_FOLDER.joinpath("netlists")


def test_dx1():
    # dx1.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx1.lfr")

    # Run through the full compiler
    api.compile_lfr(
        input_files=[str(test_file)],
        outpath=str(TEST_OUTPATH),
        technology="dropx",
        pre_load=[str(LIBRARY_PATH.absolute())],
    )
