import networkx as nx
from pymint import MINTDevice

from lfr.netlistgenerator import primitive
from lfr.netlistgenerator.constructiongraph.constructiongraph import \
    ConstructionGraph
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.primitive import PrimitiveType


def generate_device(
    construction_graph: ConstructionGraph,
    scaffhold_device: MINTDevice,
    name_generator: NameGenerator,
) -> None:
    # TODO - Generate the device
    # Step 1 - go though each of the construction nodes and genrate the corresponding
    # components
    # Step 2 - generate the connections between the outputs to input on the connected
    # construction nodes
    # Step 3 - TODO - Generate the control network

    cn_component_mapping = {}

    node_ids = nx.dfs_preorder_nodes(construction_graph)
    print("Nodes to Traverse:", node_ids)

    # Go through the ordered nodes and start creating the components and connecitons
    for node_id in node_ids:
        cn = construction_graph.get_construction_node(node_id)

        # raise and error if the construction node has no primitive
        if cn.primitive is None:
            raise Exception("Construction Node has no primitive")

        # Generate the netlist based on the primitive type
        if cn.primitive.type is PrimitiveType.COMPONENT:
            # Generate the component
            component = cn.primitive.get_default_component(
                name_generator, scaffhold_device.device.layers[0]
            )

            # Add to the scaffhold device
            scaffhold_device.device.add_component(component)

            # Add to the component mapping
            cn_component_mapping[node_id] = component.ID

        elif cn.primitive.type is PrimitiveType.NETLIST:
            netlist = cn.primitive.get_default_netlist(cn.ID, name_generator)

    pass
