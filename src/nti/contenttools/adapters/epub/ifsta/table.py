#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml.html import HtmlComment

from nti.contenttools import types

from nti.contenttools.adapters.epub.ifsta.run import Run

from nti.contenttools.adapters.epub.ifsta import check_child
from nti.contenttools.adapters.epub.ifsta import check_element_text
from nti.contenttools.adapters.epub.ifsta import check_element_tail


class Table(types.Table):

    @classmethod
    def process(cls, element, epub=None):
        me = cls()
        me.border = True
        me = check_element_text(me, element)
        me.number_of_col_body = 0

        for child in element:
            if child.tag == 'colgroup':
                pass
            elif child.tag == 'tbody':
                me.add_child(TBody.process(child, me.border, epub))
            elif child.tag == 'tr':
                row = Row.process(child, me.border)
                me.add_child(row)
                if row.number_of_col > me.number_of_col_body:
                    me.number_of_col_body = row.number_of_col
            elif child.tag == 'thead':
                me.add_child(THead.process(child, me.border, epub))
            elif child.tag == 'tfoot':
                me.add_child(TFoot.process(child, epub))
            elif child.tag == 'caption':
                caption = Run.process(child, epub=epub)
                me.caption = caption
            elif not isinstance(child, HtmlComment):
                logger.warn('Unhandled %s child: %s.', element, child)
        return me


class TBody(types.TBody):

    @classmethod
    def process(cls, element, border=None, epub=None):
        me = cls()
        me.border = border
        number_of_col = 0
        count_child = -1
        me = check_element_text(me, element)
        for child in element:
            if child.tag == 'tr':
                if me.border:
                    me.add_child(Row.process(child, me.border, epub))
                else:
                    me.add_child(Row.process(child, False, epub))
                number_of_col = me.children[count_child].number_of_col
                count_child = count_child + 1
            elif not isinstance(child, HtmlComment):
                logger.warn('Unhandled <tbody> child: %s.', child.tag)
        me.number_of_col = number_of_col
        return me


class THead(types.THead):

    @classmethod
    def process(cls, element, border=None, epub=None):
        me = cls()
        me.border = border
        number_of_col = 0
        count_child = -1
        for child in element:
            if child.tag == 'tr':
                me.add_child(Row.process(child, border, epub))
                number_of_col = me.children[count_child].number_of_col
                count_child = count_child + 1
            elif not isinstance(child, HtmlComment):
                logger.warn('Unhandled <thead> child: %s.', child.tag)
        me.number_of_col = number_of_col
        return me


class TFoot(types.TFoot):

    @classmethod
    def process(cls, element, epub=None):
        me = cls()
        number_of_col = 0
        count_child = -1
        for child in element:
            if child.tag == 'tr':
                me.add_child(Row.process(child, False, epub))
                number_of_col = me.children[count_child].number_of_col
                count_child = count_child + 1
            else:
                if isinstance(child, HtmlComment):
                    pass
                else:
                    logger.warn('Unhandled <tfoot> child: %s.', child.tag)
        me.number_of_col = number_of_col
        return me


class Row (types.Row):

    @classmethod
    def process(cls, element, border=None, epub=None):
        me = cls()
        me.border = border
        number_of_col = 0
        me = check_element_text(me, element)
        for child in element:
            if child.tag == 'td' or child.tag == 'th':
                me.add_child(Cell.process(child, border, epub))
                if number_of_col == 0:
                    me.children[0].is_first_cell_in_the_row = True
                number_of_col += 1
            elif not isinstance(child, HtmlComment):
                logger.warn('Unhandled <tr> child: %s.', child.tag)
        me.number_of_col = number_of_col
        return me


class Cell(types.Cell):

    @classmethod
    def process(cls, element, border=None, epub=None):
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
                me.h_alignment = text_align[text_align.find(u':') + 1:].strip()

        me = check_element_text(me, element)
        me = check_child(me, element, epub)
        me = check_element_tail(me, element)
        update_cell_elements(me)
        return me


def update_cell_elements(cell):
    num = len(cell.children)
    if num > 1:
        for i, child in enumerate(cell):
            if i < num - 1 :
                child.add(types.TextNode(u'\n'))
                child.add(types.TextNode(u'\\newline'))
                child.add(types.TextNode(u'\n'))
    return cell
