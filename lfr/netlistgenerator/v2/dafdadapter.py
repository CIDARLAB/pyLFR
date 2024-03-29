from typing import List

from pymint.mintcomponent import MINTComponent
from pymint.mintdevice import MINTDevice

from lfr.postprocessor.constraints import Constraint


class DAFDAdapter:
    def __init__(self, device: MINTDevice) -> None:
        super().__init__()
        self._device = device

    def size_droplet_generator(
        self, component: MINTComponent, constriants: List[Constraint]
    ) -> None:
        import faulthandler

        faulthandler.enable()

        from dafd import DAFD_Interface

        self.solver = DAFD_Interface()
        # TODO: Check the type of the component and pull info from DAFD Interface
        targets_dict = {}
        constriants_dict = {}

        for constraint in constriants:
            if constraint.key == "volume":
                # r≈0.62035V1/3
                volume = constraint.get_target_value()
                targets_dict["droplet_size"] = float(volume) ** 0.33 * 0.62035 * 2
            elif constraint.key == "generation_rate":
                generate_rate = constraint.get_target_value()
                targets_dict["generation_rate"] = generate_rate
            else:
                raise Exception("Error: Geometry constraint not defined")

        results = self.solver.runInterp(targets_dict, constriants_dict)
        if component is None:
            raise Exception("No component attached to the constraints")

        orifice_size = results["orifice_size"]
        aspect_ratio = results["aspect_ratio"]
        capillary_number = results["capillary_number"]
        expansion_ratio = results["expansion_ratio"]
        flow_rate_ratio = results["flow_rate_ratio"]
        normalized_oil_inlet = results["normalized_oil_inlet"]
        normalized_orifice_length = results["normalized_orifice_length"]
        normalized_water_inlet = results["normalized_water_inlet"]

        component.params.set_param("orificeSize", round(orifice_size))
        component.params.set_param(
            "orificeLength", round(orifice_size * normalized_orifice_length)
        )
        component.params.set_param(
            "oilInputWidth", round(orifice_size * normalized_oil_inlet)
        )
        component.params.set_param(
            "waterInputWidth", round(orifice_size * normalized_water_inlet)
        )
        component.params.set_param("outputWidth", round(orifice_size * expansion_ratio))
        component.params.set_param("outputLength", 5000)
        component.params.set_param("height", round(orifice_size / aspect_ratio))
