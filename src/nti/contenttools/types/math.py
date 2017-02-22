#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IMtd
from nti.contenttools.types.interfaces import IMtr
from nti.contenttools.types.interfaces import IMath
from nti.contenttools.types.interfaces import IMRow
from nti.contenttools.types.interfaces import IMSup
from nti.contenttools.types.interfaces import IMSub
from nti.contenttools.types.interfaces import IMFrac
from nti.contenttools.types.interfaces import IMOver
from nti.contenttools.types.interfaces import IMRoot
from nti.contenttools.types.interfaces import IMText
from nti.contenttools.types.interfaces import IMsqrt
from nti.contenttools.types.interfaces import IMSpace
from nti.contenttools.types.interfaces import IMTable
from nti.contenttools.types.interfaces import IMUnder
from nti.contenttools.types.interfaces import IMathRun
from nti.contenttools.types.interfaces import IMFenced
from nti.contenttools.types.interfaces import IMSubSup
from nti.contenttools.types.interfaces import IMMenclose
from nti.contenttools.types.interfaces import IMUnderover
from nti.contenttools.types.interfaces import IMMprescripts
from nti.contenttools.types.interfaces import IMMultiscripts


from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(IMath)
class Math(DocumentStructureNode):
    createFieldProperties(IMath)


@interface.implementer(IMRow)
class MRow(DocumentStructureNode):
    createFieldProperties(IMRow)


@interface.implementer(IMSup)
class MSup(DocumentStructureNode):
    createFieldProperties(IMSup)


@interface.implementer(IMSub)
class MSub(DocumentStructureNode):
    createFieldProperties(IMSub)


@interface.implementer(IMSubSup)
class MSubSup(DocumentStructureNode):
    createFieldProperties(IMSubSup)


@interface.implementer(IMathRun)
class MathRun(DocumentStructureNode):
    createFieldProperties(IMathRun)


@interface.implementer(IMFenced)
class MFenced(DocumentStructureNode):
    createFieldProperties(IMFenced)


@interface.implementer(IMSpace)
class MSpace(DocumentStructureNode):
    createFieldProperties(IMSpace)


@interface.implementer(IMTable)
class Mtable(DocumentStructureNode):
    createFieldProperties(IMTable)

    def set_number_of_col(self, number_of_col):
        self.number_of_col = number_of_col


@interface.implementer(IMtr)
class Mtr(DocumentStructureNode):
    createFieldProperties(IMtr)

    def set_number_of_col(self, number_of_col):
        self.number_of_col = number_of_col


@interface.implementer(IMtd)
class Mtd(DocumentStructureNode):
    createFieldProperties(IMtd)


@interface.implementer(IMFrac)
class MFrac(DocumentStructureNode):
    createFieldProperties(IMFrac)


@interface.implementer(IMsqrt)
class Msqrt(DocumentStructureNode):
    createFieldProperties(IMsqrt)


@interface.implementer(IMRoot)
class MRoot(DocumentStructureNode):
    createFieldProperties(IMRoot)


@interface.implementer(IMUnder)
class MUnder(DocumentStructureNode):
    createFieldProperties(IMRoot)


@interface.implementer(IMUnderover)
class MUnderover(DocumentStructureNode):
    createFieldProperties(IMUnderover)


@interface.implementer(IMOver)
class MOver(DocumentStructureNode):
    createFieldProperties(IMOver)


@interface.implementer(IMMenclose)
class MMenclose(DocumentStructureNode):
    createFieldProperties(IMMenclose)


@interface.implementer(IMMultiscripts)
class MMultiscripts(DocumentStructureNode):
    createFieldProperties(IMMultiscripts)


@interface.implementer(IMMprescripts)
class MMprescripts(DocumentStructureNode):
    createFieldProperties(IMMprescripts)


@interface.implementer(IMText)
class MText(DocumentStructureNode):
    createFieldProperties(IMText)
