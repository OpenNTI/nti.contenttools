#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools import types

from nti.contenttools.adapters.epub.ifsta import check_child
from nti.contenttools.adapters.epub.ifsta import check_element_tail
from nti.contenttools.adapters.epub.ifsta import check_element_text


class Sidebar(types.Sidebar):

    @classmethod
    def process(cls, element, sidebar_type=None, epub=None):
        me = cls()
        if 'id' in element.attrib:
            me.label = element.attrib['id']
        me = check_element_text(me, element)
        me = check_child(me, element, epub)
        me = check_element_tail(me, element)
        if me.title is None:
            me.title = sidebar_type.title()
        return me
