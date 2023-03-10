DEVICE dx3_ref

LAYER FLOW 

PORT port_oil1 portRadius=2000 ;
PORT port_oil2 portRadius=2000 ;
PORT port_water portRadius=2000 ;

NOZZLE DROPLET GENERATOR nozzle_droplet_generator_1 orificeSize=150 orificeLength=375 
    oilInputWidth=600 waterInputWidth=375 outputWidth=300 outputLength=5000 height=300 ;

CHANNEL connection_1 from port_oil1 to nozzle_droplet_generator_1 1 channelWidth=300 ;
CHANNEL connection_2 from port_oil2 to nozzle_droplet_generator_1 3 channelWidth=300 ;
CHANNEL connection_3 from port_water to nozzle_droplet_generator_1 4 channelWidth=300 ;

DROPLET SPLITTER droplet_splitter_1
    height=30
    inletWidth=300
    inletLength=2000
    outletWidth1=300
    outletLength1=2000
    outletWidth2=300
    outletLength2=2000;

PORT port_injector1 portRadius=2000 ;
PORT port_injector2 portRadius=2000 ;

PICOINJECTOR picoinjector_1 height=300
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

PICOINJECTOR picoinjector_2 height=300
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

CHANNEL connection_4 from nozzle_droplet_generator_1 2 to droplet_splitter_1 1 channelWidth=300 ;
CHANNEL connection_5 from droplet_splitter_1 2 to picoinjector_1 1 channelWidth=300 ;
CHANNEL connection_6 from droplet_splitter_1 3 to picoinjector_2 1 channelWidth=300 ;
CHANNEL connection_7 from port_injector1 to picoinjector_1 3 channelWidth=300 ;
CHANNEL connection_8 from port_injector2 to picoinjector_2 3 channelWidth=300 ;

PORT port_out1 portRadius=2000 ;
PORT port_out2 portRadius=2000 ;

CHANNEL connection_9 from picoinjector_1 2 to port_out1 1 channelWidth=300 ;
CHANNEL connection_10 from picoinjector_2 2 to port_out2 1 channelWidth=300 ;

END LAYER

