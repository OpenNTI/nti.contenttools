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

from nti.contenttools._compat import unicode_

from nti.contenttools.adapters.epub.ifsta.interfaces import IChildProcessor

from nti.contenttools.types import TextNode

from nti.contenttools.adapters.epub.ifsta.finder import search_sidebar_info
from nti.contenttools.adapters.epub.ifsta.finder import remove_extra_figure_icon
from nti.contenttools.adapters.epub.ifsta.finder import process_paragraph_captions
from nti.contenttools.adapters.epub.ifsta.finder import search_and_update_figure_caption
from nti.contenttools.adapters.epub.ifsta.finder import remove_paragraph_caption_from_epub_body

from nti.contenttools.adapters.epub.ifsta.finder import search_sidebar_terms
from nti.contenttools.adapters.epub.ifsta.finder import search_and_update_glossary_entries
from nti.contenttools.adapters.epub.ifsta.finder import search_sidebar_head_and_body
from nti.contenttools.adapters.epub.ifsta.finder import process_sidebar_head_and_body
from nti.contenttools.adapters.epub.ifsta.finder import update_caption_list
from nti.contenttools.adapters.epub.ifsta.finder import search_and_update_figure_caption_reflowable

def adapt(fragment, epub=None):
    body = fragment.find('body')
    epub_body = EPUBBody.process(body, epub)
    # The next line only work for IFSTA fixed (to reduce the amount of
    # unnessary text)
    epub_body.children.pop(0)

    if epub.epub_type == 'ifsta':
        # ifsta epub has what is called sidebar info
        # each sidebar info has icon,
        # unfortunately on the xhmtl, it is separated in different div tag
        # the following lines are to get the icon as sidebar child
        nodes = []
        nodes = search_sidebar_info(epub_body, nodes)
        figures = add_icon_to_sidebar_info(nodes)
        for figure in figures:
            remove_extra_figure_icon(epub_body, figure)

        captions = process_paragraph_captions(epub.captions)
        search_and_update_figure_caption(epub_body, captions)
        remove_paragraph_caption_from_epub_body(epub_body)
    else:
        sidebars = {}
        search_sidebar_terms(epub_body, sidebars, epub.sidebar_term_nodes)
        search_and_update_glossary_entries(epub_body, sidebars)

        snodes = []
        search_sidebar_head_and_body(epub_body, snodes)
        process_sidebar_head_and_body(snodes)

        captions = update_caption_list(epub.caption_list)

        search_and_update_figure_caption_reflowable(
            epub_body, captions, epub.figure_node)

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
    for child in element:
        processor = component.queryUtility(IChildProcessor, name=child.tag)
        if processor is not None:
            processor.process(child, node, element, epub=epub)
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