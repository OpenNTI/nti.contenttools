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

from nti.contenttools.adapters.epub.prmia import check_element_tail

from nti.contenttools.adapters.epub.prmia.run import Run


class Hyperlink(types.Hyperlink):

    def __init__(self):
        self.type = 'Normal'

    @classmethod
    def process(cls, link, epub=None):
        me = cls()
        if 'href' in link.attrib:
            me.target = text_(link.attrib['href'])
            if link.text:
                me.add_child(types.TextNode(link.text))
            for child in link:
                me.add_child(Run.process(child))
        elif 'id' in link.attrib:
            epub.ids.append(link.attrib['id'])
            return
        else:
            me = Run()
            check_element_tail(me, link)
        return me
