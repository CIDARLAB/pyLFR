from typing import List, Optional


class ConnectingOption:
    def __init__(
        self,
        component_name: Optional[str] = None,
        component_port: Optional[List[Optional[str]]] = None,
        fig_nodes: Optional[List[str]] = None,
    ) -> None:
        if component_port is None:
            component_port = []
        self._component_name: Optional[str] = component_name
        self._component_port: List[Optional[str]] = component_port
        # FIG nodes this option belongs to (YTREE/TREE leaf identity).
        self._fig_nodes: List[str] = list(fig_nodes or [])

    @property
    def component_name(self) -> Optional[str]:
        return self._component_name

    @property
    def component_port(self) -> List[Optional[str]]:
        return self._component_port

    @property
    def fig_nodes(self) -> List[str]:
        return self._fig_nodes
