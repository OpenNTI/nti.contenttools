#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: run.py 119034 2017-08-09 13:43:34Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)


from nti.contenttools import types

from nti.contenttools.adapters.html.mathcounts import check_child
from nti.contenttools.adapters.html.mathcounts import check_element_text
from nti.contenttools.adapters.html.mathcounts import check_element_tail

from nti.contenttools import types

class HTMLBody(types.Body):
    @classmethod
    def process(cls,element):
        me = cls()
        me = check_element_text(me, element)
        me = check_child(me, element, html)
        me = check_element_tail(me, element)
        return me    


class Run(types.Run):

    @classmethod
    def process(cls, element, styles=(), html=None):
        me = cls()
        me.styles.extend(styles)
        me = check_element_text(me, element)
        me = check_child(me, element, html)
        if element.tail:
            _t = cls()
            _t.add_child(me)
            tail = element.tail.replace('\r', '').replace('\t', '')
            _t.add_child(types.TextNode(tail))
            me = _t
        return me