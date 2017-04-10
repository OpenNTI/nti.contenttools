#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: paragraph.py 106706 2017-02-16 01:07:01Z carlos.sanchez $
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


class Paragraph(types.Paragraph):

    @classmethod
    def process(cls, element, styles=(), reading_type=None):
        me = cls()
        me.reading_type = reading_type
        if 'id' in element.attrib:
            me.label = element.attrib['id']
        me.styles.extend(styles)
        if u'class' in element.attrib:
            if element.attrib['class'] == u"ParaOverride-1":
                pass
            else:
                me = check_element_text(me, element)
                me = check_child(me, element, reading_type)
                me = check_element_tail(me, element)
                paragraph_list = [u'Body-Text', u'Block-Text', 'ParaOverride']
                section_list = [u'A-Head', u'A-HEAD']
                subsection_list = [u'B-HEAD ParaOverride-1', u'B-Head']
                sidebar_list = [u'Case-History ParaOverride-1']
                bullet_list = [u'Bullet ParaOverride-1']
                if any(substring in element.attrib['class']
                       for substring in sidebar_list):
                    sidebar_class = Sidebar()
                    if u'Case-History' in element.attrib['class']:
                        sidebar_class.title = u'Case History'
                    sidebar_class.children = me.children
                    me = sidebar_class
                elif any(substring in element.attrib['class'] for substring in section_list):
                    me.styles.append('Section')
                elif any(substring in element.attrib['class'] for substring in subsection_list):
                    me.styles.append('Subsection')
                elif any(substring in element.attrib['class'] for substring in bullet_list):
                    bullet_class = UnorderedList()
                    new_item = Item()
                    new_item.children = me.children
                    bullet_class.children = [new_item]
                    me = bullet_class
                elif element.attrib['class'] == u"sidebars-heads ParaOverride-1":
                    me.element_type = u'sidebars-heads'
                elif element.attrib['class'] == u"sidebars-body-text ParaOverride-1":
                    me.element_type = u"sidebars-body"
                    me.add_child(types.TextNode("\\\\\n"))
                elif element.attrib['class'] == u'definition ParaOverride-1':
                    sidebar = Sidebar()
                    sidebar.type = u"sidebar_term"
                    sidebar.children = me.children
                    el = Run()
                    el.add_child(sidebar)
                    el.add_child(types.TextNode("\\\\\n"))
                    me = el
                elif any(substring in element.attrib['class'] for substring in paragraph_list):
                    me.add_child(types.TextNode("\\\\\n"))
        else:
            me = check_element_text(me, element)
            me = check_child(me, element, reading_type)
            me = check_element_tail(me, element)
        return me
