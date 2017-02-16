#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division

__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IRow
from nti.contenttools.types.interfaces import ICell
from nti.contenttools.types.interfaces import ITBody
from nti.contenttools.types.interfaces import ITHead
from nti.contenttools.types.interfaces import ITFoot
from nti.contenttools.types.interfaces import ITable

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(ITable)
class Table(DocumentStructureNode):
    createFieldProperties(ITable)

    def set_number_of_col_header(self, number_of_col_header):
        self.number_of_col_header = number_of_col_header

    def set_number_of_col_body(self, number_of_col_body):
        self.number_of_col_body = number_of_col_body

    def set_caption(self, caption):
        self.caption = caption

    def set_label(self, label):
        self.label = label

    def set_border(self, border):
        self.border = border

    def set_type(self, type_):
        self.type_ = type_

    def set_alignment(self, alignment):
        self.alignment = alignment


@interface.implementer(IRow)
class Row(DocumentStructureNode):
    createFieldProperties(IRow)

    def set_number_of_col(self, number_of_col):
        self.number_of_col = number_of_col

    def set_border(self, border):
        self.border = border

    def set_type(self, type_):
        self.type_ = type_


@interface.implementer(ICell)
class Cell(DocumentStructureNode):
    createFieldProperties(ICell)

    def set_border(self, border):
        self.border = border


@interface.implementer(ITBody)
class TBody(DocumentStructureNode):
    createFieldProperties(ITBody)

    def set_number_of_col(self, number_of_col):
        self.number_of_col = number_of_col

    def set_border(self, border):
        self.border = border


@interface.implementer(ITHead)
class THead(DocumentStructureNode):
    createFieldProperties(ITHead)

    def set_number_of_col(self, number_of_col):
        self.number_of_col = number_of_col

    def set_border(self, border):
        self.border = border


@interface.implementer(ITFoot)
class TFoot(DocumentStructureNode):
    createFieldProperties(ITFoot)

    def set_number_of_col(self, number_of_col):
        self.number_of_col = number_of_col
