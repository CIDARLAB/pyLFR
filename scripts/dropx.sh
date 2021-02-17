#!/bin/sh


echo "Synthesizing DropX designs"

for f in ~/CIDAR/LFR-Testcases/dropx/*.lfr;

do 
	echo "Running File $f";
    lfr-compile $f --outpath ~/CIDAR/MINT-TestCases/dropx/
done  