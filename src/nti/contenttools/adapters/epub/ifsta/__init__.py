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

from nti.contenttools.adapters.epub.ifsta.interfaces import IChildProcessor

from nti.contenttools.types import TextNode
from nti.contenttools.types import ChapterCounter

from nti.contenttools.adapters.epub.ifsta.finder import search_sidebar_info
from nti.contenttools.adapters.epub.ifsta.finder import remove_extra_figure_icon
from nti.contenttools.adapters.epub.ifsta.finder import process_paragraph_captions
from nti.contenttools.adapters.epub.ifsta.finder import search_and_update_figure_caption
from nti.contenttools.adapters.epub.ifsta.finder import remove_paragraph_caption_from_epub_body

from nti.contenttools.adapters.epub.ifsta.finder import search_table
from nti.contenttools.adapters.epub.ifsta.finder import update_caption_list
from nti.contenttools.adapters.epub.ifsta.finder import search_sidebar_terms
from nti.contenttools.adapters.epub.ifsta.finder import cleanup_table_element
from nti.contenttools.adapters.epub.ifsta.finder import add_icon_to_sidebar_info
from nti.contenttools.adapters.epub.ifsta.finder import search_paragraph_section
from nti.contenttools.adapters.epub.ifsta.finder import search_sidebar_head_and_body
from nti.contenttools.adapters.epub.ifsta.finder import process_sidebar_head_and_body
from nti.contenttools.adapters.epub.ifsta.finder import process_sidebar_figure_info_rf
from nti.contenttools.adapters.epub.ifsta.finder import search_figure_icon_on_sidebar_title
from nti.contenttools.adapters.epub.ifsta.finder import search_and_update_glossary_entries
from nti.contenttools.adapters.epub.ifsta.finder import search_and_update_figure_caption_reflowable


def adapt(fragment, epub=None):
    body = fragment.find('body')
    epub_body = EPUBBody.process(body, epub)

    # we can use the following lines if the epub has <table> element
    tables = []
    search_table(epub_body, tables)
    cleanup_table_element(tables)

    logger.info("CHAPTER NUM")
    logger.info(epub.chapter_num)
    search_paragraph_section(epub_body, epub.section_list, epub.chapter_num)

    if epub.epub_type == 'ifsta':
        # The next line only work for IFSTA fixed (to reduce the amount of
        # unnessary text)
        epub_body.children.pop(0)

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
        search_sidebar_terms(epub_body, sidebars, epub.sidebar_term_nodes, epub.chapter_num, epub.glossary_entry_sections)
        search_and_update_glossary_entries(epub_body, sidebars)

        snodes = []
        search_sidebar_head_and_body(epub_body, snodes)
        sidebar_list = process_sidebar_head_and_body(snodes)

        for sbar in sidebar_list:
            figs = []
            search_figure_icon_on_sidebar_title(sbar.title, figs)
            if figs:
                sbar.children.insert(0, figs[0])

        captions = update_caption_list(epub.caption_list)

        search_and_update_figure_caption_reflowable(
            epub_body, captions, epub.figure_node, epub.figure_ref)

        # just in case figure icon is located outside sidebar node
        sfnodes = []
        sfnodes = search_sidebar_info(epub_body, sfnodes)
        process_sidebar_figure_info_rf(sfnodes)

    return epub_body


class EPUBBody(types.EPUBBody):

    @classmethod
    def process(cls, element, epub=None):
        me = cls()
        if epub:
            if epub.chapter_num:
                counter = ChapterCounter()
                counter.counter_number = text_(epub.chapter_num)
                me.add_child(counter)
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
