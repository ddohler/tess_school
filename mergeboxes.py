#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TesseractBox import TesseractBox
from utils import parse_boxfile, separation_x, merge_two_boxes
import codecs
import optparse

def main():
    parser = optparse.OptionParser(usage="Usage: %prog [-t threshold] boxfile")
    parser.add_option('-t', '--threshold', dest='threshold', action='store',
                      type='int', default=1, help='Adjacent boxes separated horizontally by THRESHOLD or fewer pixels will be merged. Horizontal separation is ignored. Note that this means that boxes located on different lines might be merged in certain (rare) circumstances. Defaults to 1 (boxes are adjacent).')

    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      help="Also print statistics about number of boxes merged")
    (opts, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        return 0

    boxes = parse_boxfile(args[0])
    (merged,stats) = merge_nearby_boxes(opts,boxes)

    # Print new box file; user can redirect to file
    for box in merged:
        print unicode(box).encode('utf-8')

    if opts.verbose:
        print "Merged %d out of %d boxes. Outputting %d boxes." %(stats["num_merged"], stats["total_in"], stats["total_out"])

def merge_nearby_boxes(opts,boxes):
    """Merge boxes in the passed array of boxes which are both adjacent and
    separated by fewer pixels than the threshold given in opts.threshold.
    Outputs other boxes unchanged."""

    stats = {"total_in": 0,"total_out": 0, "num_merged": 0}

    stats["total_in"] = len(boxes)
    

    output = list()
    newbox = None
    while(len(boxes) > 0):
        pivot = boxes.pop(0)

        # Newbox is the result of all previous merge operations
        # In most cases, this is simply the previous pivot box.
        if newbox is not None:
            #Check horizontal separation
            if separation_x(newbox,pivot) <= opts.threshold:
                newbox = merge_two_boxes(newbox,pivot)
                stats["num_merged"] += 1
            #No merge, onto output list.
            else:
                output.append(newbox)
                newbox = pivot
        else:
            newbox = pivot

    #Loop cleanup: push the final box onto the output
    if newbox is not None:
        output.append(newbox)

    stats["total_out"] = len(output)
    return (output,stats)



# If program is run directly
if __name__ == "__main__":
    main()
