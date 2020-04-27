FLOW LAYER

PORT p_water_in_1, p_water_in_2 portRadius=2000;

DROPLET GENERATOR default_component;

CHANNEL c_in_1 from p_water_in_1 to default_component 2 width=400;
CHANNEL c_in_2 from p_water_in_2 to default_component 4 width=400;

END LAYER