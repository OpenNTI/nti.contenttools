#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools import types

from nti.contenttools.adapters.epub.generic import check_child
from nti.contenttools.adapters.epub.generic import check_element_text
from nti.contenttools.adapters.epub.generic import check_element_tail

class OrderedList(types.OrderedList):

    @classmethod
    def process(cls, element, epub=None):
        me = cls()
        for child in element:
            el = None
            if child.tag == 'li':
                el = Item.process(child, epub=epub)
            else:
                logger.warning('OrderedList child %s', child.tag)
                el = Item()
            me.add_child(el)
        return me


class UnorderedList(types.UnorderedList):

    @classmethod
    def process(cls, element, epub=None):
        me = cls()
        for child in element:
            el = None
            if child.tag == 'li':
                el = Item.process(child, bullet_type=me.format, epub=epub)
            else:
                logger.warning('UnorderedList child %s', child.tag)
                el = Item()        
            me.add_child(el)
        return me


class Item(types.Item):

    @classmethod
    def process(cls, element, bullet_type=None, epub=None):
        me = cls()
        me = check_element_text(me, element)
        me = check_child(me, element, epub)
        me = check_element_tail(me, element)
        me.bullet_type = bullet_type
        return me
