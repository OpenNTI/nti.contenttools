#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: omath.py 106584 2017-02-15 04:19:57Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IOMath, IOMathFunc, IOMathFName
from nti.contenttools.types.interfaces import IOMathRun
from nti.contenttools.types.interfaces import IOMathFrac
from nti.contenttools.types.interfaces import IOMathDenominator
from nti.contenttools.types.interfaces import IOMathNumerator
from nti.contenttools.types.interfaces import IOMathRadical
from nti.contenttools.types.interfaces import IOMathDegree
from nti.contenttools.types.interfaces import IOMathBase
from nti.contenttools.types.interfaces import IOMathSuperscript
from nti.contenttools.types.interfaces import IOMathSup
from nti.contenttools.types.interfaces import IOMathSubscript
from nti.contenttools.types.interfaces import IOMathSub
from nti.contenttools.types.interfaces import IOMathSubSup
from nti.contenttools.types.interfaces import IOMathNary
from nti.contenttools.types.interfaces import IOMathNaryPr
from nti.contenttools.types.interfaces import IOMathDelimiter
from nti.contenttools.types.interfaces import IOMathDPr
from nti.contenttools.types.interfaces import IOMathLim
from nti.contenttools.types.interfaces import IOMathLimLow
from nti.contenttools.types.interfaces import IOMathBar
from nti.contenttools.types.interfaces import IOMathAcc
from nti.contenttools.types.interfaces import IOMathPara
from nti.contenttools.types.interfaces import IOMathMPr
from nti.contenttools.types.interfaces import IOMathMcs
from nti.contenttools.types.interfaces import IOMathMc
from nti.contenttools.types.interfaces import IOMathMcPr
from nti.contenttools.types.interfaces import IOMathMatrix
from nti.contenttools.types.interfaces import IOMathMr
from nti.contenttools.types.interfaces import IOMathEqArr
from nti.contenttools.types.interfaces import IOMathSPre
from nti.contenttools.types.interfaces import IOMathBox
from nti.contenttools.types.interfaces import IOMathGroupChr
from nti.contenttools.types.interfaces import IOMathLimUpp
from nti.contenttools.types.interfaces import IOMathBorderBox

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties

@interface.implementer(IOMath)
class OMath(DocumentStructureNode):
    createFieldProperties(IOMath)

@interface.implementer(IOMathRun)
class OMathRun(DocumentStructureNode):
    createFieldProperties(IOMathRun)

@interface.implementer(IOMathFrac)
class OMathFrac(DocumentStructureNode):
    createFieldProperties(IOMathFrac)

    def set_frac_type(self, frac_type):
        self.frac_type = frac_type

@interface.implementer(IOMathNumerator)
class OMathNumerator(DocumentStructureNode):
    createFieldProperties(IOMathNumerator)

@interface.implementer(IOMathDenominator)
class OMathDenominator(DocumentStructureNode):
    createFieldProperties(IOMathDenominator)

@interface.implementer(IOMathRadical)
class OMathRadical(DocumentStructureNode):
    createFieldProperties(IOMathRadical)

@interface.implementer(IOMathDegree)
class OMathDegree(DocumentStructureNode):
    createFieldProperties(IOMathDegree)

@interface.implementer(IOMathBase)
class OMathBase(DocumentStructureNode):
    createFieldProperties(IOMathBase)

@interface.implementer(IOMathSuperscript)
class OMathSuperscript(DocumentStructureNode):
    createFieldProperties(IOMathSuperscript)

@interface.implementer(IOMathSup)
class OMathSup(DocumentStructureNode):
    createFieldProperties(IOMathSup)

@interface.implementer(IOMathSubscript)
class OMathSubscript(DocumentStructureNode):
    createFieldProperties(IOMathSubscript)

@interface.implementer(IOMathSub)
class OMathSub(DocumentStructureNode):
    createFieldProperties(IOMathSub)

@interface.implementer(IOMathSubSup)
class OMathSubSup(DocumentStructureNode):
    createFieldProperties(IOMathSubSup)

@interface.implementer(IOMathNary)
class OMathNary(DocumentStructureNode):
    createFieldProperties(IOMathNary)

@interface.implementer(IOMathNaryPr)
class OMathNaryPr(DocumentStructureNode):
    createFieldProperties(IOMathNaryPr)

    def set_chr_val(self, chrVal):
        self.chrVal = chrVal

    def set_lim_loc_val(self, limLocVal):
        self.limLocVal = limLocVal

@interface.implementer(IOMathDelimiter)
class OMathDelimiter(DocumentStructureNode):
    createFieldProperties(IOMathDelimiter)

@interface.implementer(IOMathDPr)
class OMathDPr(DocumentStructureNode):
    createFieldProperties(IOMathDPr)
    
    def set_beg_char(self, begChr):
        self.begChr = unicode(begChr)

    def set_end_char(self, endChr):
        self.endChr = unicode(endChr)

@interface.implementer(IOMathLim)
class OMathLim(DocumentStructureNode):
    createFieldProperties(IOMathLim)

@interface.implementer(IOMathLimLow)
class OMathLimLow(DocumentStructureNode):
    createFieldProperties(IOMathLimLow)

@interface.implementer(IOMathBar)
class OMathBar(DocumentStructureNode):
    createFieldProperties(IOMathBar)
    
    def set_bar_pos(self, pos):
        self.pos = unicode(pos)

@interface.implementer(IOMathAcc)
class OMathAcc(DocumentStructureNode):
    createFieldProperties(IOMathAcc)
    
    def set_acc_chr(self, accChr):
        self.accChr = accChr

@interface.implementer(IOMathPara)
class OMathPara(DocumentStructureNode):
    createFieldProperties(IOMathPara)

# handling matrix for docx

@interface.implementer(IOMathMatrix)
class OMathMatrix(DocumentStructureNode):
    createFieldProperties(IOMathMatrix)

    def set_number_of_col(self, number_of_col):
        self.number_of_col = unicode(number_of_col)

    def set_number_of_row(self, number_of_row):
        self.number_of_row = number_of_row

    def set_beg_char(self, begChr):
        self.begChr = unicode(begChr)

    def set_end_char(self, endChr):
        self.endChr = unicode(endChr)

# handling matrix property

@interface.implementer(IOMathMPr)
class OMathMPr (DocumentStructureNode):
    createFieldProperties(IOMathMPr)

@interface.implementer(IOMathMcs)
class OMathMcs (DocumentStructureNode):
    createFieldProperties(IOMathMcs)

@interface.implementer(IOMathMc)
class OMathMc (DocumentStructureNode):
    createFieldProperties(IOMathMc)

@interface.implementer(IOMathMcPr)
class OMathMcPr (DocumentStructureNode):
    createFieldProperties(IOMathMcPr)

# handling matrix row

@interface.implementer(IOMathMr)
class OMathMr (DocumentStructureNode):
    createFieldProperties(IOMathMr)

# omath: handling function apply function

@interface.implementer(IOMathFunc)
class OMathFunc(DocumentStructureNode):
    createFieldProperties(IOMathFunc)

@interface.implementer(IOMathFName)
class OMathFName(DocumentStructureNode):
    createFieldProperties(IOMathFName)

# omath : handling equation-array function

@interface.implementer(IOMathEqArr)
class OMathEqArr(DocumentStructureNode):
    createFieldProperties(IOMathEqArr)
    def set_row_space(self, rowSpace):
        self.rowSpace = rowSpace

@interface.implementer(IOMathSPre)
class OMathSPre(DocumentStructureNode):
    createFieldProperties(IOMathSPre)

@interface.implementer(IOMathBox)
class OMathBox(DocumentStructureNode):
    createFieldProperties(IOMathBox)

@interface.implementer(IOMathGroupChr)
class OMathGroupChr(DocumentStructureNode):
    createFieldProperties(IOMathGroupChr)

    def set_groupChr(self, groupChr):
        self.groupChr = groupChr

    def set_pos(self, pos):
        self.pos = unicode(pos)

    def set_vertJc(self, vertJc):
        self.vertJc = unicode(vertJc)

@interface.implementer(IOMathLimUpp)
class OMathLimUpp(DocumentStructureNode):
    createFieldProperties(IOMathLimUpp)

@interface.implementer(IOMathBorderBox)
class OMathBorderBox(DocumentStructureNode):
    createFieldProperties(IOMathBorderBox)
