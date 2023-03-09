#!/bin/sh


echo "Synthesizing DropX designs"

for f in ./Microfluidics-Benchmarks/LFR-Testcases/dropx/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --outpath ./Microfluidics-Benchmarks/MINT-TestCases/dropx/
done  