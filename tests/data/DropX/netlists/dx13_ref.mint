DEVICE dx13_ref

LAYER FLOW 

PORT port_oil1, port_oil2, port_water1 portRadius=2000;
NOZZLE DROPLET GENERATOR nozzle_droplet_generator_1 orificeSize=150
orificeLength=375
oilInputWidth=600
waterInputWidth=375
outputWidth=300
outputLength=5000
height=300;

CHANNEL c1 from port_oil1 to nozzle_droplet_generator_1 1 channelWidth=300;
CHANNEL c2 from port_oil2 to nozzle_droplet_generator_1 3 channelWidth=300;
CHANNEL c3 from port_water1 to nozzle_droplet_generator_1 4 channelWidth=300;

MIXER mixer_1 bendSpacing=600
numberOfBends=5
channelWidth=300
bendLength=2000
height=300
;

CHANNEL c4 from nozzle_droplet_generator_1 to mixer_1 1 channelWidth=300;

PORT port_injector1 portRadius=2000;
PICOINJECTOR pico_injector_1 height=300
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

CHANNEL c5 from port_injector1 to pico_injector_1 3 channelWidth=300;

CHANNEL c6 from mixer_1 2 to pico_injector_1 1 channelWidth=300;

MIXER mixer_2 bendSpacing=600
numberOfBends=5
channelWidth=300
bendLength=2000
height=300
;

CHANNEL c7 from pico_injector_1 2 to mixer_2 1 channelWidth=300 channelWidth=300;

PORT port_waste1 portRadius=2000;
DROPLET SORTER droplet_sorter_1 height=300
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

CHANNEL c11 from droplet_sorter_1 2 to port_waste1 channelWidth=300;

CHANNEL c8 from mixer_2 2 to droplet_sorter_1 1 channelWidth=300;

PORT port_injector2 portRadius=2000;
PICOINJECTOR pico_injector_2 height=300
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

CHANNEL c9 from port_injector2 to pico_injector_2 3 channelWidth=300;
CHANNEL c10 from droplet_sorter_1 3 to pico_injector_2 1 channelWidth=300;

MIXER mixer_3 bendSpacing=600
numberOfBends=5
channelWidth=300
bendLength=2000
height=300
;

CHANNEL c10 from pico_injector_2 2 to mixer_3 1 channelWidth=300;

PORT port_waste2 portRadius=2000;
DROPLET SORTER droplet_sorter_2 height=300
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

CHANNEL c12 from mixer_3 2 to  droplet_sorter_2 1 channelWidth=300;
CHANNEL c13 from droplet_sorter_2 2 to port_waste2 channelWidth=300;

DROPLET SPLITTER droplet_splitter_1 height=30
inletWidth=300
inletLength=2000
outletWidth1=300
outletLength1=2000
outletWidth2=300
outletLength2=2000;
CHANNEL c14 from droplet_sorter_2 3 to droplet_splitter_1 1 channelWidth=300;

PORT port_out1, port_out2 portRadius=2000;
CHANNEL c15 from droplet_splitter_1 2 to port_out1 channelWidth=300;
CHANNEL c16 from droplet_splitter_1 3 to port_out2 channelWidth=300 channelWidth=300;


END LAYER

