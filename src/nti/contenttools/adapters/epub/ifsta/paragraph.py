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

from nti.contenttools.adapters.epub.ifsta.run import Run

from nti.contenttools.adapters.epub.ifsta.note import Sidebar

from nti.contenttools.adapters.epub.ifsta.lists import Item
from nti.contenttools.adapters.epub.ifsta.lists import UnorderedList

from nti.contenttools.types.interfaces import ITextNode


class Paragraph(types.Paragraph):

    bullet_list = (u'Bullet ParaOverride-1', u'Bullet')
    bold_italic_text = ('C-Head ParaOverride-1', 'C-Head')
    sidebar_list = (u'Case-History ParaOverride-1',)
    subsection_list = (u'B-HEAD ParaOverride-1', u'B-Head', u'B-HEAD')
    section_list = (u'A-Head', u'A-HEAD', 'A-HEAD ParaOverride-1',)
    paragraph_list = (u'Body-Text', u'Block-Text', 'ParaOverride',)

    @classmethod
    def process(cls, element, styles=(), reading_type=None, epub=None):
        me = cls()
        attrib = element.attrib
        me.reading_type = reading_type
        if 'id' in attrib:
            me.label = attrib['id']
        me.styles.extend(styles)
        captions = (u'Caption ParaOverride-1', u'Caption', )
        sidebars_heads = (u'Caution-Warning-Heads ParaOverride-1',
                          u'Caution-Warning-Heads',
                          u'sidebars-heads ParaOverride-1',
                          u'sidebars-heads',)
        sidebars_body = (u'Caution-Warning-Text ParaOverride-1',
                         u'Caution-Warning-Text',
                         u'sidebars-body-text ParaOverride-1',
                         u'sidebars-body-text',)
        definition_list = (u'definition', 'GlossaryTerm')

        if u'class' in attrib:
            if attrib['class'] != u"ParaOverride-1":
                me = check_element_text(me, element)
                me = check_child(me, element, epub)
                me = check_element_tail(me, element)
                if any(s in attrib['class'] for s in cls.sidebar_list):
                    sidebar_class = Sidebar()
                    if u'Case-History' in element.attrib['class']:
                        sidebar_class.title = u'Case History'
                    sidebar_class.children = me.children
                    me = sidebar_class
                elif u'C-Head' in attrib['class']:
                    el_main = Paragraph()
                    el = Run()
                    el.styles = ['bold', 'italic']
                    el.children = me.children
                    el_main.add_child(el)
                    el_main.add_child(types.TextNode("\\\\\n"))
                    me = el_main
                elif u'Table-Title' in attrib['class']:
                    el = Run()
                    el.styles = ['bold']
                    el.children = me.children
                    me = el
                elif u'Table-Text' in attrib['class']:
                    el = Run()
                    el.children = me.children
                    me = el
                elif any(s in attrib['class'] for s in cls.section_list):
                    me.styles.append('Section')
                    add_sectioning_label(me)
                elif any(s in attrib['class'] for s in cls.subsection_list):
                    me.styles.append('Subsection')
                    add_sectioning_label(me)
                elif any(s in attrib['class'] for s in cls.bullet_list):
                    new_item = Item()
                    bullet_class = UnorderedList()
                    new_item.children = me.children
                    bullet_class.children = [new_item]
                    me = bullet_class
                elif any(s in attrib['class'] for s in sidebars_heads):
                    me.element_type = u'sidebars-heads'
                    if epub.epub_type == u'ifsta_rf':
                        el = Sidebar()
                        el.type = u'sidebar-head'
                        el.title = me
                        me = el
                elif any(s in attrib['class'] for s in sidebars_body):
                    me.element_type = u"sidebars-body"
                    me.add_child(types.TextNode("\\\\\n"))
                elif attrib['class'] in captions:
                    me.element_type = u'caption'
                    if epub is not None and epub.epub_type == u'ifsta':
                        token = get_caption_token(me.children[1]).rstrip()
                        me.children = me.children[2:]
                        epub.captions[token] = me
                    if epub is not None and epub.epub_type == u'ifsta_rf':
                        epub.caption_list.append(me)
                        me = Run()
                elif any(s in attrib['class'] for s in definition_list):
                    sidebar = Sidebar()
                    sidebar.type = u"sidebar_term"
                    sidebar.children = me.children
                    el = Run()
                    el.add_child(sidebar)
                    el.add_child(types.TextNode("\n"))
                    me = el
                elif any(s in attrib['class'] for s in cls.paragraph_list):
                    pass
            else:
                me = check_element_text(me, element)
                me = check_child(me, element, epub)
                me = check_element_tail(me, element)
        else:
            me = check_element_text(me, element)
            me = check_child(me, element, epub)
            me = check_element_tail(me, element)
        return me


def add_sectioning_label(node):
    label = Run()
    label.children = node.children
    node.label = label
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
