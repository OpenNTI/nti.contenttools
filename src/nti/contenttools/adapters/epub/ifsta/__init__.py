#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: __init__.py 105585 2017-02-01 02:54:15Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml.html import HtmlComment

from nti.contenttools import types


def check_element_text(node, element):
    if element.text:
        if element.text.isspace():
            if len(element.text) == 1:
                node.add_child(types.TextNode(u' '))
            else:
                pass
        else:
            node.add_child(types.TextNode(unicode(element.text)))
    return node


def check_child(node, element, reading_type=None):
    for child in element:
        if child.tag == 'p':
            from nti.contenttools.adapters.epub.ifsta.paragraph import Paragraph
            node.add_child(Paragraph.process(child, [], reading_type))
        else:
            if isinstance(child, HtmlComment):
                pass
            else:
                logger.warn('Unhandled %s child: %s.', element, child)
    return node


def check_element_tail(node, element):
    if element.tail:
        if element.tail.isspace():
            pass
        else:
            new_el_tail = element.tail.rstrip() + u' '
            node.add_child(types.TextNode(new_el_tail))
    return node
