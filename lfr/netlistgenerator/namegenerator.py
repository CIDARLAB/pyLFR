from typing import Dict

from parchmint import Component, Connection

from pymint import MINTDevice


class NameGenerator:
    """Helps Generate new names

    Has a dictionary and helper functions that help user to to generate new
    names and keeps track of the new new names being generated for specific
    MINT technology strings.

    Has a whole bunch of functions that will let the user rename all the
    components in a device.
    """

    def __init__(self) -> None:
        self._counter_dictionary = {}
        # Key - Old NAme, Value - new name
        self._cn_rename_map: Dict[str, Dict[str, str]] = {}
        self._rename_map: Dict[str, str] = {}

    def generate_name(self, technology_string: str) -> str:
        """Generates a new name for the given technology string

        Use this function when you need to generate new names
        for components.

        Eg. for args: MIXER -> output mixer_1

        Args:
            technology_string (str): MINT Technology type to generate names

        Returns:
            str: [description]
        """
        if technology_string in self._counter_dictionary.keys():
            # Increment the number in dictionary and return the name
            ret = self._counter_dictionary[technology_string] + 1
            self._counter_dictionary[technology_string] = ret
            return "{}_{}".format(technology_string, ret).lower().replace(" ", "_")
        else:
            self._counter_dictionary[technology_string] = 1
            return "{}_{}".format(technology_string, 1).lower().replace(" ", "_")

    def rename_component(self, component: Component) -> str:
        """Renames the component

        Renames the component and stores the old name->new name reference in
        internal datastructure

        NOTE - Renames the ID of the component too

        Args:
            component (Component): Component we want to rename

        Returns:
            str: Returns the new name for the component
        """
        old_name = component.name
        new_name = self.generate_name(component.entity)
        self._rename_map[old_name] = new_name
        component.name = new_name
        component.ID = new_name
        return new_name

    def rename_cn_component(self, cn_id: str, component: Component) -> str:
        """Renames the Construction Node related component

        Also stores what the corresponding rename map against the construction
        node id

        Args:
            cn_id (str): ConstructionNode ID
            component (Component): Component we want to rename

        Returns:
            str: New name of the component
        """
        old_name = component.name
        new_name = self.generate_name(component.entity)
        # self._rename_map[old_name] = new_name
        self.store_cn_name(cn_id, old_name, new_name)
        component.name = new_name
        component.ID = new_name
        return new_name

    def rename_connection(self, connection: Connection) -> str:
        """Renames the connection

        Also renames the name of the components in the source/sink(s)
        that the connection is referring to.

        Keeps track of the rename in internal datastruction

        Args:
            connection (Connection): Connection we want to rename

        Returns:
            str: New name of the connection
        """
        old_name = connection.name
        if old_name is None:
            raise ValueError()
        if connection.entity is None:
            raise ValueError()
        new_name = self.generate_name(connection.entity)
        self._rename_map[old_name] = new_name
        connection.name = new_name
        connection.ID = new_name

        # Check if Source is none
        if connection.source is None:
            raise ValueError("Source of connection {} is None".format(connection.ID))
        # Rename source
        connection.source.component = self._rename_map[connection.source.component]

        # Rename sinks
        for sink in connection.sinks:
            sink.component = self._rename_map[sink.component]

        return new_name

    def rename_cn_connection(self, cn_id: str, connection: Connection) -> str:
        """Renames connection with reference to construciton node

        Uses the internal data struction to save the
        rename map against the construciton node id.

        Args:
            cn_id (str): ConstructionNode ID
            connection (Connection): Connection we need to rename

        Returns:
            str: New name of the connection
        """
        old_name = connection.name
        if old_name is None:
            raise ValueError()
        if connection.entity is None:
            raise ValueError()
        new_name = self.generate_name(connection.entity)
        # self._rename_map[old_name] = new_name
        self.store_cn_name(cn_id, old_name, new_name)
        connection.name = new_name
        connection.ID = new_name

        # Check if Source is none
        if connection.source is None:
            raise ValueError("Source of connection {} is None".format(connection.ID))
        # Rename source
        connection.source.component = self.get_cn_name(
            cn_id, connection.source.component
        )

        # Rename sinks
        for sink in connection.sinks:
            sink.component = self.get_cn_name(cn_id, sink.component)

        return new_name

    def rename_netlist(self, cn_id: str, mint_device: MINTDevice) -> None:
        """Renames the entire netlist corresponding to a ConstructionNode

        Calls upon all the different rename component, connection
        methods to rename the entire netlist.

        Args:
            cn_id (str): ConstructionNode Id
            device (MINTDevice): Device we want to rename
        """
        for component in mint_device.device.components:
            self.rename_cn_component(cn_id, component)

        for connection in mint_device.device.connections:
            self.rename_cn_connection(cn_id, connection)

    def store_name(self, old_name: str, new_name: str) -> None:
        """Stores the name in internal datastructure

        Args:
            old_name (str): Old Name
            new_name (str): New Name
        """
        if old_name in self._rename_map.keys():
            print("Warning! - Rewriting entry '{}'".format(old_name))
        self._rename_map[old_name] = new_name

    def get_name(self, old_name: str) -> str:
        """Gets the new name of the component from internal datastructure

        Args:
            old_name (str): old name

        Returns:
            str: new name
        """
        return self._rename_map[old_name]

    def store_cn_name(self, cn_id: str, old_name: str, new_name: str) -> None:
        """Stores construction node id, rename map in internal datastructure

        Args:
            cn_id (str): ConstructionNode Id
            old_name (str): old name
            new_name (str): new name
        """
        if cn_id not in self._cn_rename_map.keys():
            # Add entry if it isn't there
            self._cn_rename_map[cn_id] = {}

        # Print a warning incase of rewrite
        if old_name in self._cn_rename_map[cn_id].keys():
            print(
                "Warning! - Rewriting entry '{}' in Construction Node - {}".format(
                    old_name, cn_id
                )
            )
        self._cn_rename_map[cn_id][old_name] = new_name

    def get_cn_name(self, cn_id: str, old_name: str) -> str:
        """Gets the new name for corresponding ConstructionNode id and old name

        Args:
            cn_id (str): ConstructionNode ID
            old_name (str): old name

        Returns:
            str: new name
        """
        return self._cn_rename_map[cn_id][old_name]
