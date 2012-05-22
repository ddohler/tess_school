#!/bin/bash

LANG=kat

#for file in *.png; do
#	filename=$(basename $file)
#	filename=${filename%.*}
mv normproto $LANG.normproto
mv pffmtable $LANG.pffmtable
mv Microfeat $LANG.Microfeat
mv inttemp $LANG.inttemp
mv shapetable $LANG.shapetable
mv font_properties $LANG.font_properties
mv unicharset $LANG.unicharset

combine_tessdata $LANG.
#done
