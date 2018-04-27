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

from nti.contenttools.types import TextNode


class Run(types.Run):

    @classmethod
    def process(cls, element, styles=(), reading_type=None, epub=None):
        me = cls()
        me.styles.extend(styles)
        me = check_element_text(me, element)
        me = check_child(me, element, epub)
        if element.tail:
            _t = cls()
            _t.add_child(me)
            tail = element.tail.replace('\r', '').replace('\t', '')
            _t.add_child(types.TextNode(tail))
            me = _t
        return me

def process_div_elements(element, parent, epub=None):
    el = Run.process(element, epub=epub)
    return el

def process_span_elements(element, epub=None):
    el = Run.process(element, epub=epub)
    return el