#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
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
            node.add_child(types.TextNode(unicode(element.text)))
    return node


def check_child(node, element, reading_type=None):
    # XXX: Avoid circular imports
    from nti.contenttools.adapters.epub.ifsta.paragraph import Paragraph
    from nti.contenttools.adapters.epub.ifsta.run import Run
    from nti.contenttools.adapters.epub.ifsta.run import process_div_elements
    from nti.contenttools.adapters.epub.ifsta.run import process_span_elements
    for child in element:
        if child.tag == 'p':
            node.add_child(Paragraph.process(child, [], reading_type))
        elif child.tag == 'span':
            node.add_child(process_span_elements(child))
        elif child.tag == 'b':
            node.add_child(Run.process(child, ['bold']))
        elif child.tag == 'i':
            node.add_child(Run.process(child, ['italic']))
        elif child.tag == 'u':
            node.add_child(Run.process(child, ['underline']))
        elif child.tag == 'strong':
            node.add_child(Run.process(child, ['bold']))
        elif child.tag == 's':
            node.add_child(Run.process(child, ['strike']))
        elif child.tag == 'em' or child.tag == 'emphasis':
            node.add_child(Run.process(child, ['italic']))
        elif child.tag == 'sub':
            node.add_child(Run.process(child, ['sub']))
        elif child.tag == 'sup':
            node.add_child(Run.process(child, ['sup']))
        elif child.tag == 'div':
            node.add_child(process_div_elements(child, node))
        else:
            if not isinstance(child, HtmlComment):
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
