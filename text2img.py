# -*- coding: utf-8 -*-
import cairo
import pango
import pangocairo
import sys
import codecs
import optparse


def main():
    parser = optparse.OptionParser(usage="Usage: %prog [biu] font1...")
    parser.add_option('-b', '--bold', dest='bold', action='store_true',
                      help='Generate bold output, if supported by font.')
    parser.add_option('-i', '--italic',dest='italic',action='store_true',
                      help='Generate italic output, if supported by font.')
    parser.add_option('-u', '--underline',dest='underline',action='store_true',
                      help='Generate underline output, if supported by font.')

    (opts,args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        return 0
    
    generate_images(opts,args)

def generate_images(opts,args):
    # Set up variables for drawing space
    width = 2550 # Will resize to match text; default 8.5"x11" @ 300dpi
    height = 3300
    MARGIN_X = 300
    MARGIN_Y = 300
    LINE_SPACE = 35 #TODO: Command-line opts
    LANG = "ka"
    TESS_LANG = "kat"
    # Set up decent spacing for box files
    attrs = pango.AttrList() #TODO: Command line opts or config
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
    font_names = args
    #font_names = [
    #    "Sans",
    #    "Serif",
    #    "Monospace",
    #]

    # (variant, reset,"desc")
    #Font variants is an array of tuples consisting of: (AttrStyle, InverseAttrStyle, Name)
    font_variants = [
        (pango.AttrStyle(pango.STYLE_NORMAL,0,-1),pango.AttrStyle(pango.STYLE_NORMAL,0,-1),"")]

    #Add other stylings based on command-line options
    if opts.italic:
        font_variants.append((pango.AttrStyle(pango.STYLE_ITALIC,0,-1),pango.AttrStyle(pango.STYLE_NORMAL,0,-1),"italic"))
    if opts.bold:
        font_variants.append((pango.AttrWeight(pango.WEIGHT_HEAVY,0,-1),pango.AttrWeight(pango.WEIGHT_NORMAL,0,-1),"bold"))
    if opts.underline:
        font_variants.append((pango.AttrUnderline(pango.UNDERLINE_SINGLE,0,-1),pango.AttrUnderline(pango.UNDERLINE_NONE,0,-1),"underline"))

    #Generate pages for each font name and variation.
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

if __name__ == "__main__":
    main()
