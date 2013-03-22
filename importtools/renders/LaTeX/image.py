def _image_renderer(self, command):
    # SAJ: Assuming 72 DPI.  This is bound to cause a problem somewhere.
    dpi = 72
    width = int(round(self.width * dpi))
    height = int(round(self.height * dpi))

    if width > 600:
        if height != 0:
            height = int(round((600 / width) * height))
        width = 600

    params = 'width=%s,height=%s' % (width, height)

    return u'\\%s[%s]{%s}' % (command, params, self.path)

def image_annotation_renderer(self):
    return _image_renderer(self, 'ntiincludeannotationgraphics')

def image_noannotation_renderer(self):
    return _image_renderer(self, 'ntiincludenoannotationgraphics')
