#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: code.py 108562 2017-03-10 14:29:47Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IAlternateContent
from nti.contenttools.types.interfaces import ITextBoxContent

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties

@interface.implementer(IAlternateContent)
class AlternateContent(DocumentStructureNode):
    createFieldProperties(IAlternateContent)

    def __init__(self, *args, **kwargs):
        super(AlternateContent, self).__init__(*args, **kwargs)
        

@interface.implementer(ITextBoxContent)
class TextBoxContent(DocumentStructureNode):
    createFieldProperties(ITextBoxContent)

    def __init__(self, *args, **kwargs):
        super(TextBoxContent, self).__init__(*args, **kwargs)

