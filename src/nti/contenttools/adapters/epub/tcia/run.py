#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools import types

from nti.contenttools.adapters.epub.tcia import check_child
from nti.contenttools.adapters.epub.tcia import check_element_text
from nti.contenttools.adapters.epub.tcia import check_element_tail

from nti.contenttools.adapters.epub.generic.run import Run

from nti.contenttools.types import TextNode

def process_span_elements(element, epub=None):
    el = Run.process(element, epub=epub)
    attrib = element.attrib
    span_class = attrib['class'] if 'class' in attrib else u''
    font_style = u''
    font_weight = u''
    if epub is not None:
        span_class = u'span_%s' % span_class.replace('-', '_')
        if span_class in epub.css_dict:
            if 'fontStyle' in epub.css_dict[span_class]:
                font_style = epub.css_dict[span_class]['fontStyle']
                if font_style != u'normal':
                    el.styles.append(font_style)
            if 'fontWeight' in epub.css_dict[span_class]:
                font_weight = epub.css_dict[span_class]['fontWeight']
                if font_weight != u'normal':
                    el.styles.append(font_weight)
    return el