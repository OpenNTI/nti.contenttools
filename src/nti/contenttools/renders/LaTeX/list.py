#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer, _environment_renderer

def ordered_list_renderer(self):
    optional = u''
    if self.format == 'decimal':
        optional = u'1'
    elif self.format == 'lowerLetter':
        optional = u'a'
    elif self.format == 'upperLetter':
        optional = u'A'
    elif self.format == 'lowerRoman':
        optional = u'i'
    elif self.format == 'upperRoman':
        optional = u'I'

    if self.start != 1:
        optional = optional + u', start=%s' % self.start

    if optional:
        optional = u'[' + optional + u']'

    return _environment_renderer(self, u'enumerate', optional)

def list_renderer(self):
    return _environment_renderer(self, u'itemize', u'')

def item_renderer(self):
    return u'\\item %s' % base_renderer(self)

