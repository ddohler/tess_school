#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TesseractBox import TesseractBox
from utils import parse_boxfile, separation_x, merge_two_boxes
import codecs
import optparse

def main():
    parser = optparse.OptionParser(usage="Usage: %prog truthfile boxfile")

    (opts, args) = parser.parse_args()

    if len(args) != 2:
        parser.print_help()
        return 0

    boxes = parse_boxfile(args[1])
    glyphs = get_glyphs(args[0])

    if len(boxes) != len(glyphs):
        raise ValueError("Mismatch between number of boxes (%d) and number of glyphs (%d)." %(len(boxes),len(glyphs)))

    else:
        align_boxes(boxes,glyphs)

    for box in boxes:
        print unicode(box).encode('utf-8')

def get_glyphs(text_file):
    """Read a text file and return an array of non-whitespace characters."""
    glyphs = u''
    with codecs.open(text_file,mode='r',encoding='utf-8') as ifile:
        for line in ifile:
            glyphs += ''.join(line.split())

    return glyphs

def align_boxes(boxes,glyphs):
    """Changes the text of the boxes parameter to match the character in the glyphs parameter at the corresponding position. Assumes that the two arrays are the same length."""
    for i in range(len(glyphs)):
        boxes[i].set_text(glyphs[i])

# If program is run directly
if __name__ == "__main__":
    main()
