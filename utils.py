from TesseractBox import TesseractBox
import codecs

def parse_boxfile(args):
    """Read in a boxfile, return an array of TesseractBox objects"""

    ifile = codecs.open(args[0],mode='r',encoding='utf-8')
    boxes = list()

    for line in ifile:
        boxes.append(TesseractBox(line))

    return boxes

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
