#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tesseract3Box import Tesseract3Box
from utils import parse_boxfile, separation_x, merge_two_boxes
import codecs
import optparse

def main():
    parser = optparse.OptionParser(usage="Usage: %prog [-o outfile] truthfile boxfile")
    parser.add_option('-o', '--output', dest='output', action='store',
                      type='str', default='aligned.box', help='Output file. Overwrites existing files with no warning.')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      help="Print shifted lines as they are encountered and metrics about the number of lines affected.")
    (opts, args) = parser.parse_args()

    if len(args) != 2:
        parser.print_help()
        return 0

    boxes = parse_boxfile(args[1])
    glyphs = get_glyphs(args[0])

    if len(boxes) != len(glyphs):
        raise ValueError("Mismatch between number of boxes (%d) and number of glyphs (%d)." %(len(boxes),len(glyphs)))

    else:
        align_boxes(boxes,glyphs,opts.verbose)

    with codecs.open(opts.output,mode='wb',encoding='utf-8') as outfile:
        for box in boxes:
            outfile.write(unicode(box)+u'\n')

def get_glyphs(text_file):
    """Read a text file and return an array of non-whitespace characters."""
    glyphs = u''
    with codecs.open(text_file,mode='r',encoding='utf-8') as ifile:
        for line in ifile:
            glyphs += ''.join(line.split())

    return glyphs

def align_boxes(boxes,glyphs,verbose=False):
    """Changes the text of the boxes parameter to match the character in the glyphs parameter at the corresponding position. Assumes that the two arrays are the same length."""
    count = 0
    for i in range(len(glyphs)):
        if boxes[i].text != glyphs[i]:
            count += 1
            if verbose:
                print "%d: %s > %s" %(i,boxes[i].text,glyphs[i])
            boxes[i].set_text(glyphs[i])

    if verbose:
        print "Total: %d" %(count)

# If program is run directly
if __name__ == "__main__":
    main()
