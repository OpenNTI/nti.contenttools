#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IFootnote
from nti.contenttools.types.interfaces import IFootnoteText
from nti.contenttools.types.interfaces import IFootnoteMark

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(IFootnote)
class Footnote(DocumentStructureNode):
    createFieldProperties(IFootnote)


@interface.implementer(IFootnoteText)
class FootnoteText(DocumentStructureNode):
    createFieldProperties(IFootnoteText)


@interface.implementer(IFootnoteMark)
class FootnoteMark(DocumentStructureNode):
    createFieldProperties(IFootnoteMark)
