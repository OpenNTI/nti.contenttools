#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IDocument

from nti.contenttools.types.node import DocumentStructureNode


@interface.implementer(IDocument)
class Document(DocumentStructureNode):

    packages = ['graphicx',
                'hyperref',
                'ulem',
                'ntilatexmacros',
                'ntiassessment',
                'amsmath',
                'enumitem',
                'listings',
                'ntiglossary',
                'Tabbing',
                'textgreek']

    title = ''
    author = ''
    
    def __init__(self, doc_type=u'book'):
        DocumentStructureNode.__init__(self)
        self.doc_type = doc_type or u'book'
