from typing import List, Optional


class ConnectingOption(object):
    def __init__(
        self,
        component_name: str = None,
        component_port: List[int] = [],
    ) -> None:
        self._component_name: str = component_name
        self._component_port: List[int] = component_port

    @property
    def component_name(self) -> Optional[str]:
        return self._component_name

    @property
    def component_port(self) -> List[int]:
        return self._component_port
