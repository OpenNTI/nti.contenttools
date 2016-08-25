#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: run_adapter.py 58552 2015-01-29 23:10:30Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml.html import HtmlComment
from .math_adapter import Math
from .image_adapter import Image
from ... import types
from ... import scoped_registry
import math

def adapt(fragment):
    head = fragment.find('head')
    body = fragment.find('body')
    epub_body = EPUBBody.process(body)
    return epub_body


class EPUBBody(types.EPUBBody):
    @classmethod
    def process(cls,element):
        me = cls()
        me = check_element_text(me, element)
        me = check_child(me, element)
        me = check_element_tail(me, element)
        return me    


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

class Sidebar(types.Sidebar):
    @classmethod
    def process(cls, element, sidebar_type=None):
        me = cls()
        if 'id' in element.attrib : me.label = element.attrib['id']
        me = check_element_text(me, element)
        me = check_child(me, element)
        me = check_element_tail(me, element)
        if me.title is None : 
            me.title = sidebar_type.title()
        return me

class Section( types.Section):
    @classmethod
    def process(cls, element):
        data_depth = element.attrib['data-depth'] if u'data-depth' in element.attrib  else None
        
        if data_depth == u'1': me = types.SubSection()
        elif data_depth == u'2' : me = types.SubSubSection()
        elif data_depth == u'3' : 
            me = Paragraph.process(element)
            return me
        else : 
            me = cls()
            logger.warn('Unhandled section data depth %s', data_depth)
        
        if u'id' in element.attrib : me.label = element.attrib['id']
        if u'class' in element.attrib : me.section_type = element.attrib['class']

        me = check_element_text(me, element)
        me = check_child(me, element)
        check_header = me.children[0]
        if isinstance(check_header, types.Paragraph):
            styles = set([u'Heading1', u'Heading2'])
            compare_list = set(check_header.styles)
            if styles.intersection(compare_list):
                me.title = check_header
                me.title.styles = []
                me.remove_child(check_header)
        me = check_element_tail(me, element)
        return me

class Paragraph( types.Paragraph ):
    @classmethod
    def process(cls, element, styles=(), reading_type=None):
        me = cls()
        me.reading_type = reading_type
        if 'id' in element.attrib : me.label = element.attrib['id']
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
                if any(substring in element.attrib['class'] for substring in sidebar_list):
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
                    new_item  = Item()
                    new_item.children = me.children
                    bullet_class.children = [new_item]
                    me = bullet_class
                elif element.attrib['class'] == u"sidebars-heads ParaOverride-1":
                    me.element_type = u'sidebars-heads'
                elif element.attrib['class'] == u"sidebars-body-text ParaOverride-1":
                    me.element_type = u"sidebars-body"
                    me.add_child(types.TextNode("\\\\\n"))
                elif element.attrib['class'] == u'definition ParaOverride-1':
                    blockquote = BlockQuote()
                    blockquote.children = me.children
                    el = Run()
                    el.add_child(blockquote)
                    el.add_child(types.TextNode("\\\\\n"))
                    me = el
                elif any(substring in element.attrib['class'] for substring in paragraph_list):
                    me.add_child(types.TextNode("\\\\\n"))
                    #from IPython.core.debugger import Tracer; Tracer()()
        else:
            me = check_element_text(me, element)
            me = check_child(me, element, reading_type)
            me = check_element_tail(me, element)
        return me

class Hyperlink( types.Hyperlink ):

    def __init__(self):
        self.type = 'Normal'

    @classmethod
    def process(cls, link):
        me = cls()
        me.target = link.attrib['href']
        if u'class' in link.attrib : 
            if link.attrib[u'class'] == u'autogenerated-content':
                me.type = u'Pageref'
                if u'/contents/' in me.target:
                    idx = me.target.find(u'#')
                    me.target = me.target[idx:]
                if u'#' in me.target :  me.target = me.target.replace(u'#', u'')
        if link.text:
            me.add_child(types.TextNode(link.text ) )
        for child in link:
            me.add_child( Run.process( child))
        return me

class OrderedList( types.OrderedList ):
    @classmethod
    def process(cls, element):
        me = cls()
        if 'data-number-style' in element.attrib:
            numbering_type = element.attrib['data-number-style']
            me.start = 1

            if numbering_type == u'1': me.format = 'decimal'
            elif u'lower-alpha' in  numbering_type : me.format = 'lowerLetter'
            elif u'upper-alpha' in numbering_type : me.format = 'upperLetter'
            elif u'lower-roman' in numbering_type : me.format = 'lowerRoman'
            elif u'upper-roman' in numbering_type : me.format = 'upperRoman'
            elif u'arabic' in numbering_type : me.format = 'decimal'
            else:
                logger.warn("UNHANDLED OrderedList numbering format type %s", numbering_type)

        for child in element:
            el = None
            if child.tag == 'li':
                el = Item.process(child)
            else:
                logger.info('OrderedList child %s',child.tag)
                el = Item()
            if isinstance(el, types.Item) or isinstance(el, types.List):
                me.add_child( el )
            else:
                if len(me.children) == 0:
                    me.add_child( Item() )
                me.children[-1].add_child( el )
        return me

class UnorderedList( types.UnorderedList ):
    @classmethod
    def process(cls, element):
        me = cls()
        if 'style' in element.attrib:
            numbering_style = element.attrib['style']
            me.start = 1
            if u'circle' in numbering_style: me.format = u'circ'
            elif u'disc' in numbering_style: me.format = u'bullet'
            elif u'square' in numbering_style: me.format = u'blacksquare'
            else:
                logger.warn("UNHANDLED UnorderedList numbering format type %s", numbering_style)
        for child in element:
            el = None
            if child.tag == 'li':
                el = Item.process(child, format=me.format)
            elif child.tag == 'div':
                el = _process_div_elements(child, me)
            elif child.tag == 'p':
                el = _process_p_elements(child)
            else:
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
    def process(cls, element, format=None):
        me = cls()
        me = check_element_text(me, element)
        me = check_child(me, element)
        me = check_element_tail(me, element)
        me.bullet_type = format
        return me

class Table(types.Table):
    @classmethod
    def process(cls, element):
        me = cls()
        if 'id' in element.attrib : me.label = element.attrib['id']
        me = check_element_text(me, element)
        style_ = u''
        if u'border' in element.attrib.keys():
            me.border = element.attrib[u'border']

        for child in element:
            if child.tag == 'colgroup':
                me.add_child(_process_colgroup_elements(child))
            elif child.tag == 'tbody':
                if me.border:
                    me.add_child(_process_tbody_elements(child, True))
                else:
                    me.add_child(_process_tbody_elements(child))
            elif child.tag == 'tr':
                me.add_child(Row.process(child, me.border))
            elif child.tag == 'thead':
                me.add_child(THead.process(child, me.border))
            elif child.tag == 'tfoot':
                me.add_child(TFoot.process(child))
            elif child.tag == 'caption':
                caption = Run.process(child)
                me.caption = caption
            else:
                if isinstance(child,HtmlComment): pass
                else:
                    logger.warn('Unhandled table child: %s.',child.tag)
        return me


class TBody(types.TBody):
    @classmethod
    def process(cls, element, border=None):
        me = cls()
        me.border = border
        number_of_col = 0 
        count_child = -1
        me = check_element_text(me, element)
        for child in element:
            if child.tag == 'tr':
                if me.border:
                    me.add_child(Row.process(child, me.border))
                else:
                    me.add_child(Row.process(child))
                number_of_col = me.children[count_child].number_of_col
                count_child = count_child + 1
            else:
                if isinstance(child,HtmlComment):
                    pass
                else:
                    logger.warn('Unhandled <tbody> child: %s.',child.tag)
        me.number_of_col = number_of_col
        return me

class THead(types.THead):  
    @classmethod
    def process(cls, element, border=None):
        me = cls()
        me.border = border
        number_of_col = 0 
        count_child = -1
        for child in element:
            if child.tag == 'tr':
                me.add_child(Row.process(child, border))
                number_of_col = me.children[count_child].number_of_col
                count_child = count_child + 1
            else:
                if isinstance(child,HtmlComment):
                    pass
                else:
                    logger.warn('Unhandled <thead> child: %s.',child.tag)
        me.number_of_col = number_of_col
        return me

class TFoot(types.TFoot):
    @classmethod
    def process(cls, element):
        me = cls()
        number_of_col = 0 
        count_child = -1
        for child in element:
            if child.tag == 'tr':
                me.add_child(Row.process(child))
                number_of_col = me.children[count_child].number_of_col
                count_child = count_child + 1
            else:
                if isinstance(child,HtmlComment): pass
                else:
                    logger.warn('Unhandled <tfoot> child: %s.',child.tag)
        me.number_of_col = number_of_col
        return me

class Row (types.Row):
    @classmethod
    def process(cls, element, border=None):
        me = cls()
        me.border = border
        number_of_col = 0
        me = check_element_text(me, element)
        for child in element:
            if child.tag == 'td' or child.tag == 'th':
                me.add_child(Cell.process(child, border))
                if number_of_col == 0:
                    me.children[0].is_first_cell_in_the_row = True
                number_of_col += 1
            else:
                if isinstance(child,HtmlComment):
                    pass
                else:
                    logger.warn('Unhandled <tr> child: %s.',child.tag)
        me.number_of_col = number_of_col
        return me

class Cell(types.Cell):
    @classmethod
    def process(cls, element, border = None):
        me = cls()
        me.border = border
        
        if u'valign' in element.attrib.keys():
            me.v_alignment = element.attrib[u'valign']

        if u'colspan' in element.attrib.keys():
            me.colspan = int(element.attrib[u'colspan'])

        if u'style' in element.attrib.keys():
            style = element.attrib[u'style']
            if u'text-align' in style:
                idx = style.find(u'text-align')
                text_align = style[idx:style.find(u';')]
                me.h_alignment = text_align[text_align.find(u':')+1:].strip()

        me = check_element_text(me, element)
        me = check_child(me, element)
        return me


def add_children_from_lists(node, list_of_child_types):
    for item in list_of_child_types:
        node.add_child(item)
    return node



def check_element_text(me, element):
    if element.text:
        if element.text.isspace(): 
            if len(element.text) == 1:
                me.add_child(types.TextNode(u' '))
            else:
                pass
        else:
            new_el_text = element.text
            me.add_child(types.TextNode(new_el_text))
    return me

def check_child(me, element, reading_type=None):
    for child in element:
        if child.tag == 'a':
            me.add_child(_process_a_elements(child))
        elif child.tag == 'b':
            me.add_child(_process_b_elements(child))
        elif child.tag == 'br':
            me.add_child( types.Newline() )
            if child.tail:
                me.add_child(types.TextNode(child.tail))    
        elif child.tag == 'i':
            me.add_child(_process_i_elements(child))
        elif child.tag == 'u' : 
            me.add_child(_process_u_elements(child))
        elif child.tag == 'span':
            me.add_child(_process_span_elements(child))
        elif child.tag == 'sub':
            me.add_child(_process_sub_elements(child))
        elif child.tag == 'sup':
            me.add_child(_process_sup_elements(child))
        elif child.tag == 'em' or child.tag == 'emphasis':
            me.add_child(_process_em_elements(child))
        elif child.tag == 'img':
            me.add_child(Image.process(child, reading_type))
        elif child.tag == 'h1':
            me.add_child(_process_h1_elements(child,reading_type))
        elif child.tag == 'h2':
            me.add_child(_process_h2_elements(child, reading_type))
        elif child.tag == 'h3':
            me.add_child(_process_h3_elements(child, reading_type))
        elif child.tag == 'h4':
            me.add_child(_process_h4_elements(child, reading_type))
        elif child.tag == 'h5':
            me.add_child(_process_h5_elements(child, reading_type))
        elif child.tag == 'h6':
            me.add_child(_process_h6_elements(child, reading_type))
        elif child.tag == 'h7':
            me.add_child(_process_h7_elements(child, reading_type))
        elif child.tag == 'ol':
            me.add_child(_process_ol_elements(child))
        elif child.tag == 'p':
            me.add_child(_process_p_elements(child, reading_type))
        elif child.tag == 'div':
            me.add_child(_process_div_elements(child, me))
        elif child.tag == 'ul':
            me.add_child(_process_ul_elements(child))
        elif child.tag == 'hr':
            me.add_child(_process_hr_elements(child))
        elif child.tag == 'big':
            me.add_child(_process_big_elements(child))
        elif child.tag == 'small':
            me.add_child(_process_small_elements(child))
        elif child.tag == 'table':
            me.add_child(_process_table_elements(child))
        elif child.tag == 'strong':
            me.add_child(_process_strong_elements(child))
        elif child.tag == 'dl':
            type_ = 'with_new_line'
            me.add_child(_process_strong_elements(child, type_))
        elif child.tag == 'li':
            me.add_child(Item.process(child))
        elif child.tag == 'pre':
            me.add_child(PreTag.process(child))
        elif child.tag == 'iframe' : 
            me.add_child(Iframe.process(child))
        elif child.tag == 'blockquote':
            me.add_child(BlockQuote.process(child))
        elif child.tag == 's':
            me.add_child(_process_s_elements(child))
        elif child.tag == 'figure':
            me.add_child(Figure.process(child))
        elif child.tag == 'section':
            me.add_child(Section.process(child))
        elif child.tag == 'math':
            me.add_child(Math.process(child))
        elif child.tag == 'code':
            from .code_adapter import Code
            me.add_child(Code.process(child))
        else:
            if isinstance(child,HtmlComment):
                pass
            else:
                logger.warn('Unhandled Run child: %s.',child)
    return me 
 
def check_element_tail(me, element):
    if element.tail:
            if element.tail.isspace(): pass
            else:
                new_el_tail = element.tail.rstrip() + u' '
                me.add_child(types.TextNode(new_el_tail))
    return me

def _process_p_elements( element, reading_type=None):
    el = Paragraph.process(element, [], reading_type)
    return el

def _process_section_elements(element, reading_type=None):
    el = Paragraph.process(element, [], reading_type)
    return el

def _process_h1_elements(element, reading_type=None):
    return Paragraph.process(element, ['Heading1'], reading_type)

def _process_h2_elements( element,reading_type=None ):
    return Paragraph.process(element,['Heading2'], reading_type)

def _process_h3_elements( element,reading_type=None ):
    return Paragraph.process(element, ['Heading3'], reading_type)

def _process_h4_elements( element,reading_type=None ):
    return Paragraph.process(element, ['Heading4'], reading_type)

def _process_h5_elements( element,reading_type=None):
    return Paragraph.process(element, ['Heading5'], reading_type)

def _process_h6_elements( element,reading_type=None):
    return Paragraph.process(element, ['Heading6'], reading_type)

def _process_h7_elements( element,reading_type=None):
    return Paragraph.process(element, ['Heading7'], reading_type)

def _process_span_elements( element ):
    span_class = element.attrib['class'] if u'class' in element.attrib else u''
    if 'bullet' in span_class:
        el = Run()
        el.element_type = 'bullet' 
    else:
        el = Run.process(element)
    return el

def process_span_list(element):
    table = Table()
    table.label = element.attrib[u'id'] if u'id' in element.attrib else None
    table.number_of_col = 3
    children = []
    for child in element:
        if child.tag == 'span':
            children.append(Run.process(child))
        else:
            logger.warn('Unhandled span list child : %s', child.tag)
    row = Row()
    row.number_of_col = table.number_of_col
    cell = Cell()
    cell.add_child(children[0])
    row.add_child(cell)
    for i in range(1,len(children)):
        cell = Cell()
        cell.add_child(children[i])
        if i % table.number_of_col == 0:
            table.add_child(row)
            row = Row()
            row.number_of_col = table.number_of_col
        row.add_child(cell)
    table.add_child(row)
    return table

def _process_ul_elements( element ):
    return UnorderedList.process(element)

def _process_dl_elements( element, type_=None ):
    return DescriptionList.process(element, type_)

def _process_b_elements( element ):
    return Run.process(element, ['bold'])

def _process_i_elements( element ):
    return Run.process(element, ['italic'])

def _process_u_elements( element ):
    return Run.process(element, ['underline'])

def _process_sub_elements( element ):
    return Run.process(element, ['sub'])

def _process_sup_elements( element ):
    return Run.process(element, ['sup'])

def _process_a_elements( element ):
    data_type = element.attrib[u'data-type'] if 'data-type' in element.attrib else u''
    if data_type == u'footnote-number':
        from .footnote_adapter import FootnoteMark
        el = FootnoteMark.process(element)
    else:
        if 'href' in element.attrib.keys():
            el = None
            if element.tail:
                el = Run()
                el.add_child( Hyperlink.process(element) )
                el.add_child( types.TextNode(element.tail))
            else:
                el = Hyperlink.process(element)
            return el
        else:
            el = None
            if element.tail:
                el = Run()
                el.add_child( types.TextNode(element.tail) )
    return el

def _process_strong_elements(element):
    return Run.process(element, ['bold'])

def _process_em_elements(element):
    return Run.process(element, ['italic'])

def _process_q_elements(element):
    return Run.process(element, ['bold'])

def _process_s_elements(element):
    return Run.process(element, ['strike'])

def _process_dfn_elements(child):
    return Run.process(element, 'italic')

def _process_samp_elements(element):
    return Run.process(element)

def _process_kbd_elements(element):
    return Run.process(element)

def _process_var_elements(element):
    return Run.process(element, ['italic']) 

def _process_hr_elements(element):
    return Run.process(element)

def _process_big_elements(element):
    return Run.process(element)

def _process_small_elements(element):
    return Run.process(element)

def _process_ol_elements(element):
    return OrderedList.process(element)

def _process_table_elements(element):
    return Table.process(element)

def _process_colgroup_elements(element):
    pass

def _process_tbody_elements(element, border=None):
    return TBody.process(element, border)

def _process_tr_elements(element):
    return Row.process(element)

def _process_td_elements(element):
    return Cell.process(element)

def _process_div_elements( element, parent):
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

class Iframe(types.Iframe):
    @classmethod
    def process(cls, element):
        me = cls()
        if 'id' in element.attrib : me.label = element.attrib['id']
        if u'src' in element.attrib : me.source = element.attrib[u'src']
        me = check_element_text(me, element)
        me = check_child(me , element)
        me = check_element_tail(me, element)
        return me

class BlockQuote(types.BlockQuote):
    @classmethod
    def process(cls, element):
        me = cls()
        if 'id' in element.attrib : me.label = element.attrib['id']
        me = check_element_text(me, element)
        me = check_child(me, element)
        me = check_element_tail(me, element)
        return me

class Figure(types.Figure):
    @classmethod
    def process(cls, element):
        me = cls()
        multi_figures = Run()
        if u'id' in element.attrib : me.label = element.attrib[u'id']
        for child in element:
            if child.tag == u'figcaption':
                me.caption = Run.process(child)
            elif child.tag == u'span':
                if u'data-type' in child.attrib : me.data_type = child.attrib[u'data-type']
                if u'id' in child.attrib : me.image_id = child.attrib[u'id']
                if u'data-alt' in child.attrib : me.image_alt = types.TextNode(child.attrib[u'data-alt'])
                img = get_figure_image(child)
                me.add_child(img)
            elif child.tag == u'figure':
                me.add_child(Figure.process(child))
            elif child.tag == u'div':
                me.add_child(_process_div_elements(child, me))
            else:
                logger.warn('Unhandled figure child %s', child.tag)
        return me

def get_figure_image(element):
    for child in element:
        if child.tag == u'img':
            return Image.process(child)


class PreTag(types.PreTag):
    @classmethod
    def process(cls, element):
        me = cls()
        data_type = element.attrib[u'data-type'] if u'data-type' in element.attrib else None
        me.label = element.attrib[u'id'] if u'id' in element.attrib else None
        me = check_element_text(me, element)
        me = check_child(me, element)
        me = check_element_tail(me, element)
        return me

