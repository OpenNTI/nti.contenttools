#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IBody
from nti.contenttools.types.interfaces import IDocument
from nti.contenttools.types.interfaces import IEPUBBody

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(IDocument)
class Document(DocumentStructureNode):
    createFieldProperties(IDocument)

    packages = ('graphicx',
                'hyperref',
                'ulem',
                'ntilatexmacros',
                'ntiassessment',
                'amsmath',
                'enumitem',
                'listings',
                'ntiglossary',
                'Tabbing',
                'textgreek')

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.title = self.title or u''
        self.author = self.author or u''
        self.doc_type = self.doc_type or u'book'
        if not self.packages:
            self.packages = list(Document.packages)


@interface.implementer(IBody)
class Body(DocumentStructureNode):
    createFieldProperties(IBody)


@interface.implementer(IEPUBBody)
class EPUBBody(DocumentStructureNode):
    createFieldProperties(IEPUBBody)
