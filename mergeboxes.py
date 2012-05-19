#!/usr/bin/env python
# -*- coding: utf-8 -*-

from moshpytt import TesseractBox
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

    boxes = parse_boxfile(args)
    (merged,stats) = merge_nearby_boxes(opts,boxes)

    # Print new box file; user can redirect to file
    for box in merged:
        print box

    if opts.verbose:
        print "Merged %d out of %d boxes. Outputting %d boxes." %(stats["num_merged"], stats["total_in"], stats["total_out"])

def parse_boxfile(args):
    """Read in a boxfile, return an array of TesseractBox objects"""

    ifile = codecs.open(args[0],mode='r',encoding='utf-8')
    boxes = list()

    for line in ifile:
        boxes.append(TesseractBox(line))

    return boxes

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

def merge_two_boxes(box1,box2):
    merged = TesseractBox()

    if box1.page != box2.page:
        raise ValueError("Can't merge boxes on different pages.")

    merged.left     = min(box1.left,box2.left)
    merged.right    = max(box1.right,box2.right)
    merged.bottom   = min(box1.bottom,box2.bottom)
    merged.top      = max(box1.top,box2.top)

    merged.page = box1.page
    merged.text = box1.text + box2.text

    merged.valid = True
    #Ignore italic, uline, and bold -- they are meaningless to merged
    #boxes, so leave them false.
    return merged

def separation_x(box1,box2):
    """Return the horizontal separation of the boxes."""
    # We don't know which is left and which is right, so calc both and return
    # the smallest value, which will be the inside separation.
    sep1 = abs(box1.right - box2.left)
    sep2 = abs(box2.right - box1.left)
    
    return min(sep1,sep2)

def separation_y(box1,box2):
    """Return the vertical separation of the boxes."""
    sep1 = abs(box1.top - box2.bottom)
    sep2 = abs(box2.top - box1.bottom)

    return min(sep1,sep2)

# If program is run directly
if __name__ == "__main__":
    main()
