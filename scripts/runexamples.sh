#!/bin/sh


echo "Testing all the files"

for f in $1/*.lfr;

do 
	echo "Running File $f";
    python ../cmdline.py --outpath ../out/ $f
done  