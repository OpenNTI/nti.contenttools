#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools import types

from nti.contenttools._compat import text_

from nti.contenttools.adapters.epub.tcia import check_element_tail

from nti.contenttools.adapters.epub.tcia.run import Run


class Hyperlink(types.Hyperlink):

    def __init__(self):
        self.type = u'Normal'

    @classmethod
    def process(cls, link, epub=None):
        me = cls()
        if u'href' in link.attrib:
            me.target = text_(link.attrib['href'])
            if link.text:
                me.add_child(types.TextNode(link.text))
            for child in link:
                me.add_child(Run.process(child))
        else:
            me = Run()
            check_element_tail(me, link)
        return me
