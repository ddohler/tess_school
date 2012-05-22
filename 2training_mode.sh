#!/bin/bash

LANG=kat

for file in *.tif; do
	filename=$(basename $file)
	filename=${filename%.*}
	tesseract $file $filename nobatch box.train.stderr
done
