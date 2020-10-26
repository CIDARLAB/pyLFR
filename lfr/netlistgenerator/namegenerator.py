from typing import Dict
from pymint import MINTConnection, MINTComponent, MINTDevice


class NameGenerator(object):

    def __init__(self) -> None:
        self.dictionary = dict()
        # Key - Old NAme, Value - new name
        self._cn_rename_map: Dict[str, Dict[str, str]] = dict()
        self._rename_map: Dict[str, str] = dict()

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

    def rename_cn_component(self, cn_id: str, component: MINTComponent) -> str:
        old_name = component.name
        new_name = self.generate_name(component.entity)
        # self._rename_map[old_name] = new_name
        self.store_cn_name(cn_id, old_name, new_name)
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

    def rename_cn_connection(self, cn_id: str, connection: MINTConnection) -> str:
        old_name = connection.name
        new_name = self.generate_name(connection.entity)
        # self._rename_map[old_name] = new_name
        self.store_cn_name(cn_id, old_name, new_name)
        connection.name = new_name
        connection.overwrite_id(new_name)

        # Rename source
        connection.source.component = self.get_cn_name(cn_id, connection.source.component)

        # Rename sinks
        for sink in connection.sinks:
            sink.component = self.get_cn_name(cn_id, sink.component)

        return new_name

    def rename_netlist(self, cn_id: str, device: MINTDevice) -> None:
        for component in device.components:
            self.rename_cn_component(cn_id, component)

        for connection in device.connections:
            self.rename_cn_connection(cn_id, connection)

    def store_name(self, old_name: str, new_name: str) -> None:
        if old_name in self._rename_map.keys():
            print("Warning! - Rewriting entry '{}'".format(old_name))
        self._rename_map[old_name] = new_name

    def get_name(self, old_name: str) -> str:
        return self._rename_map[old_name]

    def store_cn_name(self, cn_id: str, old_name: str, new_name: str) -> None:
        if cn_id not in self._cn_rename_map.keys():
            # Add entry if it isn't there
            self._cn_rename_map[cn_id] = dict()

        # Print a warning incase of rewrite
        if old_name in self._cn_rename_map[cn_id].keys():
            print("Warning! - Rewriting entry '{}' in Construction Node - {}".format(old_name, cn_id.id))
        self._cn_rename_map[cn_id][old_name] = new_name

    def get_cn_name(self, cn_id: str, old_name: str) -> str:
        return self._cn_rename_map[cn_id][old_name]
