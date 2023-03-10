DEVICE dx6_ref

LAYER FLOW 

PORT port_in1 portRadius=2000;
PORT port_in2 portRadius=2000;
MIXER mixer_1 
    bendSpacing=600
    numberOfBends=5
    channelWidth=300
    bendLength=2000
    height=300;

CHANNEL connection_1 from port_in1 to mixer_1 1 channelWidth=300;
CHANNEL connection_2 from port_in2 to mixer_1 1 channelWidth=300;

PORT port_oil1 portRadius=2000;
PORT port_oil2 portRadius=2000;

NOZZLE DROPLET GENERATOR nozzle_droplet_generator_1
    orificeSize=150
    orificeLength=375
    oilInputWidth=600
    waterInputWidth=375
    outputWidth=300
    outputLength=5000
    height=300;

CHANNEL connection_3 from port_oil1 to nozzle_droplet_generator_1 1 channelWidth=300;
CHANNEL connection_4 from port_oil2 to nozzle_droplet_generator_1 3 channelWidth=300;
CHANNEL connection_5 from mixer_1 2 to nozzle_droplet_generator_1 4 channelWidth=300;

DROPLET SPLITTER droplet_splitter_1
    height=30
    inletWidth=300
    inletLength=2000
    outletWidth1=300
    outletLength1=2000
    outletWidth2=300
    outletLength2=2000;

CHANNEL connection_6 from nozzle_droplet_generator_1 2 to droplet_splitter_1 1 channelWidth=300;

PORT port_out1 portRadius=2000;
PORT port_out2 portRadius=2000;

CHANNEL connection_7 from droplet_splitter_1 2 to port_out1 channelWidth=300;
CHANNEL connection_8 from droplet_splitter_1 3 to port_out2 channelWidth=300;

END LAYER

