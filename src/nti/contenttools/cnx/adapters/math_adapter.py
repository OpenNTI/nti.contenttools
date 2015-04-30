#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: math_adapter.py 58552 2015-01-29 23:10:30Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ... import types
from lxml.html import HtmlComment

class Math(types.Math):
    @classmethod
    def process(cls, element):
        me = cls()
        if 'display' in element.attrib : me.equation_type = element.attrib['display']
        logger.info(me.equation_type)
        me.add_child(MathRun.process(element))
        return me

class MRow(types.MRow):
    @classmethod
    def process(cls, element):
        me = cls()
        me = check_math_element_child(me, element)
        return me

class MFenced(types.MFenced):
    @classmethod
    def process(cls, element):
        me = cls()
        me.close = element.attrib['close']
        me.opener = element.attrib['open']
        me.separators = element.attrib['separators']
        for child in element:
            if child.tag == 'mtable':
                me.add_child(_process_mtable_elements(child))
            elif child.tag == 'mrow':
                me.add_child(_process_mrow_elements(child))
            else:
                me.add_child(MathRun.process(element))
        return me

class Mtable(types.Mtable):
    @classmethod
    def process(cls, element):
        me = cls()
        number_of_col = 0 
        count_child = -1
        if 'id' in element.attrib:
            me.add_child(Label.process(element))

        if element.text:
            if element.text.isspace():
                pass
            else:
                me.add_child(types.TextNode(element.text, type_text = 'omath'))

        for child in element:
            if child.tag == 'mtr':
                me.add_child(_process_mtr_elements(child))
                number_of_col = me.children[count_child].number_of_col 
            else:
                logger.warn("UNHANDLED child under TABLE element %s", child.tag)
            count_child = count_child + 1
        me.set_number_of_col(number_of_col)
        return me

class Mtr(types.Mtr):
    @classmethod
    def process(cls, element):
        me = cls()
        number_of_col = 0
        if 'id' in element.attrib:
            me.add_child(Label.process(element))

        if element.text:
            if element.text.isspace():
                pass
            else:
                me.add_child(types.TextNode(element.text, type_text = 'omath'))

        for child in element:
            if child.tag == 'mtd':
                me.add_child(_process_mtd_elements(child))
                number_of_col = number_of_col + 1
            else:
                logger.warn("UNHANDLED child under TABLE element %s", child.tag)
        me.set_number_of_col(number_of_col)
        return me

class Mtd(types.Mtd):
    @classmethod
    def process(cls, element):
        me = cls()
        me.add_child(MathRun.process(element))
        return me

class Mfrac (types.Mfrac):
    @classmethod
    def process(cls, element):
        me = cls()
        if 'id' in element.attrib:
            me.add_child(Label.process(element))

        if element.text:
            if element.text.isspace():
                pass
            else:
                me.add_child(types.TextNode(element.text, type_text = 'omath'))

        for child in element:
            if child.tag == 'mrow':
                me.add_child(_process_mrow_elements(child))
            else:
                logger.warn("UNHANDLED child under TABLE element %s", child.tag)
        return me

class MSup (types.MSup):
    @classmethod
    def process(cls, element):
        me = cls()
        me.add_child(MathRun.process(element))
        return me

class MSub (types.MSub):
    @classmethod
    def process(cls, element):
        me = cls()
        me.add_child(MathRun.process(element))
        return me

class MSubSup(types.MSubSup):
    @classmethod
    def process(cls, element):
        me = cls()
        me.add_child(MathRun.process(element))
        return me

class MSqrt(types.Msqrt):
    @classmethod
    def process(cls, element):
        me = cls()
        me.add_child(MathRun.process(element))
        return me

class MRoot(types.Mroot):
    @classmethod
    def process(cls, element):
        me = cls()
        me.add_child(MathRun.process(element))
        return me

class MUnder(types.MUnder):
    @classmethod
    def process(cls, element):
        me = cls()
        me.add_child(MathRun.process(element))
        return me

class MUnderover(types.MUnderover):
    @classmethod
    def process(cls, element):
        me = cls()
        me.add_child(MathRun.process(element))
        return me

class MOver(types.MOver):
    @classmethod
    def process(cls, element):
        me = cls()
        me.add_child(MathRun.process(element))
        return me

class MathRun(types.MathRun):
    @classmethod
    def process(cls, element, styles=[]):
        me = cls()
        me.styles.extend(styles)
        if element.text:
            if element.text.isspace():
                pass
            else:
                me.add_child(types.TextNode(element.text, type_text = 'omath'))
        me = check_math_element_child(me, element)
        return me

def check_math_element_child(me, element):
    for child in element:
        if child.tag == 'mi':
            me.add_child(_process_mi_elements(child))
        elif child.tag == 'mo':
            me.add_child(_process_mo_elements(child))
        elif child.tag == 'mn':
            me.add_child(_process_mn_elements(child))
        elif child.tag == 'mrow':
            me.add_child(_process_mrow_elements(child))
        elif child.tag == 'msup':
            me.add_child(_process_msup_elements(child))
        elif child.tag == 'msub':
            me.add_child(_process_msub_elements(child))
        elif child.tag == 'mfenced':
            me.add_child(_process_mfenced_elements(child))
        elif child.tag == 'mspace':
            pass
        elif child.tag == 'msubsup':
            me.add_child(_process_msubsup_elements(child))
        elif child.tag == 'mfrac':
            me.add_child(_process_mfrac_elements(child))
        elif child.tag == 'mover':
            me.add_child(_process_mover_elements(child))
        elif child.tag == 'mtable':
            me.add_child(_process_mtable_elements(child))
        elif child.tag == 'msqrt':
            me.add_child(_process_msqrt_elements(child))
        elif child.tag == 'mroot':
            me.add_child(_process_mroot_elements(child))
        elif child.tag == 'mtext':
            me.add_child(_process_mtext_elements(child))
        elif child.tag == 'munderover':
            me.add_child(_process_munderover_elements(child))
        elif child.tag == 'munder':
            me.add_child(_process_munder_elements(child))
        elif child.tag == 'mstyle':
            pass
        else:
            logger.warn("UNHANDLED  math element: %s", child.tag)
    return me