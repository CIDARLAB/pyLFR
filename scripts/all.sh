#!/bin/sh


echo "Synthesizing DropX designs"

for f in ./Microfluidics-Benchmarks/LFR-Testcases/dropx/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ./Microfluidics-Benchmarks/LFR-Dry-Run/dropx/ --pre-load ./Microfluidics-Benchmarks/LFR-Testcases/distribute-library
done  


echo "Synthesizing Cassie Thesis Designs"

for f in ./Microfluidics-Benchmarks/LFR-Testcases/chthesis/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ./Microfluidics-Benchmarks/LFR-Dry-Run/chthesis/ --pre-load ./Microfluidics-Benchmarks/LFR-Testcases/distribute-library
done  



echo "Synthesizing COVID"

for f in ./Microfluidics-Benchmarks/LFR-Testcases/COVID/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ./Microfluidics-Benchmarks/LFR-Dry-Run/COVID/ --pre-load ./Microfluidics-Benchmarks/LFR-Testcases/distribute-library
done  


echo "Synthesizing Expressions"

for f in ./Microfluidics-Benchmarks/LFR-Testcases/Expressions/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ./Microfluidics-Benchmarks/LFR-Dry-Run/Expressions/ --pre-load ./Microfluidics-Benchmarks/LFR-Testcases/distribute-library
done  

echo "Synthesizing ghissues"

for f in ./Microfluidics-Benchmarks/LFR-Testcases/ghissues/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ./Microfluidics-Benchmarks/LFR-Dry-Run/ghissues/ --pre-load ./Microfluidics-Benchmarks/LFR-Testcases/distribute-library
done  



echo "Synthesizing Graph Coverage"

for f in ./Microfluidics-Benchmarks/LFR-Testcases/GraphCoverage/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ./Microfluidics-Benchmarks/LFR-Dry-Run/GraphCoverage/ --pre-load ./Microfluidics-Benchmarks/LFR-Testcases/distribute-library
done  


echo "Synthesizing Parser Test"

for f in ./Microfluidics-Benchmarks/LFR-Testcases/ParserTest/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ./Microfluidics-Benchmarks/LFR-Dry-Run/ParserTest/ --pre-load ./Microfluidics-Benchmarks/LFR-Testcases/distribute-library
done  



echo "Synthesizing Protocols"

for f in ./Microfluidics-Benchmarks/LFR-Testcases/Protocols/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ./Microfluidics-Benchmarks/LFR-Dry-Run/Protocols/ --pre-load ./Microfluidics-Benchmarks/LFR-Testcases/distribute-library
done  


echo "Synthesizing Ryuichi's Designs"

for f in ./Microfluidics-Benchmarks/LFR-Testcases/Ryuichi\'s\ designs/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ./Microfluidics-Benchmarks/LFR-Dry-Run/Ryuichi\'s\ designs/ --pre-load ./Microfluidics-Benchmarks/LFR-Testcases/distribute-library
done 


echo "Synthesizing Technology Mapping"

for f in ./Microfluidics-Benchmarks/LFR-Testcases/TechnologyMapping/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --no-gen --outpath ./Microfluidics-Benchmarks/LFR-Dry-Run/TechnologyMapping/ --pre-load ./Microfluidics-Benchmarks/LFR-Testcases/distribute-library
done 

