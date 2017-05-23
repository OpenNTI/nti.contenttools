#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IGlossary
from nti.contenttools.types.interfaces import IGlossaryDD
from nti.contenttools.types.interfaces import IGlossaryDT
from nti.contenttools.types.interfaces import IGlossaryItem
from nti.contenttools.types.interfaces import IGlossaryList
from nti.contenttools.types.interfaces import IGlossaryTerm
from nti.contenttools.types.interfaces import IGlossaryEntry
from nti.contenttools.types.interfaces import IGlossaryDefinition

from nti.contenttools.types.node import DocumentStructureNode

from nti.property.property import alias

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(IGlossary)
class Glossary(DocumentStructureNode):
    createFieldProperties(IGlossary)

    glossary = alias('glossary_dict')

    def set_title(self, title):
        self.title = title

    def set_filename(self, filename):
        self.filename = filename

    def set_glossary_dict(self, glossary_dict):
        self.glossary_dict = glossary_dict


@interface.implementer(IGlossaryList)
class GlossaryList(DocumentStructureNode):
    createFieldProperties(IGlossaryList)


@interface.implementer(IGlossaryItem)
class GlossaryItem(DocumentStructureNode):
    createFieldProperties(IGlossaryItem)


@interface.implementer(IGlossaryDT)
class GlossaryDT(DocumentStructureNode):
    createFieldProperties(IGlossaryDT)

    description = alias('desc')

    def set_description(self, desc):
        self.desc = desc


@interface.implementer(IGlossaryDD)
class GlossaryDD(DocumentStructureNode):
    createFieldProperties(IGlossaryDD)


@interface.implementer(IGlossaryTerm)
class GlossaryTerm(DocumentStructureNode):
    createFieldProperties(IGlossaryTerm)


@interface.implementer(IGlossaryDefinition)
class GlossaryDefinition(DocumentStructureNode):
    createFieldProperties(IGlossaryDefinition)


@interface.implementer(IGlossaryEntry)
class GlossaryEntry(DocumentStructureNode):
    createFieldProperties(IGlossaryEntry)
