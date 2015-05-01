#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: math_adapter.py 58552 2015-01-29 23:10:30Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ... import types
from lxml.html import HtmlComment
import os
from IPython.core.debugger import Tracer

class Image(types.Image):
    @classmethod
    def process(cls, element, inline_image=False):
        me = cls()
        path = element.attrib['src']
        head, me.path = os.path.split(path)
        me.inline_image = inline_image
        if 'alt' in element.attrib.keys():
            me.caption = element.attrib['alt']