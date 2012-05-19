class TesseractBox:

    text = u''

    left = None
    right = None
    top = None
    bottom = None

    page = None

    italic = False
    uline = False
    bold = False

    valid = False # if the box is valid


    def make_string(self):
        """Constructs a box string from the box object"""
        string = u''
        if self.bold:
            string += u"@"
        if self.italic:
            string += u"$"
        if self.uline:
            string += u"'"

        string +=  u'%s %d %d %d %d %d' % (self.text, self.left, self.bottom, self.right, self.top, self.page)

        return string

    def set_text(self, string):
        if type(string) is str or type(string) is unicode:
            self.text = string
        else:
            raise TypeError(u"Box text must be a string, not " + str(type(string)))

    def __init__(self, string=None):

        if not string:
            return

        fields = string.split()

        if len(fields) == 6:
            try:

                self.left = int(fields[1])
                self.bottom = int(fields[2])
                self.right = int(fields[3])
                self.top = int(fields[4])

                self.page = int(fields[5])

                self.text = fields[0]

                self.valid = True

            except ValueError: 
                return

            # Potentially have attribute markers
            # The first three characters must be $, @, or ' to
            # signify the character's attributes. Any other
            # character, or a repeat of one of these three
            # characters, indicates that the attribute markers
            # are over, and the main text begins.
            # A single character should be treated as that character.
            if len(self.text) > 1:
                i = 0
                while (not self.bold or not self.italic or not self.uline) and i < len(self.text):
                    if text[i] == u'$' and not self.italic:
                        self.italic = True
                    elif text[i] == u'@' and not self.bold:
                        self.bold = True
                    elif text[i] == u"'" and not self.uline:
                        self.uline = True
                    else:
                        self.text = self.text[i:]
                        break

    def __repr__(self):
        return "TesseractBox: "+self.make_string()

    def __str__(self):
        return self.make_string()

    def __unicode__(self):
        return self.make_string()
