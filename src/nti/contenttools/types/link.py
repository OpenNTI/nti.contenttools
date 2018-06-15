#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IHyperlink

from nti.contenttools.types.interfaces import IRealPageNumber

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(IHyperlink)
class Hyperlink(DocumentStructureNode):
    createFieldProperties(IHyperlink)


    

@interface.implementer(IRealPageNumber)
class RealPageNumber(DocumentStructureNode):
    createFieldProperties(IRealPageNumber)
