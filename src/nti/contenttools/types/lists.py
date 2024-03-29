#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division

__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IDD
from nti.contenttools.types.interfaces import IDT
from nti.contenttools.types.interfaces import IItem
from nti.contenttools.types.interfaces import IList
from nti.contenttools.types.interfaces import IOrderedList
from nti.contenttools.types.interfaces import IItemWithDesc
from nti.contenttools.types.interfaces import IUnorderedList
from nti.contenttools.types.interfaces import IDescriptionList

from nti.contenttools.types.node import DocumentStructureNode

from nti.property.property import alias

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(IList)
class List(DocumentStructureNode):
    createFieldProperties(IList)


@interface.implementer(IUnorderedList)
class UnorderedList(List):
    createFieldProperties(IUnorderedList)


@interface.implementer(IOrderedList)
class OrderedList(List):
    createFieldProperties(IOrderedList)


@interface.implementer(IItem)
class Item(DocumentStructureNode):
    createFieldProperties(IItem)


@interface.implementer(IDescriptionList)
class DescriptionList(List):
    createFieldProperties(IDescriptionList)


@interface.implementer(IItemWithDesc)
class ItemWithDesc(Item):
    createFieldProperties(IItemWithDesc)


@interface.implementer(IDT)
class DT(DocumentStructureNode):
    createFieldProperties(IDT)

    type_ = alias('type')
    description = alias('desc')

    def set_description(self, desc):
        self.desc = desc

    def set_type(self, type_):
        self.type_ = type_


@interface.implementer(IDD)
class DD(DocumentStructureNode):
    createFieldProperties(IDD)
