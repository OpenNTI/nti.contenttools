#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools import types

from nti.contenttools.types.glossary import GlossaryEntry

from nti.contenttools.adapters.epub.ifsta import check_child
from nti.contenttools.adapters.epub.ifsta import check_element_text
from nti.contenttools.adapters.epub.ifsta import check_element_tail

from nti.contenttools.adapters.epub.ifsta.lists import Item
from nti.contenttools.adapters.epub.ifsta.lists import UnorderedList

from nti.contenttools.adapters.epub.ifsta.note import Sidebar

from nti.contenttools.types import TextNode

from nti.contenttools.types.interfaces import ITextNode
from nti.contenttools.types.interfaces import IParagraph

from nti.contenttools.renderers.LaTeX.base import render_output


class Run(types.Run):

    @classmethod
    def process(cls, element, styles=(), reading_type=None, epub=None):
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
            if child.element_type == 'sidebars-body':
                body_text.append(child)
        elif isinstance(child, types.Sidebar):
            caption.append(child)
        elif isinstance(child, Run):
            examine_div_element_for_sidebar(child, caption, body_text)
    return caption


def process_div_elements(element, parent, epub=None):
    # note: table_div_classes may vary from chapter to chapter
    table_div_classes = (u'_idGenObjectStyleOverride-9', )

    el = Run.process(element, epub=epub)

    if epub is not None:
        # need to check if there the div has sidebar-head and sidebar-text
        caption = []
        sidebar_body_text = []
        caption = examine_div_element_for_sidebar(el, caption, sidebar_body_text)
        if sidebar_body_text:
            if not caption:
                new_el = Sidebar()
                new_el.type = u'sidebar-head'
                parent = sidebar_body_text[0].__parent__
                index = parent.children.index(sidebar_body_text[0])
                parent.children.insert(index, new_el)

    attrib = element.attrib
    div_class = attrib['class'] if 'class' in attrib else u''

    if div_class in table_div_classes:
        # need to clean up paragraph element that located under this particular div
        # therefore when the node is rendered it won't have extra \\
        update_node_under_table_div_class(el)
    return el


def update_node_under_table_div_class(root):
    if IParagraph.providedBy(root):
        if hasattr(root, '__parent__'):
            parent = root.__parent__
            idx = parent.children.index(root)
            parent.remove(root)
            node = Run()
            node.children = root.children
            node.add(TextNode(u'\n'))
            parent.children.insert(idx, node)
    if hasattr(root, 'children'):
        for child in root:
            update_node_under_table_div_class(child)


def check_paragraph_bullet(el):
    for child in el.children:
        if isinstance(child, types.Run):
            if child.element_type == 'bullet':
                return True
    return False


def process_span_elements(element, epub=None):
    font_style = u''
    font_weight = u''
    color = u''
    font_family = u''
    vertical_align = u''

    term_class = (u'Key_Term_in_Body', u'Key-Term-in-text', u'Key-Term', u'Key_Term',)

    term_colors = (u'#c00000', u'#c8161d', u'#bf2026', u'#802023', u'#812023', u'#a30022', u'#ff0000', u'#c8151c', u'#ab1d22', u'#b4282e')
    font_terms = (u'Utopia Std', u'Minion Pro', u'Helvetica LT Std',)

    attrib = element.attrib
    span_class = attrib['class'] if 'class' in attrib else u''

    if 'bullet' in span_class:
        span_class = u'span_%s' % span_class.replace('-', '_').replace('bullet ', '')
        if epub is not None and span_class in epub.css_dict:
            font_style, font_weight, font_family, color = get_font_attribute_value(epub, span_class)
            if epub.epub_type == 'ifsta_rf' \
                    and (font_style == u'normal' or font_style == u'italic')\
                    and font_weight == u'bold' \
                    and color in term_colors \
                    and font_family in font_terms:
                fstyles = [font_style, font_weight]
                el = create_glossary_entry(element, fstyles)
            else:
                el = Run()
                el_text = Run()
                check_element_text(el_text, element)
                check_element_tail(el_text, element)
                if font_style == 'italic' or font_style == 'oblique':
                    el_text.styles.append('italic')
                if font_weight == 'bold':
                    el_text.styles.append('bold')
                el.add(el_text)
                el.element_type = 'bullet'
    elif 'bold' in span_class.lower():
        el = Run.process(element, styles=('bold',), epub=epub)
    elif 'italic' in span_class.lower():
        el = Run.process(element, styles=('italic',), epub=epub)
    elif any(s.lower() in span_class.lower() for s in term_class):
        el = create_glossary_entry(element)
    elif 'NOTE' in span_class:
        el = Run.process(element, epub=epub)
        el.element_type = 'span-note'
    else:
        span_class = u'span_%s' % span_class.replace('-', '_')
        if epub is not None and span_class in epub.css_dict:
            font_style, font_weight, font_family, color = get_font_attribute_value(epub, span_class)
            if 'verticalAlign' in epub.css_dict[span_class]:
                vertical_align = epub.css_dict[span_class]['verticalAlign']

            if epub.epub_type == 'ifsta_rf' \
                    and (font_style == u'normal' or font_style == u'italic')\
                    and font_weight == u'bold' \
                    and color in term_colors \
                    and font_family in font_terms:
                fstyles = [font_style, font_weight]
                el = create_glossary_entry(element, fstyles)
            else:
                el = Run()
                el_text = Run()
                check_element_text(el_text, element)
                check_child(el_text, element, epub)

                if font_style == 'italic' or font_style == 'oblique':
                    el_text.styles.append('italic')
                elif 'italic' in font_family.lower():
                    el_text.styles.append('italic')

                if font_weight == 'bold':
                    el_text.styles.append(font_weight)
                elif 'bold' in font_family.lower():
                    el_text.styles.append('bold')

                if vertical_align == 'super':
                    el_text.styles.append('superscript')
                elif vertical_align == 'sub':
                    el_text.styles.append('subscript')

                el.add(el_text)
                check_element_tail(el, element)
        else:
            el = Run.process(element, epub=epub)
            if 'italic' in span_class:
                el.styles.append('italic')
            if 'bold' in span_class:
                el.styles.append('bold')

    if epub is not None and epub.epub_type == 'ifsta':
        check_span_child(el)
    return el


def create_glossary_entry(element, fstyles=('bold',)):
    el = Run()
    t_el = Run()
    check_element_text(t_el, element)
    check_child(t_el, element)
    check_term = render_output(t_el)
    if not check_term.isspace():
        t_el.styles = list(t_el.styles) + list(fstyles)
        glossary = GlossaryEntry()
        glossary.term = t_el
        el.add(glossary)
    check_element_tail(el, element)
    return el


def check_span_child(span_node):
    for child in span_node:
        if ITextNode.providedBy(child):
            if child.endswith('-'):
                child = child[:-1]


def get_font_attribute_value(epub, span_class):
    font_style = u''
    font_weight = u''
    color = u''
    font_family = u''

    if 'fontStyle' in epub.css_dict[span_class]:
        font_style = epub.css_dict[span_class]['fontStyle']

    if 'fontWeight' in epub.css_dict[span_class]:
        font_weight = epub.css_dict[span_class]['fontWeight']

    if 'color' in epub.css_dict[span_class]:
        color = epub.css_dict[span_class]['color']

    if 'fontFamily' in epub.css_dict[span_class]:
        font_family = epub.css_dict[span_class]['fontFamily']
        font_family = font_family.replace('"', '')

    return font_style, font_weight, font_family, color
