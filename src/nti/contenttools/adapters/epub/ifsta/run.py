#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: run.py 106706 2017-02-16 01:07:01Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools import types

from nti.contenttools.adapters.epub.ifsta import check_child
from nti.contenttools.adapters.epub.ifsta import check_element_text

from nti.contenttools.adapters.epub.ifsta.lists import UnorderedList
from nti.contenttools.adapters.epub.ifsta.lists import Item

from nti.contenttools.adapters.epub.ifsta.note import Sidebar

class Run( types.Run ):
    @classmethod
    def process(cls, element, styles=[], reading_type=None):
        me = cls()
        if 'id' in element.attrib : me.label = element.attrib['id']
        me.styles.extend(styles)
        me = check_element_text(me, element)
        me = check_child(me, element, reading_type)
        if element.tail:
            _t = cls()
            _t.add_child( me )
            _t.add_child( types.TextNode( element.tail.replace('\r', '' ) ) )
            me = _t
        return me

def process_div_elements( element, parent):
    class_type = element.attrib['class'] if 'class' in element.attrib else None
    el = Run.process(element)
    if class_type is None:
        pass
    else:
        if class_type == u"Basic-Text-Frame":
            el.element_type = u"Basic-Text-Frame"
            #need to check if there the div has sidebar-head and sidebar-text
            caption = Run()
            body_text = Run()
            caption, body_text = examine_div_element_for_sidebar(el, caption, body_text)
            if len(caption.children) > 0 and len(body_text.children) > 0:
                new_el  = Sidebar()
                new_el.title  = caption
                new_el.children = body_text.children
                el = new_el
    return el

def examine_div_element_for_sidebar(el, caption, body_text):   
    for child in el.children:
        if isinstance(child, types.Paragraph):
            if child.element_type == u'sidebars-heads':
                caption.add_child(child)
            elif child.element_type == u'sidebars-body':
                check_list = check_paragraph_bullet(child)
                if check_list:
                    bullet_class = UnorderedList()
                    new_item  = Item()
                    new_item.children = [child]
                    bullet_class.children = [new_item]
                    body_text.add_child(bullet_class)
                else:
                    body_text.add_child(child)
        elif isinstance(child, Run):
            caption, body_text = examine_div_element_for_sidebar(child, caption, body_text)
    return caption, body_text

def check_paragraph_bullet(el):
    for child in el.children:
        if isinstance(child, types.Run):
            if child.element_type == 'bullet':
                return True
    return False