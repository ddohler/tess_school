# -*- coding: utf-8 -*-
import cairo
import pango
import pangocairo
import sys
import codecs

WIDTH = 2550 # Assuming 300 dpi
HEIGHT = 3300
TXT_WIDTH = WIDTH - 300
TXT_HEIGHT = HEIGHT - 300
LINE_SPACE = 35

attrs = pango.AttrList()
attrs.insert(pango.AttrLanguage('ka',start_index=0,end_index=-1))
attrs.insert(pango.AttrStretch(pango.STRETCH_ULTRA_EXPANDED,start_index=0,end_index=-1))
attrs.insert(pango.AttrSize(48000,start_index=0,end_index=-1))
attrs.insert(pango.AttrFallback(False,start_index=0,end_index=-1))

surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
context = cairo.Context(surf)

#draw a background rectangle:
context.rectangle(0,0,WIDTH,HEIGHT)
context.set_source_rgb(1, 1, 1)
context.fill()

#get font families:

font_map = pangocairo.cairo_font_map_get_default()
families = font_map.list_families()

# to see family names:
print [f.get_name() for f in   font_map.list_families()]

#context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

# Translates context so that desired text upperleft corner is at 0,0
context.translate(50,25)

pangocairo_context = pangocairo.CairoContext(context)
pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

layout = pangocairo_context.create_layout()
fontname = sys.argv[1] if len(sys.argv) >= 2 else "Sans"
font = pango.FontDescription(fontname + " 25")
layout.set_attributes(attrs)
layout.set_font_description(font)
layout.set_width(TXT_WIDTH*pango.SCALE)
layout.set_spacing(LINE_SPACE*pango.SCALE)
print layout.get_width()

text = ''
with codecs.open("text.txt") as text_file:
    for line in text_file:
        text += line + '\n'
    
layout.set_text(text)
context.set_source_rgb(0, 0, 0)
pangocairo_context.update_layout(layout)
pangocairo_context.show_layout(layout)

with open("cairo_text.png", "wb") as image_file:
        surf.write_to_png(image_file)
