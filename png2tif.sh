#!/bin/bash

mogrify -density 300 -units PixelsPerInch -type TrueColor -format tif *.png
