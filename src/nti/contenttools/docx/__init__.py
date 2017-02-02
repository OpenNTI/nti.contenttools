#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import properties as docx

from ..types import _Node
from ..types import *

# These classes encapsulate WordprocessingML structures


class _DocxStructureElement(_Node):
    STYLES = {}

    def __init__(self):
        super(_DocxStructureElement, self).__init__()
        self.styles = []

    def raw(self):
        val = u''
        for child in self.children:
            if hasattr(child, 'raw'):
                val = val + child.raw()
            else:
                val = val + child
        return val

    def addStyle(self, style):
        self.styles.append(style)

    def removeStyle(self, style):
        self.styles.remove(style)


def process_border(border):

    def process_attributes(attributes):
        attribs = {}
        if '{' + docx.nsprefixes['w'] + '}color' in attributes.keys():
            attribs['color'] = attributes['{' + docx.nsprefixes['w'] + '}color'] or None
        if '{' + docx.nsprefixes['w'] + '}frame' in attributes.keys():
            attribs['frame'] = attributes['{' + docx.nsprefixes['w'] + '}frame']
        if '{' + docx.nsprefixes['w'] + '}shadow' in attributes.keys():
            attribs['shadow'] = attributes['{' + docx.nsprefixes['w'] + '}shadow'] or None
        if '{' + docx.nsprefixes['w'] + '}space' in attributes.keys():
            attribs['space'] = attributes['{' + docx.nsprefixes['w'] + '}space'] or None
        if '{' + docx.nsprefixes['w'] + '}sz' in attributes.keys():
            attribs['sz'] = attributes['{' + docx.nsprefixes['w'] + '}sz'] or None
        if '{' + docx.nsprefixes['w'] + '}themeColor' in attributes.keys():
            attribs['themeColor'] = attributes[
                '{' + docx.nsprefixes['w'] + '}themeColor'] or None
        if '{' + docx.nsprefixes['w'] + '}themeShade' in attributes.keys():
            attribs['themeShade'] = attributes[
                '{' + docx.nsprefixes['w'] + '}themeShade'] or None
        if '{' + docx.nsprefixes['w'] + '}themeTint' in attributes.keys():
            attribs['themeTint'] = attributes[
                '{' + docx.nsprefixes['w'] + '}themeTint'] or None
        if '{' + docx.nsprefixes['w'] + '}val' in attributes.keys():
            attribs['val'] = attributes['{' + docx.nsprefixes['w'] + '}val'] or None
        return attribs

    borders = {}
    for element in border.iterchildren():
        if element.tag == '{' + docx.nsprefixes['w'] + '}bottom':
            borders['bottom'] = process_attributes(element.attrib)
        elif element.tag == '{' + docx.nsprefixes['w'] + '}end':
            borders['end'] = process_attributes(element.attrib)
        elif element.tag == '{' + docx.nsprefixes['w'] + '}insideH':
            borders['insideH'] = process_attributes(element.attrib)
        elif element.tag == '{' + docx.nsprefixes['w'] + '}insideV':
            borders['insideV'] = process_attributes(element.attrib)
        elif element.tag == '{' + docx.nsprefixes['w'] + '}start':
            borders['start'] = process_attributes(element.attrib)
        elif element.tag == '{' + docx.nsprefixes['w'] + '}top':
            borders['top'] = process_attributes(element.attrib)
        elif element.tag == '{' + docx.nsprefixes['w'] + '}left':
            borders['left'] = process_attributes(element.attrib)
        elif element.tag == '{' + docx.nsprefixes['w'] + '}right':
            borders['right'] = process_attributes(element.attrib)
        else:
            print(element.tag)

    return borders
