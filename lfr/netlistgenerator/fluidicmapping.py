from pymint.minttarget import MINTTarget
from pymint.mintcomponent import MINTComponent
from .mappinglibrary import MappingLibrary, Primitive
from lfr.fig.interaction import Interaction
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from pymint.mintdevice import MINTDevice
from typing import Optional


class FluidicMapping(object):

    def __init__(self, finteraction: Interaction, device_generator) -> None:
        if device_generator is None:
            raise Exception("Need to provide a default library")
        self.__library: MappingLibrary = device_generator.library
        self.__name_generator = device_generator.namegenerator
        self.__finteraction = finteraction
        self.__blacklist_map = device_generator.blacklist_map
        self.__primitive_map = device_generator.primitive_map

        self.technology: str = ''
        self.params = dict()

    def get_technology(self, finteraction: Interaction) -> Primitive:
        # TODO: Insert algorithm to figure which component would be the best fit for this scenario

        # Naive approach, pick the first component in the mapping library
        primitive = self.__library.get_operators(finteraction.interactionType)[0]
        return primitive

    def rewrite_target(self, old_target: MINTTarget, newtarget: str):
        return MINTTarget(newtarget, old_target.port)

    def stitch_component(self, component: MINTComponent, netlist: MINTDevice, default_netlist: MINTDevice):
        default_component = default_netlist.getComponent('default_component')
        new_old_component_map = dict()
        new_old_component_map['default_component'] = component.ID
        # Add all the components from
        for component in default_netlist.get_components():
            # Skip the default component
            if component == default_component:
                continue
            else:
                name = self.__name_generator.generate_name(component.entity)
                new_old_component_map[component.ID] = name
                netlist.addComponent(name, component.entity, component.params.data, '0')

        # Add connections from
        for connection in default_netlist.get_connections():
            name = self.__name_generator.generate_name(connection.entity)
            source_target = self.rewrite_target(connection.source, new_old_component_map[connection.source.component])
            sink_targets = [self.rewrite_target(t, new_old_component_map[t.component]) for t in connection.sinks]
            netlist.addConnection(name, connection.entity, connection.params.data, source_target, sink_targets, '0')

    def map(self, netlist: MINTDevice, fig: FluidInteractionGraph):
        # TODO: map the operator
        interaction_id = self.__finteraction.id
        primitive = self.get_technology(self.__finteraction)
        if interaction_id not in fig.G.nodes:
            raise Exception("Could not find interaction `{}` in fig".format(interaction_id))

        print("Found {} in FIG, constructing design now ...".format(interaction_id))

        # TODO: Pull the data of the default params from whereever

        # Add the component first into the netlist
        name = self.__name_generator.generate_name(primitive.mint)
        component = netlist.addComponent(name, primitive.mint, {}, '0')
        self.__blacklist_map[interaction_id] = name
        self.__primitive_map[interaction_id] = primitive

        # Stitch together the default netlist if it exists
        default_netlist = primitive.default_netlist
        if default_netlist is not None:
            print("Stitching component: {}".format(primitive.mint))
            self.stitch_component(component, netlist, default_netlist)
        # Create arcs to it's neighbours ?
        # inputs = fig.get_input_nodes(interaction_id)
        # for _input in inputs :
        #     if not netlist.componentExists(_input):
        #       Create create a temporary that connects them

            # Create the arcs

        # Check if inputs exist in
        # TODO: Connect the outputs to the component created

        # TODO:Connect the inputs to the component created
