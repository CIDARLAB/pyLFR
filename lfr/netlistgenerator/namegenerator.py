from pymint import MINTConnection, MINTComponent, MINTDevice


class NameGenerator(object):

    def __init__(self) -> None:
        self.dictionary = dict()
        # Key - Old NAme, Value - new name
        self._rename_map = dict()

    def generate_name(self, technology_string: str) -> str:
        if technology_string in self.dictionary.keys():
            # Increment the number in dictionary and return the name
            ret = self.dictionary[technology_string] + 1
            self.dictionary[technology_string] = ret
            return "{}_{}".format(technology_string, ret).lower().replace(" ", "_")
        else:
            self.dictionary[technology_string] = 1
            return "{}_{}".format(technology_string, 1).lower().replace(" ", "_")

    def rename_component(self, component: MINTComponent) -> str:
        old_name = component.name
        new_name = self.generate_name(component.entity)
        self._rename_map[old_name] = new_name
        component.name = new_name
        component.overwrite_id(new_name)
        return new_name

    def rename_connection(self, connection: MINTConnection) -> str:
        old_name = connection.name
        new_name = self.generate_name(connection.entity)
        self._rename_map[old_name] = new_name
        connection.name = new_name
        connection.overwrite_id(new_name)

        # Rename source
        connection.source.component = self._rename_map[connection.source.component]

        # Rename sinks
        for sink in connection.sinks:
            sink.component = self._rename_map[sink.component]

        return new_name

    def rename_netlist(self, device: MINTDevice) -> None:
        for component in device.components:
            self.rename_component(component)

        for connection in device.connections:
            self.rename_connection(connection)

