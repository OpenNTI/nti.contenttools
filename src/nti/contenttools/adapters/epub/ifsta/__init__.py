#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
from pty import CHILD
from re import search

__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml.html import HtmlComment

from nti.contenttools import types

from nti.contenttools._compat import unicode_

from nti.contenttools.types import TextNode

from nti.contenttools.types.interfaces import ISidebar, IFigure, ITextNode


def adapt(fragment, epub=None):
    body = fragment.find('body')
    epub_body = EPUBBody.process(body, epub)
    #The next line only work for IFSTA fixed (to reduce the amount of unnessary text)
    epub_body.children.pop(0)
    nodes = []
    nodes = search_sidebar_info(epub_body, nodes)
    logger.info(nodes)
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
            node.add_child(TextNode(unicode_(element.text)))
    return node


def check_child(node, element, epub=None):
    # XXX: Avoid circular imports
    from nti.contenttools.adapters.epub.ifsta.lists import OrderedList
    from nti.contenttools.adapters.epub.ifsta.lists import UnorderedList
    from nti.contenttools.adapters.epub.ifsta.media import Image
    from nti.contenttools.adapters.epub.ifsta.media import Figure
    from nti.contenttools.adapters.epub.ifsta.paragraph import Paragraph
    from nti.contenttools.adapters.epub.ifsta.run import Run
    from nti.contenttools.adapters.epub.ifsta.run import process_div_elements
    from nti.contenttools.adapters.epub.ifsta.run import process_span_elements
    from nti.contenttools.adapters.epub.ifsta.table import Table
    from nti.contenttools.adapters.epub.ifsta.link import Hyperlink

    for child in element:
        if child.tag == 'p':
            node.add_child(Paragraph.process(child, [], epub=epub))
        elif child.tag == 'span':
            node.add_child(process_span_elements(child, epub=epub))
        elif child.tag == 'a':
            node.add_child(Hyperlink.process(child, epub=epub))
        elif child.tag == 'b':
            node.add_child(Run.process(child, ['bold'], epub=epub))
        elif child.tag == 'i':
            node.add_child(Run.process(child, ['italic'], epub=epub))
        elif child.tag == 'u':
            node.add_child(Run.process(child, ['underline'], epub=epub))
        elif child.tag == 'strong':
            node.add_child(Run.process(child, ['bold'], epub=epub))
        elif child.tag == 's':
            node.add_child(Run.process(child, ['strike'], epub=epub))
        elif child.tag == 'em' or child.tag == 'emphasis':
            node.add_child(Run.process(child, ['italic'], epub=epub))
        elif child.tag == 'sub':
            node.add_child(Run.process(child, ['sub'], epub=epub))
        elif child.tag == 'sup':
            node.add_child(Run.process(child, ['sup'], epub=epub))
        elif child.tag == 'div':
            node.add_child(process_div_elements(child, node, epub=epub))
        elif child.tag == 'h1':
            node.add_child(Paragraph.process(child, ['Heading1'], epub=epub))
        elif child.tag == 'h2':
            node.add_child(Paragraph.process(child, ['Heading2'], epub=epub))
        elif child.tag == 'h3':
            node.add_child(Paragraph.process(child, ['Heading3'], epub=epub))
        elif child.tag == 'h4':
            node.add_child(Paragraph.process(child, ['Heading4'], epub=epub))
        elif child.tag == 'h5':
            node.add_child(Paragraph.process(child, ['Heading5'], epub=epub))
        elif child.tag == 'h6':
            node.add_child(Paragraph.process(child, ['Heading6'], epub=epub))
        elif child.tag == 'h7':
            node.add_child(Paragraph.process(child, ['Heading7'], epub=epub))
        elif child.tag == 'ol':
            node.add_child(OrderedList.process(child, epub=epub))
        elif child.tag == 'ul':
            node.add_child(UnorderedList.process(child, epub=epub))
        elif child.tag == 'table':
            node.add_child(Table.process(child, epub=epub))
        elif child.tag == 'img':
            node.add_child(Image.process(child, epub=epub))
        elif child.tag == 'figure':
            node.add_child(Figure.process(child, epub=epub))
        elif not isinstance(child, HtmlComment):
            logger.warn('Unhandled %s child: %s.', element, child)
    return node


def check_element_tail(node, element):
    if element.tail:
        if element.tail.isspace():
            pass
        else:
            new_el_tail = element.tail.rstrip() + u' '
            node.add_child(TextNode(new_el_tail))
    return node

def search_sidebar_info(root,nodes):
    if ISidebar.providedBy(root):
        if root.type == u"sidebar_term":
            pass
        else:
            nodes.append(root)
    if ITextNode.providedBy(root):
        pass
    else:
        for child in root.children:
            if IFigure.providedBy(child):
                if child.floating == True:
                    nodes.append(child)
            else:
                search_sidebar_info(child, nodes)
    return nodes