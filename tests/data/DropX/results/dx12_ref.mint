DEVICE dx12_ref

LAYER FLOW 

PORT port_oil1 portRadius=2000;
PORT port_water1 portRadius=2000;
PORT port_oil2 portRadius=2000;
NOZZLE DROPLET GENERATOR nozzle_droplet_generator_1 
    orificeSize=150
    orificeLength=375
    oilInputWidth=600
    waterInputWidth=375
    outputWidth=300
    outputLength=5000
    height=300;

CHANNEL connection_1 from port_oil1 to nozzle_droplet_generator_1 1 channelWidth=300 channelWidth=300;
CHANNEL connection_2 from port_water1 to nozzle_droplet_generator_1 4 channelWidth=300 channelWidth=300;
CHANNEL connection_3 from port_oil2 to nozzle_droplet_generator_1 3 channelWidth=300 channelWidth=300;

PORT port_injector portRadius=2000;
PICOINJECTOR pico_injector_1
    height=300
    injectorWidth=1000
    width=10000
    injectorWidth=1000
    injectorLength=5000
    dropletWidth=100
    nozzleWidth=50
    nozzleLength=500
    electrodeDistance=500
    electrodeWidth=800
    electrodeLength=3000;

CHANNEL connection_4 from port_injector to pico_injector_1 3 channelWidth=300;
CHANNEL connection_5 from nozzle_droplet_generator_1 2 to pico_injector_1 1 channelWidth=300;

MIXER mixer_1
    bendSpacing=600
    numberOfBends=5
    channelWidth=300
    bendLength=2000
    height=300;

CHANNEL connection_6 from pico_injector_1 2 to mixer_1 1 channelWidth=300;

PORT port_out_waste portRadius=2000;
PORT port_out_keep portRadius=2000;
DROPLET SORTER droplet_sorter_1
    height=300
    inletWidth=300
    inletLength=4000
    inletLength=4000
    electrodeDistance=1000
    electrodeWidth=700
    electrodeLength=5000
    outletWidth=300
    angle=45
    wasteWidth=600
    outputLength=4000
    keepWidth=600
    pressureWidth=1000
    numberofDistributors=5
    channelDepth=300
    electrodeDepth=300
    pressureDepth=200;

CHANNEL connection_7 from mixer_1 2 to droplet_sorter_1 1 channelWidth=300;
CHANNEL connection_8 from droplet_sorter_1 2 to port_out_waste channelWidth=300;
CHANNEL connection_9 from droplet_sorter_1 3 to port_out_keep channelWidth=300;

END LAYER

