#!/bin/bash

LANG=kat

for file in *.png; do
	filename=$(basename $file)
	filename=${filename%.*}
	tesseract $file $filename -l $LANG batch.nochop makebox
done
