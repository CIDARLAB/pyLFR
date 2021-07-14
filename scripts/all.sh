#!/bin/sh


echo "Synthesizing DropX designs"

for f in ~/CIDAR/LFR-Testcases/dropx/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/dropx/ --pre-load ~/CIDAR/LFR-Testcases/distribute-library
done  


echo "Synthesizing Cassie Thesis Designs"

for f in ~/CIDAR/LFR-Testcases/chthesis/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/chthesis/ --pre-load ~/CIDAR/LFR-Testcases/distribute-library
done  



echo "Synthesizing COVID"

for f in ~/CIDAR/LFR-Testcases/COVID/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/COVID/ --pre-load ~/CIDAR/LFR-Testcases/distribute-library
done  


echo "Synthesizing Expressions"

for f in ~/CIDAR/LFR-Testcases/Expressions/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/Expressions/ --pre-load ~/CIDAR/LFR-Testcases/distribute-library
done  

echo "Synthesizing ghissues"

for f in ~/CIDAR/LFR-Testcases/ghissues/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/ghissues/ --pre-load ~/CIDAR/LFR-Testcases/distribute-library
done  



echo "Synthesizing Graph Coverage"

for f in ~/CIDAR/LFR-Testcases/GraphCoverage/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/GraphCoverage/ --pre-load ~/CIDAR/LFR-Testcases/distribute-library
done  


echo "Synthesizing Parser Test"

for f in ~/CIDAR/LFR-Testcases/ParserTest/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/ParserTest/ --pre-load ~/CIDAR/LFR-Testcases/distribute-library
done  



echo "Synthesizing Protocols"

for f in ~/CIDAR/LFR-Testcases/Protocols/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/Protocols/ --pre-load ~/CIDAR/LFR-Testcases/distribute-library
done  


echo "Synthesizing Ryuichi's Designs"

for f in ~/CIDAR/LFR-Testcases/Ryuichi\'s\ designs/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/Ryuichi\'s\ designs/ --pre-load ~/CIDAR/LFR-Testcases/distribute-library
done 


echo "Synthesizing Technology Mapping"

for f in ~/CIDAR/LFR-Testcases/TechnologyMapping/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ~/CIDAR/LFR-Dry-Run/TechnologyMapping/ --pre-load ~/CIDAR/LFR-Testcases/distribute-library
done 

