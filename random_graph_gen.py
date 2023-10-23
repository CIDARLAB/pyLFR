import networkx as nx
from lfr import utils
from lfr.fig.fignode import Flow, IONode
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.fig.interaction import FluidFluidInteraction, FluidProcessInteraction, Interaction, InteractionType
import random


G = nx.gnr_graph(8, 0.3)
FG = FluidInteractionGraph()


topo_sort = nx.topological_sort(G)
# print(list(topo_sort))
flow_list = []
type_list = list(InteractionType)

node_list = [node for node in G.nodes if G.in_edges(node) == 0]
print(node_list)

print(list(G))

for node in G:
    if G.pred[node] != {}:
        # if random.randrange(2) == 1:
        #     fig_to_add = Interaction(node, type_list[random.randrange(len(type_list))])
        fig_to_add = Flow(node)

    
    else: 
        fig_to_add = IONode(node)

    print(type(fig_to_add))
    FG.add_fignode(fig_to_add)
    flow_list.append(fig_to_add)


# print(list(G))

# for new_node in G:
#     # if new_node.pred[new_node]
#     new_temp_flow = Flow(new_node) if G.pred[node]
#     FG.add_fignode(new_temp_flow)



for fnode in G:
    if len(G.pred[fnode]) >= 2:
        print(random.randrange(2))
        if random.randrange(2) == 1:
            store_vals = [Flow(x) for x in list(G.pred[fnode])]
            print("trig")
            for i in range(len(store_vals)-1):
                ffint = FluidFluidInteraction(store_vals[i], store_vals[i+1], type_list[random.randrange(len(type_list))])
                flow_list[store_vals[i].ID] = ffint
                flow_list[store_vals[i+1].ID] = ffint
                FG.add_interaction(ffint)

for source, sink in G.edges():
    FG.connect_fignodes(flow_list[source], flow_list[sink])

print(list(FG))

print(G.in_edges())

utils.printgraph(FG, "fg.dot")

