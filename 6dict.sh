#!/bin/bash

LANG=kat

#for file in *.png; do
#	filename=$(basename $file)
#	filename=${filename%.*}
wordlist2dawg frequent_words_list $LANG.freq-dawg $LANG.unicharset
wordlist2dawg words_list $LANG.word-dawg $LANG.unicharset
#done
