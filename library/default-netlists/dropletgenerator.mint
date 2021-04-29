DEVICE dropletgenerator

LAYER FLOW

PORT p_oil_in_1, p_oil_in_2 portRadius=2000;

NOZZLE DROPLET GENERATOR default_component;

CHANNEL c_in_1 from p_oil_in_1 to default_component 2 channelWidth=400;
CHANNEL c_in_2 from p_oil_in_2 to default_component 4 channelWidth=400;

END LAYER