DEVICE dx14_ref

LAYER FLOW 

PORT port_in1, port_in2, port_in3 portRadius=2000;
MIXER mixer_in bendSpacing=600
numberOfBends=5
channelWidth=300
bendLength=2000
height=300;

CHANNEL channel_1 from port_in1 to mixer_in 1 channelWidth=300;
CHANNEL channel_2 from port_in2 to mixer_in 1 channelWidth=300;
CHANNEL channel_3 from port_in3 to mixer_in 1 channelWidth=300;

NOZZLE DROPLET GENERATOR nozzle_droplet_generator1 orificeSize=150
orificeLength=375
oilInputWidth=600
waterInputWidth=375
outputWidth=300
outputLength=5000
height=300;
NOZZLE DROPLET GENERATOR nozzle_droplet_generator2 orificeSize=150
orificeLength=375
oilInputWidth=600
waterInputWidth=375
outputWidth=300
outputLength=5000
height=300;

CHANNEL channel_mixed_1 from mixer_in 2 to nozzle_droplet_generator1 4 channelWidth=300;
CHANNEL channel_mixed_2 from mixer_in 2 to nozzle_droplet_generator2 4 channelWidth=300;

PORT port_oil1, port_oil2, port_oil3, port_oil4 portRadius=2000;
CHANNEL channel_oil1 from port_oil1 to nozzle_droplet_generator1 1 channelWidth=300;
CHANNEL channel_oil2 from port_oil2 to nozzle_droplet_generator1 3 channelWidth=300;
CHANNEL channel_oil3 from port_oil3 to nozzle_droplet_generator2 1 channelWidth=300;
CHANNEL channel_oil4 from port_oil4 to nozzle_droplet_generator2 3 channelWidth=300;

MIXER mixer_incubate1, mixer_incubate2 bendSpacing=600
numberOfBends=5
channelWidth=300
bendLength=2000
height=300;
CHANNEL channel_incubate1 from nozzle_droplet_generator1 2 to mixer_incubate1 1 channelWidth=300;
CHANNEL channel_incubate2 from nozzle_droplet_generator2 2 to mixer_incubate2 1 channelWidth=300;

DROPLET SORTER droplet_sorter1 height=300
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
pressureDepth=200 ;
CHANNEL channel_incubate3 from mixer_incubate1 1 to droplet_sorter1 1 channelWidth=300;
CHANNEL channel_incubate4 from mixer_incubate2 1 to droplet_sorter1 1 channelWidth=300;

PORT port_out1, port_out2 portRadius=2000;
CHANNEL channel_out1 from droplet_sorter1 2 to port_out1 channelWidth=300;
CHANNEL channel_out2 from droplet_sorter1 3 to port_out2 channelWidth=300;

END LAYER

