#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: __init__.py 110899 2017-04-18 12:35:19Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml.html import HtmlComment

from zope import component

from nti.contenttools._compat import text_

from nti.contenttools.types import TextNode

from nti.contenttools.adapters.html.mathcounts.interfaces import IChildProcessor

def check_element_text(node, element):
    if element.text:
        if element.text.isspace():
            if len(element.text) == 1:
                node.add_child(TextNode(u' '))
        else:
            node.add_child(TextNode(text_(element.text)))
    return node


def check_child(node, element, html=None):
    for child in element:
        processor = component.queryUtility(IChildProcessor, name=child.tag)
        print(child.tag)
        print(child.attrib)
        if processor is not None:
            processor.process(child, node, element, html)
        elif not isinstance(child, HtmlComment):
            logger.warn('Unhandled %s child: %s.', element, child)
    return node


def check_element_tail(node, element):
    if element.tail:
        if not element.tail.isspace():
            new_el_tail = element.tail
            node.add_child(TextNode(new_el_tail))
    return node
