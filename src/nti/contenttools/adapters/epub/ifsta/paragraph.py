#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import copy

from nti.contenttools import types

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.adapters.epub.ifsta import check_child
from nti.contenttools.adapters.epub.ifsta import check_element_text
from nti.contenttools.adapters.epub.ifsta import check_element_tail

from nti.contenttools.adapters.epub.ifsta.lists import Item
from nti.contenttools.adapters.epub.ifsta.lists import UnorderedList

from nti.contenttools.adapters.epub.ifsta.note import Sidebar

from nti.contenttools.adapters.epub.ifsta.run import Run

from nti.contenttools.types import TextNode
from nti.contenttools.types.interfaces import ITextNode

from nti.contenttools.adapters.epub.ifsta.finder import search_span_note
from nti.contenttools.adapters.epub.ifsta.finder import update_sidebar_body_bullet
from nti.contenttools.adapters.epub.ifsta.finder import search_figure_icon_on_sidebar_body

from nti.contenttools.types.note import BlockQuote
from nti.contenttools.types.note import CenterNode


class Paragraph(types.Paragraph):

    sidebar_list = (u'Case-History ParaOverride-1', u'Case-History',)
    bullet_list = (u'Bullet ParaOverride-1', u'Bullet')
    subsection_list = (u'B-HEAD ParaOverride-1', u'B-Head', u'B-HEAD')
    section_list = (u'A-Head', u'A-HEAD', 'A-HEAD ParaOverride-1',)
    paragraph_list = (u'Body-Text', u'Block-Text', 'ParaOverride', u'Basic-Paragraph')
    term_list = (u'Body-Copy_Keyterm_End-of-chapter', )

    @classmethod
    def process(cls, element, styles=(), reading_type=None, epub=None):
        me = cls()
        attrib = element.attrib
        me.reading_type = reading_type
        if 'id' in attrib:
            me.label = attrib['id']
        me.styles.extend(styles)
        captions = (u'Caption', u'Captions')
        sidebars_heads = (u'Caution-Warning-Heads ParaOverride-1',
                          u'Caution-Warning-Heads',
                          u'sidebars-heads ParaOverride-1',
                          u'sidebars-heads',
                          u'sidebar---header',
                          u'Safety-Alert-Box---Title',
                          u'Information-Box---Title',
                          u'WARNING---Title',
                          u'CAUTION---Title')
        sidebars_body = (u'Caution-Warning-Text ParaOverride-1',
                         u'Caution-Warning-Text',
                         u'sidebars-body-text ParaOverride-1',
                         u'sidebars-body-text',
                         u'sidebars-block-body-text',
                         u'Safety-Alert-Box---Body-Text',
                         u'Information-Box---Body-Text',
                         u'CAUTION---Body-Text',
                         u'WARNING---Body-Text')
        definition_list = (u'definition', 'GlossaryTerm')

        if 'class' in attrib:
            if any(s.lower() in attrib['class'].lower() for s in cls.term_list):
                if epub:
                    for child in element:
                        key = child.text
                        el_key = Run()
                        el_key.styles = ['bold']
                        el_key.add_child(TextNode(key))
                        me.add_child(el_key)
                        el_def = Run()
                        el_def = check_element_tail(el_def, child)
                        term_def = render_output(el_def)
                        me.add_child(el_def)
                        if key and term_def:
                            term_def = u'{}{}'.format(render_output(el_key), term_def)
                            epub.term_defs[key.strip()] = term_def
            elif attrib['class'] != "ParaOverride-1":
                me = check_element_text(me, element)
                me = check_child(me, element, epub)
                me = check_element_tail(me, element)
                if epub:
                    if u'Sub1' in attrib['class'] and epub.chapter_num == 'Index':
                        el = types.BlockQuote()
                        el.children = me.children
                        me = el
                    elif u'Sub2' in attrib['class'] and epub.chapter_num == 'Index':
                        el = types.BlockQuote()
                        el_2 = types.BlockQuote()
                        el_2.children = me.children
                        el.add_child(el_2)
                        me = el

                if any(s.lower() in attrib['class'].lower() for s in cls.sidebar_list):
                    sidebar_class = Sidebar()
                    if 'Case-History' in element.attrib['class']:
                        sidebar_class.title = u'Case History'
                    sidebar_class.children = me.children
                    me = sidebar_class
                elif 'c-head' in attrib['class'].lower():
                    el_main = Paragraph()
                    el = Run()
                    el.styles = ['bold', 'italic']
                    el.children = me.children
                    el_main.add_child(el)
                    me = el_main
                    check = render_output(me)
                    if u'What This Means to You'.lower() in check.lower():
                        el.styles = ['italic']
                        me.element_type = u'sidebars-heads'
                        if epub.epub_type == u'ifsta_rf':
                            el_sidebar = Sidebar()
                            el_sidebar.type = u'sidebar-head'
                            el_sidebar.title = me
                            me = el_sidebar
                elif 'Table-Title' in attrib['class']:
                    el = Run()
                    el.styles = ['bold']
                    el.children = me.children
                    me = el
                elif 'Table-Text' in attrib['class']:
                    el = Run()
                    el.children = me.children
                    me = el
                elif any(s.lower() in attrib['class'].lower() for s in cls.section_list):
                    me.styles.append('Section')
                    label = copy.deepcopy(me)
                    add_sectioning_label(me, label)
                elif any(s.lower() in attrib['class'].lower() for s in cls.subsection_list):
                    me.styles.append('Subsection')
                    label = copy.deepcopy(me)
                    add_sectioning_label(me, label)
                elif any(s.lower() in attrib['class'].lower() for s in cls.bullet_list):
                    new_item = Item()
                    bullet_class = UnorderedList()
                    new_item.children = me.children
                    bullet_class.children = [new_item]
                    me = bullet_class
                elif any(s.lower() in attrib['class'].lower() for s in sidebars_heads):
                    me.element_type = u'sidebars-heads'
                    if epub.epub_type == u'ifsta_rf':
                        el = Sidebar()
                        el.type = u'sidebar-head'
                        el.title = me
                        me = el
                elif any(s.lower() in attrib['class'].lower() for s in sidebars_body):
                    check_head = []
                    search_figure_icon_on_sidebar_body(me, check_head)
                    if check_head:
                        me.element_type = u'sidebars-heads'
                        if epub.epub_type == u'ifsta_rf':
                            el = Sidebar()
                            el.type = u'sidebar-head'
                            el.title = me
                            me = el
                    else:
                        me.element_type = u"sidebars-body"
                        update_sidebar_body_bullet(me)
                        me.add_child(types.TextNode("\n"))
                elif attrib['class'] in captions:
                    me.element_type = u'caption'
                    if epub is not None and epub.epub_type == u'ifsta':
                        token = get_caption_token(me.children[1]).rstrip()
                        me.children = me.children[2:]
                        epub.captions[token] = me
                    if epub is not None and epub.epub_type == u'ifsta_rf':
                        epub.caption_list.append(me)
                        me = Run()
                elif any(s.lower() in attrib['class'].lower() for s in definition_list):
                    sidebar = Sidebar()
                    sidebar.type = u"sidebar_term"
                    sidebar.children = me.children
                    el = Run()
                    el.add_child(sidebar)
                    el.add_child(types.TextNode("\n"))
                    me = el
                elif any(s.lower() in attrib['class'].lower() for s in cls.paragraph_list):
                    check_head = []
                    check_note = []
                    search_figure_icon_on_sidebar_body(me, check_head)
                    if check_head:
                        me.element_type = u'sidebars-heads'
                        if epub.epub_type == u'ifsta_rf':
                            el = Sidebar()
                            el.type = u'sidebar-head'
                            el.title = me
                            me = el
                    else:
                        check_note = search_span_note(me, check_note)
                        check_content = render_output(me)
                        if check_note or u'NOTE' in check_content or u'CAUTION' in check_content or u'WARNING' in check_content:
                            el = Sidebar()
                            el.options = u'css-class=note'
                            el.children = me.children
                            if u'NOTE' in check_content:
                                el.title = u'NOTE:'
                            elif u'CAUTION' in check_content:
                                el.title = u'CAUTION:'
                            elif u'WARNING' in check_content:
                                el.title = u'WARNING:'
                            me = el
                    # Handle some text styling in SKILL SHEET
                    if not check_head and not check_note:
                        para_class = attrib['class'] if 'class' in attrib else u''
                        para_class = u'p_%s' % para_class.replace('-', '_')
                        para_class = para_class.replace(u'Basic_Paragraph ', u'')
                        if epub is not None and para_class in epub.css_dict:
                            if 'textAlign' in epub.css_dict[para_class]:
                                if epub.css_dict[para_class]['textAlign'] == u'center':
                                    el = CenterNode()
                                    el.children = me.children
                                    me = el
                                elif epub.css_dict[para_class]['textAlign'] == u'left':
                                    if 'textIndent' in epub.css_dict[para_class]:
                                        if epub.css_dict[para_class]['textIndent'] == u'-45px':
                                            el = BlockQuote()
                                            el.children = me.children
                                            me = el
            else:
                add_basic_paragraph_children(me, element, epub)
        else:
            add_basic_paragraph_children(me, element, epub)
        return me


def add_basic_paragraph_children(node, element, epub):
    node = check_element_text(node, element)
    node = check_child(node, element, epub)
    node = check_element_tail(node, element)


def add_sectioning_label(node, label):
    new_label = Run()
    new_label.children = label.children
    node.label = new_label
    return node


def get_caption_token(root):
    if ITextNode.providedBy(root):
        return root
    elif hasattr(root, u'children'):
        for node in root:
            result = get_caption_token(node)
            if result:
                return result
    return False
