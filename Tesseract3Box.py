class Tesseract3Box:

    text = u''

    left = None
    right = None
    top = None
    bottom = None

    page = None

    valid = False


    def make_string(self):
        """Constructs a box string from the box object"""
        string = u''

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

    def __repr__(self):
        return "Tesseract3Box: "+self.make_string()

    def __str__(self):
        return self.make_string()

    def __unicode__(self):
        return self.make_string()
