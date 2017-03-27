#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: docx_table.py 108562 2017-03-10 14:29:47Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IDocxTable
from nti.contenttools.types.interfaces import IDocxTRow
from nti.contenttools.types.interfaces import IDocxTCell

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(IDocxTable)
class DocxTable(DocumentStructureNode):
    createFieldProperties(IDocxTable)

    def __init__(self, *args, **kwargs):
        super(DocxTable, self).__init__(*args, **kwargs)


@interface.implementer(IDocxTRow)
class DocxTRow(DocumentStructureNode):
    createFieldProperties(IDocxTRow)

    def __init__(self, *args, **kwargs):
        super(DocxTRow, self).__init__(*args, **kwargs)


@interface.implementer(IDocxTCell)
class DocxTCell(DocumentStructureNode):
    createFieldProperties(IDocxTCell)

    def __init__(self, *args, **kwargs):
        super(DocxTCell, self).__init__(*args, **kwargs)
