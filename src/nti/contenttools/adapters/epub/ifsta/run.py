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

from nti.contenttools.adapters.epub.ifsta.lists import Item
from nti.contenttools.adapters.epub.ifsta.lists import UnorderedList

from nti.contenttools.adapters.epub.ifsta.note import Sidebar

from nti.contenttools.types.interfaces import ITextNode


class Run(types.Run):

    @classmethod
    def process(cls, element, styles=[], reading_type=None, epub=None):
        me = cls()
        if 'id' in element.attrib:
            me.label = element.attrib['id']
        me.styles.extend(styles)
        me = check_element_text(me, element)
        me = check_child(me, element, epub)
        if element.tail:
            _t = cls()
            _t.add_child(me)
            tail = element.tail.replace('\r', '').replace('\t', '')
            _t.add_child(types.TextNode(tail))
            me = _t
        return me


def examine_div_element_for_sidebar(el, caption, body_text):
    for child in el.children:
        if isinstance(child, types.Paragraph):
            if child.element_type == u'sidebars-heads':
                caption.add_child(child)
            elif child.element_type == u'sidebars-body':
                check_list = check_paragraph_bullet(child)
                if check_list:
                    bullet_class = UnorderedList()
                    new_item = Item()
                    new_item.children = [child]
                    bullet_class.children = [new_item]
                    body_text.add_child(bullet_class)
                else:
                    body_text.add_child(child)
            elif child.element_type == u'caption':
                pass
            else:
                body_text.add_child(child)
        elif isinstance(child, Run):
            caption, body_text = examine_div_element_for_sidebar(child,
                                                                 caption,
                                                                 body_text)
    return caption, body_text


def process_div_elements(element, parent, epub=None):
    el = Run.process(element, epub=epub)

    if epub is not None and epub.epub_type == 'ifsta':
        logger.info(epub.epub_type)
        # need to check if there the div has sidebar-head and sidebar-text
        caption = Run()
        body_text = Run()
        caption, body_text = examine_div_element_for_sidebar(el,
                                                             caption,
                                                             body_text)
        if caption.children and body_text.children:
            new_el = Sidebar()
            new_el.title = caption
            new_el.children = body_text.children
            el = new_el

    return el


def check_paragraph_bullet(el):
    for child in el.children:
        if isinstance(child, types.Run):
            if child.element_type == 'bullet':
                return True
    return False


def process_span_elements(element, epub=None):
    attrib = element.attrib
    span_class = attrib['class'] if u'class' in attrib else u''
    span_class = u'span_%s' % span_class.replace('-', '_')
    if 'bullet' in span_class:
        el = Run()
        check_element_tail(el, element)
        el.element_type = 'bullet'
    elif 'NOTE' in span_class:
        el = Run.process(element, epub=epub)
        el.styles = ['bold']
    else:
        el = Run.process(element, epub=epub)
        if epub is not None and span_class in epub.css_dict:
            if 'fontStyle' in epub.css_dict[span_class]:
                style = epub.css_dict[span_class]['fontStyle']
                if style == 'italic':
                    el.styles.append(style)
            if 'fontWeight' in epub.css_dict[span_class]:
                weight = epub.css_dict[span_class]['fontWeight']
                if weight == 'bold':
                    el.styles.append(weight)
    check_span_child(el)
    return el


def check_span_child(span_node):
    for child in span_node:
        if ITextNode.providedBy(child):
            if child.endswith('-'):
                logger.info(child)
                child = child[:-1]
