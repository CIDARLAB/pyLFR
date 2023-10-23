DEVICE dx15_ref

LAYER FLOW 

PORT port_in1, port_in2, port_in3 portRadius=2000 ;

MIXER mixer1 bendSpacing=600
numberOfBends=5
channelWidth=300
bendLength=2000
height=300 ;

CHANNEL c1 from port_in1 to mixer1 1 channelWidth=300 ;
CHANNEL c2 from port_in2 to mixer1 1 channelWidth=300 ;
CHANNEL c3 from port_in3 to mixer1 1 channelWidth=300 ;

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
pressureDepth=200;

CHANNEL c4 from mixer1 2 to droplet_sorter1 1 channelWidth=300;

PORT port_out_keep, port_out_waste portRadius=2000;

CHANNEL c5 from droplet_sorter1 3 to port_out_keep 1 channelWidth=300;
CHANNEL c6 from droplet_sorter1 2 to port_out_waste 1 channelWidth=300;

END LAYER

