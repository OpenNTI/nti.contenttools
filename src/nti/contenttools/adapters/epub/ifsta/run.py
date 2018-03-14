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
            if child.element_type == 'sidebars-heads':
                caption.add_child(child)
            elif child.element_type == 'sidebars-body':
                check_list = check_paragraph_bullet(child)
                if check_list:
                    bullet_class = UnorderedList()
                    new_item = Item()
                    new_item.children = [child]
                    bullet_class.children = [new_item]
                    body_text.add_child(bullet_class)
                else:
                    body_text.add_child(child)
            elif child.element_type == 'caption':
                pass
            else:
                body_text.add_child(child)
        elif isinstance(child, Run):
            caption, body_text = examine_div_element_for_sidebar(child,
                                                                 caption,
                                                                 body_text)
    return caption, body_text


def process_div_elements(element, parent, epub=None):
    # note: table_div_classes may vary from chapter to chapter
    table_div_classes = (u'_idGenObjectStyleOverride-9', )

    el = Run.process(element, epub=epub)

    if epub is not None and epub.epub_type == 'ifsta':
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

    term_class = (u'Key_Term_in_Body', u'Key-Term-in-text')

    term_colors = (u'#c00000', u'#c8161d', u'#bf2026', u'#802023', u'#812023')
    font_terms = (u'Utopia Std', u'Minion Pro', u'Helvetica LT Std',)

    attrib = element.attrib
    span_class = attrib['class'] if 'class' in attrib else u''

    if 'bullet' in span_class:
        el = Run()
        check_element_text(el, element)
        check_element_tail(el, element)
        el.element_type = 'bullet'
    elif any(s.lower() in span_class.lower() for s in term_class):
        el = create_glossary_entry(element)
    elif 'NOTE' in span_class:
        el = Run.process(element, epub=epub)
        el.styles = ['bold']
    else:
        span_class = u'span_%s' % span_class.replace('-', '_')
        if epub is not None and span_class in epub.css_dict:
            if 'fontStyle' in epub.css_dict[span_class]:
                font_style = epub.css_dict[span_class]['fontStyle']

            if 'fontWeight' in epub.css_dict[span_class]:
                font_weight = epub.css_dict[span_class]['fontWeight']

            if 'color' in epub.css_dict[span_class]:
                color = epub.css_dict[span_class]['color']

            if 'fontFamily' in epub.css_dict[span_class]:
                font_family = epub.css_dict[span_class]['fontFamily']
                font_family = font_family.replace('"','')
                
            if 'verticalAlign' in epub.css_dict[span_class]:
                vertical_align = epub.css_dict[span_class]['verticalAlign']

            if      epub.epub_type == 'ifsta_rf' \
                and font_style == u'normal' \
                and font_weight == u'bold' \
                and color in term_colors \
                and font_family in font_terms:
                el = create_glossary_entry(element)
            else:
                el = Run()
                el_text = Run()
                check_element_text(el_text, element)
                check_child(el_text, element, epub)

                if font_style == 'italic' or font_style == 'oblique':
                    el_text.styles.append('italic')

                if font_weight == 'bold':
                    el_text.styles.append(font_weight)

                if vertical_align == 'super':
                    el_text.styles.append('superscript')
                elif vertical_align == 'sub':
                    el_text.styles.append('subscript')

                el.add(el_text)
                check_element_tail(el, element)
        else:
            el = Run.process(element, epub=epub)

    if epub is not None and epub.epub_type == 'ifsta':
        check_span_child(el)
    return el

def create_glossary_entry(element):
    el = Run()
    t_el = Run()
    check_element_text(t_el, element)
    t_el.styles.append('bold')
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
