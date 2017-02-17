#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: paragraph.py 106646 2017-02-15 19:47:11Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import ICNXCollection
from nti.contenttools.types.interfaces import ICNXSubcollection
from nti.contenttools.types.interfaces import ICNXContent
from nti.contenttools.types.interfaces import ICNXModule
from nti.contenttools.types.interfaces import ICNXHTMLBody
from nti.contenttools.types.interfaces import ICNXGlossary
from nti.contenttools.types.interfaces import ICNXProblemSolution


from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties

@interface.implementer(ICNXCollection)
class CNXCollection(DocumentStructureNode):
    createFieldProperties(ICNXCollection)

@interface.implementer(ICNXSubcollection)
class CNXSubcollection(DocumentStructureNode):
    createFieldProperties(ICNXSubcollection)

@interface.implementer(ICNXContent)
class CNXContent(DocumentStructureNode):
    createFieldProperties(ICNXContent)

@interface.implementer(ICNXModule)
class CNXModule(DocumentStructureNode):
    createFieldProperties(ICNXModule)

@interface.implementer(ICNXHTMLBody)
class CNXHTMLBody(DocumentStructureNode):
    createFieldProperties(ICNXHTMLBody)

@interface.implementer(ICNXGlossary)
class CNXGlossary(DocumentStructureNode):
    createFieldProperties(ICNXGlossary)

@interface.implementer(ICNXProblemSolution)
class CNXProblemSolution(DocumentStructureNode):
    createFieldProperties(ICNXProblemSolution)

