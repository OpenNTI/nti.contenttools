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
from nti.contenttools.adapters.epub.ifsta import check_element_text
from nti.contenttools.adapters.epub.ifsta import check_element_tail


class OrderedList(types.OrderedList):

    @classmethod
    def process(cls, element):
        me = cls()
        if 'data-number-style' in element.attrib:
            numbering_type = element.attrib['data-number-style']
            me.start = 1

            if numbering_type == u'1':
                me.format = 'decimal'
            elif u'lower-alpha' in numbering_type:
                me.format = 'lowerLetter'
            elif u'upper-alpha' in numbering_type:
                me.format = 'upperLetter'
            elif u'lower-roman' in numbering_type:
                me.format = 'lowerRoman'
            elif u'upper-roman' in numbering_type:
                me.format = 'upperRoman'
            elif u'arabic' in numbering_type:
                me.format = 'decimal'
            else:
                logger.warn("UNHANDLED OrderedList numbering format type %s", 
                            numbering_type)

        for child in element:
            el = None
            if child.tag == 'li':
                el = Item.process(child)
            else:
                logger.info('OrderedList child %s', child.tag)
                el = Item()
            if isinstance(el, types.Item) or isinstance(el, types.List):
                me.add_child(el)
            else:
                if len(me.children) == 0:
                    me.add_child(Item())
                me.children[-1].add_child(el)
        return me


class UnorderedList(types.UnorderedList):

    @classmethod
    def process(cls, element):
        me = cls()
        if 'style' in element.attrib:
            numbering_style = element.attrib['style']
            me.start = 1
            if u'circle' in numbering_style:
                me.format = u'circ'
            elif u'disc' in numbering_style:
                me.format = u'bullet'
            elif u'square' in numbering_style:
                me.format = u'blacksquare'
            else:
                logger.warn("UNHANDLED UnorderedList numbering format type %s", 
                            numbering_style)
        for child in element:
            el = None
            if child.tag == 'li':
                el = Item.process(child, format=me.format)
            elif child.tag == 'div':
                from nti.contenttools.adapters.epub.ifsta.run import process_div_elements
                el = process_div_elements(child, me)
            elif child.tag == 'p':
                from nti.contenttools.adapters.epub.ifsta.paragraph import Paragraph
                el = Paragraph.process(child)
            else:
                el = Item()

            if isinstance(el, (types.Item, types.List)):
                me.add_child(el)
            else:
                if not me.children:
                    me.add_child(Item())
                me.children[-1].add_child(el)
        return me


class Item(types.Item):

    @classmethod
    def process(cls, element, format_=None):
        me = cls()
        me = check_element_text(me, element)
        me = check_child(me, element)
        me = check_element_tail(me, element)
        me.bullet_type = format_
        return me
