# -*- coding: utf-8 -*-
import cairo
import pango
import pangocairo
import sys
import codecs

width = 2550 # Will resize to match text; default 8.5"x11" @ 300dpi
height = 3300
MARGIN_X = 300
MARGIN_Y = 300
LINE_SPACE = 35 #TODO: Command-line opts
LANG = "ka"
TESS_LANG = "kat"

# Set up decent spacing for box files
attrs = pango.AttrList() #TODO: Command line opts
attrs.insert(pango.AttrLanguage(LANG,0,-1))
attrs.insert(pango.AttrLetterSpacing(10000,0,-1))
attrs.insert(pango.AttrSize(48000,0,-1))
attrs.insert(pango.AttrFallback(False,0,-1))
attrs.insert(pango.AttrStyle(pango.STYLE_NORMAL,0,-1))
attrs.insert(pango.AttrWeight(pango.WEIGHT_NORMAL,0,-1))
attrs.insert(pango.AttrUnderline(pango.UNDERLINE_NONE,0,-1))

# Instantiate Cairo surface and context
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
context = pangocairo.CairoContext(cairo.Context(surf))

# Instantiate PangoCairo context
context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

#get font families:
font_map = pangocairo.cairo_font_map_get_default()

# to see family names:
#print [f.get_name() for f in font_map.list_families()]

# Select font
#fontname = sys.argv[1] if len(sys.argv) >= 2 else "Sans"

# Set up pango layout
layout = context.create_layout()
layout.set_attributes(attrs)
layout.set_width((width+MARGIN_X)*pango.SCALE)
layout.set_spacing(LINE_SPACE*pango.SCALE)

#print layout.get_width()

# Read text from file TODO: Command line argument
# TODO: Multiple files print to multiple image documents
text = ''
with codecs.open("text.txt") as text_file:
    for line in text_file:
        text += line + '\n'

#TODO: Construct from command-line options
font_names = [
    "Sans",
    "Serif",
    "Monospace",
]

# (variant, reset,"desc")
#TODO construct from command-line options
font_variants = [
    (pango.AttrStyle(pango.STYLE_NORMAL,0,-1),pango.AttrStyle(pango.STYLE_NORMAL,0,-1),""),
    #(pango.AttrStyle(pango.STYLE_OBLIQUE,0,-1),pango.AttrStyle(pango.STYLE_NORMAL,0,-1),"oblique"),
    (pango.AttrStyle(pango.STYLE_ITALIC,0,-1),pango.AttrStyle(pango.STYLE_NORMAL,0,-1),"italic"),
    (pango.AttrWeight(pango.WEIGHT_HEAVY,0,-1),pango.AttrWeight(pango.WEIGHT_NORMAL,0,-1),"bold"),
    (pango.AttrUnderline(pango.UNDERLINE_SINGLE,0,-1),pango.AttrUnderline(pango.UNDERLINE_NONE,0,-1),"underline"),
]

for fn in font_names:
    for fvar in font_variants:
        # Change to a new variant
        attrs.change(fvar[0])
        layout.set_attributes(attrs)

        # Change to a new font
        fontname = fn
        font = pango.FontDescription(fontname + " 25")
        
        layout.set_font_description(font)
        layout.set_text(text)

        (ink, logical) = layout.get_pixel_extents()

        # If layout exceeds size of surface, change surface size
        if logical[2] > (width-MARGIN_X) or logical[3] > (height-MARGIN_Y):
            width = logical[2]+MARGIN_X
            height = logical[3]+MARGIN_Y
            surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
            context = pangocairo.CairoContext(cairo.Context(surf))
            context.update_layout(layout)

        #draw a background rectangle:
        context.rectangle(0,0,width,height)
        context.set_source_rgb(1, 1, 1)
        context.fill()

        # Translate context so that desired text upperleft corner is at 0,0
        context.translate(50,25)
        context.set_source_rgb(0, 0, 0)

        context.update_layout(layout)
        context.show_layout(layout)

        # Write to image 
        # TODO: Specify outfile on command line
        #print fontname
        #print fvar[2]
        with open(TESS_LANG+"."+fontname+fvar[2]+".exp0.png", "wb") as image_file:
                surf.write_to_png(image_file)

        attrs.change(fvar[1])
        layout.set_attributes(attrs)
