#!/bin/bash

LANG=kat

#for file in *.png; do
#	filename=$(basename $file)
#	filename=${filename%.*}
	mftraining -F font_properties -U unicharset -O $LANG.unicharset *.tr
	cntraining *.tr
#done
