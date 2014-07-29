#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: views.py 44701 2014-07-29 20:30:15Z carlos.sanchez $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

def _image_renderer(self, command):
    width = self.width
    height = self.height

    if self.width > 600:
        if self.height != 0:
            height = int(float(600.0 / self.width) * self.height)
        width = 600

    params = 'width=%spx,height=%spx' % (width, height)

    # Output 'small' images as ordinary graphics instead of some fancy type
    threshold = 30
    if self.width < threshold or self.height < threshold:
        command = u'includegraphics'

    return u'\\%s[%s]{%s}' % (command, params, self.path)

def image_annotation_renderer(self):
    return _image_renderer(self, 'ntiincludeannotationgraphics')

def image_noannotation_renderer(self):
    return _image_renderer(self, 'ntiincludenoannotationgraphics')
