from pathlib import Path

import networkx
from networkx import is_isomorphic
from tests.conftest import LIBRARY_PATH, TEST_DATA_FOLDER, TEST_OUTPATH

from lfr import api
from lfr.utils import printgraph

TEST_CASES_FOLDER = TEST_DATA_FOLDER.joinpath("DropX")
REF_DATA_FIG_FOLDER = TEST_CASES_FOLDER.joinpath("figs")


def test_dx1():
    # dx1.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx1.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG
    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx1.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx2():
    # dx2.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx2.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx2.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx3():
    # dx3.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx3.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx3.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx4():
    # dx4.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx4.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx4.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx5():
    # dx5.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx5.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx5.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx6():
    # dx6.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx6.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx6.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx7():
    # dx7.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx7.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx7.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx8():
    # dx8.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx8.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx8.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx9():
    # dx9.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx9.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx9.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx10():
    # dx10.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx10.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx10.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx11():
    # dx11.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx11.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx11.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx12():
    # dx12.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx12.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx12.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx13():
    # dx13.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx13.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx13.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx14():
    # dx14.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx14.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx14.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True


def test_dx15():
    # dx15.lfr
    test_file = TEST_CASES_FOLDER.joinpath("dx15.lfr")
    # Read the text and dump it on console
    module_listener = api.synthesize_module(
        input_path=test_file,
        no_annotations_flag=True,
        print_fig=False,
    )

    assert module_listener.success is True
    assert module_listener.currentModule is not None

    # Get FIG from the module
    fig = module_listener.currentModule.FIG

    # Load the reference data
    ref_fig_data = REF_DATA_FIG_FOLDER.joinpath("dx15.dot")
    ref_graph = networkx.nx_agraph.read_dot(ref_fig_data)
    # Compare the reference data with the generated data and assert equality
    # Ref data load the dot file using networkx
    # Generated data load the dot file using pydot
    success = is_isomorphic(ref_graph, fig)
    assert success is True
