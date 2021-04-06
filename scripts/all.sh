#!/bin/sh


echo "Synthesizing DropX designs"

for f in ~/CIDAR/LFR-Testcases/dropx/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/dropx/
done  


echo "Synthesizing Cassie Thesis Designs"

for f in ~/CIDAR/LFR-Testcases/chthesis/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/chthesis/
done  



echo "Synthesizing COVID"

for f in ~/CIDAR/LFR-Testcases/COVID/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/COVID/
done  


echo "Synthesizing Expressions"

for f in ~/CIDAR/LFR-Testcases/Expressions/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/Expressions/
done  

echo "Synthesizing ghissues"

for f in ~/CIDAR/LFR-Testcases/ghissues/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/ghissues/
done  



echo "Synthesizing Graph Coverage"

for f in ~/CIDAR/LFR-Testcases/GraphCoverage/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/GraphCoverage/
done  


echo "Synthesizing Parser Test"

for f in ~/CIDAR/LFR-Testcases/ParserTest/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/ParserTest/
done  



echo "Synthesizing Protocols"

for f in ~/CIDAR/LFR-Testcases/Protocols/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/Protocols/
done  


echo "Synthesizing Ryuichi's Designs"

for f in ~/CIDAR/LFR-Testcases/Ryuichi\'s\ designs/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/Ryuichi\'s\ designs/
done 


echo "Synthesizing Technology Mapping"

for f in ~/CIDAR/LFR-Testcases/TechnologyMapping/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/TechnologyMapping/
done 

