#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
try:
    import cStringIO as StringIO
except:
    import StringIO

from ... import types

from PIL import Image as PILImage
from urlparse import urlparse

from lxml import etree


class Chapter( types.Chapter ):

    @classmethod
    def process(cls, element, epub):
        me = cls()
        me.add_child( Run.process(element, epub) )
        return me


class Section( types.Section ):

    @classmethod
    def process(cls, element, epub):
        me = cls()
        me.add_child( Run.process(element, epub) )
        return me


class SubSection( types.SubSection ):

    @classmethod
    def process(cls, element, epub):
        me = cls()
        me.add_child( Run.process(element, epub) )
        return me


class SubSubSection( types.SubSubSection ):

    @classmethod
    def process(cls, element, epub):
        me = cls()
        me.add_child( Run.process(element, epub) )
        return me


class Paragraph( types.Paragraph ):

    @classmethod
    def process(cls, element, epub):
        me = cls()

        if 'id' in element.attrib:
            me.add_child( Label.process( element, epub ) )

        if element.text:
            me.add_child( types.TextNode( element.text ) )

        for child in element:
            if child.tag == 'a':
                me.add_child( _process_a_elements( child, epub ) )
            elif child.tag == 'b':
                me.add_child( _process_b_elements( child, epub ) )
            elif child.tag == 'i':
                me.add_child( _process_i_elements( child, epub ) )
            elif child.tag == 'img':
                me.add_child( Image.process( child, epub ) )
            elif child.tag == 'p':
                me.add_child( _process_p_elements( child, epub ) )
            elif child.tag == 'span':
                me.add_child( _process_span_elements( child, epub ) )
            elif child.tag == 'sub':
                me.add_child( _process_sub_elements( child, epub ) )
            elif child.tag == 'video':
                me.add_child( Video.process( child, epub ) )
            else:
                print('Unhandled p child: %s' % child)

        if element.tail:
            me.add_child( types.TextNode( element.tail.replace('\r', '' ) ) )

        return me


class Run( types.Run ):

    @classmethod
    def process(cls, element, epub, styles=[]):
        me = cls()
        me.styles.extend(styles)

        if element.text:
            me.add_child( types.TextNode( element.text ) )

        for child in element:
            if child.tag == 'a':
                me.add_child( _process_a_elements( child, epub ) )
            elif child.tag == 'b':
                me.add_child( _process_b_elements( child, epub ) )
            elif child.tag == 'br':
                me.add_child( types.Newline() )
                me.add_child( types.TextNode( child.tail ) )
            elif child.tag == 'i':
                me.add_child( _process_i_elements( child, epub ) )
            elif child.tag == 'span':
                me.add_child( _process_span_elements( child, epub ) )
            elif child.tag == 'sub':
                me.add_child( _process_sub_elements( child, epub ) )
            else:
                print('Unhandled Run child: %s' % child)

        if element.tail:
            _t = cls()
            _t.add_child( me )
            _t.add_child( types.TextNode( element.tail.replace('\r', '' ) ) )
            me = _t

        return me


class Hyperlink( types.Hyperlink ):

    def __init__(self):
        self.type = 'Normal'

    @classmethod
    def process(cls, link, epub ):
        me = cls()

        me.target = link.attrib['href']

        if link.text:
            me.add_child( types.TextNode( link.text ) )

        for child in link:
            me.add_child( Run.process( child, epub ) )

        return me

class Label( types.Label ):

    @classmethod
    def process(cls, label, epub ):
        me = cls()
        me.name = label.attrib['id']
        return me


class Sidebar( types.Sidebar ):

    @classmethod
    def process(cls, element, epub):
        me = cls()

        for child in element:
            if child.tag == 'div':
                el = _process_div_elements( child, epub )
                if 'class' in child.attrib.keys() and 'title' in child.attrib['class']:
                    me.title = el
                else:
                    me.add_child( el )
            elif child.tag == 'p':
                me.add_child( _process_p_elements( child, epub ) )
            elif child.tag == 'ul':
                me.add_child( _process_ul_elements( child, epub ) )
            else:
                print('Unhandled Sidebar child: %s' % child)

        return me

class BlockQuote( types.BlockQuote ):

    @classmethod
    def process(cls, element, epub):
        me = cls()
        me.add_child( Paragraph.process( element, epub ) )
        return me

class Image( types.Image ):

    @classmethod
    def process(cls, element, epub):
        me = cls()
        me.path = element.attrib['src']
        me.caption = element.attrib['alt']
        me.data = StringIO.StringIO( epub.zipfile.read(os.path.join(epub.content_path, me.path)) )
        me.width, me.height = PILImage.open(me.data).size
        epub.image_list.append(me)
        return me

class Video( types.Video ):

    @classmethod
    def process(cls, element, epub):
        me = cls()
        me.path = element.attrib['src']
        me.caption = element.attrib['title']
        me.thumbnail = element.attrib['poster']
        me.thumbnaildata = StringIO.StringIO( epub.zipfile.read(os.path.join(epub.content_path, me.thumbnail)) )
        #me.width, me.height = PILImage.open(me.thumbnaildata).size
        me.width, me.height = ( 640, 480 )
        me.add_child( Run.process( element, epub ) )
        epub.video_list.append(me)
        return me

class UnorderedList( types.UnorderedList ):

    @classmethod
    def process(cls, element, epub):
        me = cls()

        for child in element:
            el = None
            if child.tag == 'li':
                el = Item.process(child, epub)
            elif child.tag == 'div':
                el = _process_div_elements(child, epub)
            elif child.tag == 'p':
                el = _process_p_elements(child, epub)
            else:
                print(child)
                el = Item()

            if isinstance(el, types.Item) or isinstance(el, types.List):
                me.add_child( el )
            else:
                if len(me.children) == 0:
                    me.add_child( Item() )
                me.children[-1].add_child( el )

        return me


class Item( types.Item ):

    @classmethod
    def process(cls, element, epub):
        me = None
        child = Run.process(element, epub)
        if isinstance(child, types.List):
            me = child
        else:
            me = cls()
            me.add_child( child )
        return me


def adapt( fragment, epub, label ):
    els = _process_fragment( fragment, epub )

    # Make sure that each chapter and section object have a Label child
    if els and (isinstance(els[0], Chapter) or isinstance(els[0], Section)):
        label_el = Label()
        label_el.name = label
        els[0].add_child( label_el )

    # Upgrade front and back matter 'sections' to 'chapters' as appropriate
    if els and isinstance(els[0], Section):
        if els[0].children[-1].name[0] in [ 'b', 'f' ] and len(els[0].children[-1].name) == 3:
            chapter = Chapter()
            for child in els[0].children:
                chapter.add_child(child)
            els[0] = chapter

    for el in els:
        _fix_hyperlinks( el, epub.manifest )

    return els

def _fix_hyperlinks( element, manifest ):

    if isinstance( element, Hyperlink ):
        hyperparts = urlparse( element.target )
        for item in manifest:
            if hyperparts[2] == manifest[item]['href']:
                element.type = u'Pageref'
                if hyperparts[5]:
                    element.target = hyperparts[5]
                else:
                    element.target = item
    else:
        if hasattr(element, 'children'):
            for child in element.children:
                _fix_hyperlinks( child, manifest )

def _process_fragment( fragment, epub ):
    head = fragment.find('head')
    body = fragment.find('body')

    el = []
    for element in body:
        if element.tag == 'div':
            el.append(_process_div_elements( element, epub ))
        elif element.tag == 'p':
            el.append(_process_p_elements( element, epub ))
        elif element.tag == 'h1':
            el.append(_process_h1_elements( element, epub ))
        elif element.tag == 'h2':
            el.append(_process_h2_elements( element, epub ))
        elif element.tag == 'ul':
            el.append(_process_ul_elements( element, epub ))
        else:
            print('Unhandled body child: %s' %  element )

    # Consolidate multi-line chapter or section titles
    new_el = []
    for i in range(len(el)):
        if (i+1 < len(el)) and type(el[i]) == type(el[i+1]):
            if type(el[i]) == Chapter or type(el[i]) == Section:
                el[i].add_child( types.TextNode(': ') )
                for child in el[i+1].children:
                    el[i].add_child( child )
                el[i+1] = el[i]
            else:
                new_el.append(el[i])
        else:
            new_el.append(el[i])
    el = new_el

    # If the chapter or section title was not parsed out of the text, then extract it from the document head.
    # Maybe we should do this all of the time.
    chapter = Chapter()
    chapter.suppressed = True
    chapter.add_child( types.TextNode( _get_title( head ) ) )
    if el is []:
        el.append(chapter)
    elif not ( (isinstance(el[0], Chapter) or isinstance(el[0], Section)) ):
        el.insert(0,chapter)

    # Consolidate list elements
    el = _consolidate_lists( el )

    return el

def _get_title( head ):
    title = u''
    for element in head:
        if element.tag == 'title':
            title = element.text
    return title

def _consolidate_lists( list = [] ):
    def pull_up_children( element ):
        if isinstance(element, types.List):
            for i in range(len(element.children)):
                if isinstance(element.children[i], types.List) and element.level == element.children[i].level:
                    child = element.children[i]
                    for j in range(len(child.children)):
                        element.children.insert(i+j, child.children[j])
                    element.children.remove(child)

    new_list = []
    for i in range(len(list)):
        if isinstance(list[i], types.List) and (i + 1 < len(list)) and isinstance(list[i+1], types.List) and list[i].group == list[i+1].group:
            if list[i].level == list[i+1].level:
                for child in list[i+1].children:
                    list[i].add_child( child )
                    list[i+1] = list[i]
            elif list[i].level < list[i+1].level:
                list[i].add_child( list[i+1] )
                list[i+1] = list[i]
            else:
                list[i].children = _consolidate_lists( list[i].children )
                # Pull up children if necessary
                pull_up_children( list[i] )
                new_list.append( list[i] )
        else:
            if isinstance(list[i], types.List):
                list[i].children = _consolidate_lists( list[i].children )
                # Pull up children if necessary
                pull_up_children( list[i] )
            new_list.append( list[i] )
    return new_list

def _process_div_elements( element, epub ):

    class_ = u''
    if 'class' in element.attrib.keys():
        class_ = element.attrib['class']

    el = None
    if class_ in [ 'figure' ]:
        el = Paragraph.process( element, epub )
    elif class_ in [ 'list' ]:
        el = UnorderedList.process( element, epub )
        el.format = 'None'
        el.level = 1
    elif class_ in [ 'feature1', 'feature2', 'feature3', 'feature4' ]:
        el = Sidebar.process( element, epub )
    elif class_ in [ 'featuretitle', 'feature1_title', 'feature2_title', 'feature3_title', 'feature4_title' ]:
        el = Run.process( element, epub )
    elif class_ in [ 'feature1_text', 'feature2_text', 'feature3_text', 'feature4_text' ]:
        el = Paragraph.process( element, epub )
    elif class_ in [ 'featurepara' ]:
        el = Paragraph.process( element, epub )
    elif class_ in [ 'top', 'dotted_top', 'bottom', 'dotted_bottom' ]:
        pass #ignored
    elif class_ in [ 'item1' ]:
        el = UnorderedList()
        el.format = 'None'
        el.level = 1
        el.add_child( Item.process( element, epub ) )
    elif class_ in [ 'item2' ]:
        el = UnorderedList()
        el.format = 'None'
        el.level = 2
        el.add_child( Item.process( element, epub ) )
    elif class_ in [ 'listpara1' ]:
        el = Paragraph.process( element, epub )
    elif class_ in [ 'index2' ]:
        el = UnorderedList()
        el.format = 'None'
        el.level = 2
        el.add_child( Item.process( element, epub ) )
    else:
        print(class_)

    return el


def _process_p_elements( element, epub ):
    class_ = u''
    if 'class' in element.attrib.keys():
        class_ = element.attrib['class']

    el = None
    if class_ in [ 'para', 'paraaftertitle', 'listhead', 'dedication', 'copyright', 'center' ]:
        el = Paragraph.process( element, epub )
    elif class_ in [ 'extractpara' ]:
        el = BlockQuote.process( element, epub )
    elif class_ in [ 'bibliographyentry' ]:
        el = Paragraph.process( element, epub )
    elif class_ in [ 'parttitle' ]:
        # Model as a 'chapter'
        el = Chapter.process( element, epub )
    elif class_ in [ 'chaptertitle', 'chaptersubtitle' ]:
        # Model as a 'section'
        el = Section.process( element, epub )
    elif class_ in [ 'figuresource', 'quotesource', 'featuresource' ]:
        el = Paragraph.process( element, epub )
    elif class_ == 'featureh1':
        el = Run.process( element, epub, styles=['bold'] )
    elif class_ == 'featureextract':
        el = BlockQuote.process( element, epub )
    elif class_ == 'av-caption':
        el = Paragraph.process( element, epub )
    elif class_ in [ 'mattertitle', 'toctitle' ]:
        el = SubSection.process( element, epub )
    elif class_ in [ 'index1', 'contentsparttitle' ]:
        el = UnorderedList()
        el.format = 'None'
        el.level = 1
        el.add_child( Item.process( element, epub ) )
    elif class_ == 'contentschaptertitle':
        el = UnorderedList()
        el.format = 'None'
        el.level = 2
        el.add_child( Item.process( element, epub ) )
    elif class_ == 'contentsh1':
        el = UnorderedList()
        el.format = 'None'
        el.level = 3
        el.add_child( Item.process( element, epub ) )
    elif class_ == 'av':
        el = Paragraph.process( element, epub )
    else:
        print( class_ )
        el = Paragraph()

    return el


def _process_h1_elements( element, epub ):
    # Model as a subsection
    return SubSection.process(element, epub)

def _process_h2_elements( element, epub ):
    # Model as a subsubsection
    return SubSubSection.process(element, epub)

def _process_span_elements( element, epub ):
    return Run.process(element, epub)

def _process_ul_elements( element, epub ):
    return UnorderedList.process(element, epub)

def _process_b_elements( element, epub ):
    return Run.process(element, epub, ['bold'])

def _process_i_elements( element, epub ):
    return Run.process(element, epub, ['italic'])

def _process_sub_elements( element, epub ):
    return Run.process(element, epub, ['sub'])

def _process_a_elements( element, epub ):
    if 'href' in element.attrib.keys():
        el = None
        if element.tail:
            el = Run()
            el.add_child( Hyperlink.process(element, epub) )
            el.add_child( types.TextNode(element.tail) )
        else:
            el = Hyperlink.process(element, epub)
        return el
    else:
        el = None
        if element.tail:
            el = Run()
            el.add_child( Label.process(element, epub) )
            el.add_child( types.TextNode(element.tail) )
        else:
            el = Label.process(element, epub)
        return el

