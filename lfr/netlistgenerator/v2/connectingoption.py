from typing import List, Optional


class ConnectingOption:
    def __init__(
        self,
        component_name: Optional[str] = None,
        component_port: List[Optional[str]] = None,
    ) -> None:
        if component_port is None:
            component_port = []
        self._component_name: Optional[str] = component_name
        self._component_port: List[Optional[str]] = component_port

    @property
    def component_name(self) -> Optional[str]:
        return self._component_name

    @property
    def component_port(self) -> List[Optional[str]]:
        return self._component_port
