#!/bin/bash

LANG=kat

#for file in *.png; do
#	filename=$(basename $file)
#	filename=${filename%.*}
cp normproto $LANG.normproto
cp pffmtable $LANG.pffmtable
cp Microfeat $LANG.Microfeat
cp inttemp $LANG.inttemp
cp shapetable $LANG.shapetable
cp font_properties $LANG.font_properties
cp unicharset $LANG.unicharset

combine_tessdata $LANG.
#done
