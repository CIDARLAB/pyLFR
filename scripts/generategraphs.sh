#!/bin/sh


echo "Converting all the dot files to ps"

for f in ../out/*.dot;

do 
	echo "Running File $f";
    dot -Tpng $f -o $f.png
done 