#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml.html import HtmlComment

from zope import component

from nti.contenttools import types

from nti.contenttools._compat import text_

from nti.contenttools.adapters.epub.tcia.interfaces import IChildProcessor

from nti.contenttools.types import TextNode

from nti.contenttools.adapters.epub.tcia.finder import search_image_thubms_up_down

def adapt(fragment, epub=None):
    body = fragment.find('body')
    epub_body = EPUBBody.process(body, epub)
    search_image_thubms_up_down(epub_body)
    return epub_body


class EPUBBody(types.EPUBBody):

    @classmethod
    def process(cls, element, epub=None):
        me = cls()
        me = check_element_text(me, element)
        me = check_child(me, element, epub)
        me = check_element_tail(me, element)
        return me


def check_element_text(node, element):
    if element.text:
        if element.text.isspace():
            if len(element.text) == 1:
                node.add_child(TextNode(u' '))
        else:
            node.add_child(TextNode(text_(element.text)))
    return node


def check_child(node, element, epub=None):
    for child in element:
        processor = component.queryUtility(IChildProcessor, name=child.tag)
        if processor is not None:
            processor.process(child, node, element, epub=epub)
        elif not isinstance(child, HtmlComment):
            logger.warn('Unhandled %s child: %s.', element, child)
    return node


def check_element_tail(node, element):
    if element.tail:
        if not element.tail.isspace():
            new_el_tail = element.tail
            node.add_child(TextNode(new_el_tail))
    return node
