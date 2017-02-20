#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import IOMath
from nti.contenttools.types.interfaces import IOMathMc
from nti.contenttools.types.interfaces import IOMathMr
from nti.contenttools.types.interfaces import IOMathAcc
from nti.contenttools.types.interfaces import IOMathBar
from nti.contenttools.types.interfaces import IOMathBox
from nti.contenttools.types.interfaces import IOMathDPr
from nti.contenttools.types.interfaces import IOMathLim
from nti.contenttools.types.interfaces import IOMathMcs
from nti.contenttools.types.interfaces import IOMathMPr
from nti.contenttools.types.interfaces import IOMathRun
from nti.contenttools.types.interfaces import IOMathSub
from nti.contenttools.types.interfaces import IOMathSup
from nti.contenttools.types.interfaces import IOMathBase
from nti.contenttools.types.interfaces import IOMathFrac
from nti.contenttools.types.interfaces import IOMathFunc
from nti.contenttools.types.interfaces import IOMathMcPr
from nti.contenttools.types.interfaces import IOMathNary
from nti.contenttools.types.interfaces import IOMathPara
from nti.contenttools.types.interfaces import IOMathSPre
from nti.contenttools.types.interfaces import IOMathEqArr
from nti.contenttools.types.interfaces import IOMathFName
from nti.contenttools.types.interfaces import IOMathLimLow
from nti.contenttools.types.interfaces import IOMathLimUpp
from nti.contenttools.types.interfaces import IOMathMatrix
from nti.contenttools.types.interfaces import IOMathNaryPr
from nti.contenttools.types.interfaces import IOMathDegree
from nti.contenttools.types.interfaces import IOMathSubSup
from nti.contenttools.types.interfaces import IOMathRadical
from nti.contenttools.types.interfaces import IOMathGroupChr
from nti.contenttools.types.interfaces import IOMathBorderBox
from nti.contenttools.types.interfaces import IOMathDelimiter
from nti.contenttools.types.interfaces import IOMathNumerator
from nti.contenttools.types.interfaces import IOMathSubscript
from nti.contenttools.types.interfaces import IOMathDenominator
from nti.contenttools.types.interfaces import IOMathSuperscript

from nti.contenttools.types.omath import OMath
from nti.contenttools.types.omath import OMathMc
from nti.contenttools.types.omath import OMathMr
from nti.contenttools.types.omath import OMathAcc
from nti.contenttools.types.omath import OMathBar
from nti.contenttools.types.omath import OMathBox
from nti.contenttools.types.omath import OMathDPr
from nti.contenttools.types.omath import OMathLim
from nti.contenttools.types.omath import OMathMcs
from nti.contenttools.types.omath import OMathMPr
from nti.contenttools.types.omath import OMathRun
from nti.contenttools.types.omath import OMathSub
from nti.contenttools.types.omath import OMathSup
from nti.contenttools.types.omath import OMathBase
from nti.contenttools.types.omath import OMathFrac
from nti.contenttools.types.omath import OMathFunc
from nti.contenttools.types.omath import OMathMcPr
from nti.contenttools.types.omath import OMathNary
from nti.contenttools.types.omath import OMathPara
from nti.contenttools.types.omath import OMathSPre
from nti.contenttools.types.omath import OMathEqArr
from nti.contenttools.types.omath import OMathFName
from nti.contenttools.types.omath import OMathLimLow
from nti.contenttools.types.omath import OMathLimUpp
from nti.contenttools.types.omath import OMathMatrix
from nti.contenttools.types.omath import OMathNaryPr
from nti.contenttools.types.omath import OMathDegree
from nti.contenttools.types.omath import OMathSubSup
from nti.contenttools.types.omath import OMathRadical
from nti.contenttools.types.omath import OMathGroupChr
from nti.contenttools.types.omath import OMathBorderBox
from nti.contenttools.types.omath import OMathDelimiter
from nti.contenttools.types.omath import OMathNumerator
from nti.contenttools.types.omath import OMathSubscript
from nti.contenttools.types.omath import OMathDenominator
from nti.contenttools.types.omath import OMathSuperscript

from nti.contenttools.tests import ContentToolsTestCase


class TestOMath(ContentToolsTestCase):

    def test_omath(self):
        node = OMath()
        assert_that(node, validly_provides(IOMath))
        assert_that(node, verifiably_provides(IOMath))

    def test_omath_run(self):
        node = OMathRun()
        assert_that(node, validly_provides(IOMathRun))
        assert_that(node, verifiably_provides(IOMathRun))

    def test_omath_frac(self):
        node = OMathFrac()
        assert_that(node, validly_provides(IOMathFrac))
        assert_that(node, verifiably_provides(IOMathFrac))

    def test_omath_numerator(self):
        node = OMathNumerator()
        assert_that(node, validly_provides(IOMathNumerator))
        assert_that(node, verifiably_provides(IOMathNumerator))

    def test_omath_denominator(self):
        node = OMathDenominator()
        assert_that(node, validly_provides(IOMathDenominator))
        assert_that(node, verifiably_provides(IOMathDenominator))

    def test_omath_radical(self):
        node = OMathRadical()
        assert_that(node, validly_provides(IOMathRadical))
        assert_that(node, verifiably_provides(IOMathRadical))

    def test_omath_degree(self):
        node = OMathDegree()
        assert_that(node, validly_provides(IOMathDegree))
        assert_that(node, verifiably_provides(IOMathDegree))

    def test_omath_base(self):
        node = OMathBase()
        assert_that(node, validly_provides(IOMathBase))
        assert_that(node, verifiably_provides(IOMathBase))

    def test_omath_superscript(self):
        node = OMathSuperscript()
        assert_that(node, validly_provides(IOMathSuperscript))
        assert_that(node, verifiably_provides(IOMathSuperscript))

    def test_omath_sup(self):
        node = OMathSup()
        assert_that(node, validly_provides(IOMathSup))
        assert_that(node, verifiably_provides(IOMathSup))

    def test_omath_subscript(self):
        node = OMathSubscript()
        assert_that(node, validly_provides(IOMathSubscript))
        assert_that(node, verifiably_provides(IOMathSubscript))

    def test_omath_sub(self):
        node = OMathSub()
        assert_that(node, validly_provides(IOMathSub))
        assert_that(node, verifiably_provides(IOMathSub))

    def test_omath_sub_sup(self):
        node = OMathSubSup()
        assert_that(node, validly_provides(IOMathSubSup))
        assert_that(node, verifiably_provides(IOMathSubSup))

    def test_omath_nary(self):
        node = OMathNary()
        assert_that(node, validly_provides(IOMathNary))
        assert_that(node, verifiably_provides(IOMathNary))

    def test_omath_nary_pr(self):
        node = OMathNaryPr()
        assert_that(node, validly_provides(IOMathNaryPr))
        assert_that(node, verifiably_provides(IOMathNaryPr))

    def test_omath_delimiter(self):
        node = OMathDelimiter()
        assert_that(node, validly_provides(IOMathDelimiter))
        assert_that(node, verifiably_provides(IOMathDelimiter))

    def test_omath_dpr(self):
        node = OMathDPr()
        assert_that(node, validly_provides(IOMathDPr))
        assert_that(node, verifiably_provides(IOMathDPr))

    def test_omath_lim(self):
        node = OMathLim()
        assert_that(node, validly_provides(IOMathLim))
        assert_that(node, verifiably_provides(IOMathLim))

    def test_omath_lim_low(self):
        node = OMathLimLow()
        assert_that(node, validly_provides(IOMathLimLow))
        assert_that(node, verifiably_provides(IOMathLimLow))

    def test_omath_bar(self):
        node = OMathBar()
        assert_that(node, validly_provides(IOMathBar))
        assert_that(node, verifiably_provides(IOMathBar))

    def test_omath_acc(self):
        node = OMathAcc()
        assert_that(node, validly_provides(IOMathAcc))
        assert_that(node, verifiably_provides(IOMathAcc))

    def test_omath_para(self):
        node = OMathPara()
        assert_that(node, validly_provides(IOMathPara))
        assert_that(node, verifiably_provides(IOMathPara))

    def test_omath_matrix(self):
        node = OMathMatrix()
        assert_that(node, validly_provides(IOMathMatrix))
        assert_that(node, verifiably_provides(IOMathMatrix))

    def test_omath_mpr(self):
        node = OMathMPr()
        assert_that(node, validly_provides(IOMathMPr))
        assert_that(node, verifiably_provides(IOMathMPr))

    def test_omath_mcs(self):
        node = OMathMcs()
        assert_that(node, validly_provides(IOMathMcs))
        assert_that(node, verifiably_provides(IOMathMcs))

    def test_omath_mc(self):
        node = OMathMc()
        assert_that(node, validly_provides(IOMathMc))
        assert_that(node, verifiably_provides(IOMathMc))

    def test_omath_mc_pr(self):
        node = OMathMcPr()
        assert_that(node, validly_provides(IOMathMcPr))
        assert_that(node, verifiably_provides(IOMathMcPr))

    def test_omath_mr(self):
        node = OMathMr()
        assert_that(node, validly_provides(IOMathMr))
        assert_that(node, verifiably_provides(IOMathMr))

    def test_omath_func(self):
        node = OMathFunc()
        assert_that(node, validly_provides(IOMathFunc))
        assert_that(node, verifiably_provides(IOMathFunc))

    def test_omath_fname(self):
        node = OMathFName()
        assert_that(node, validly_provides(IOMathFName))
        assert_that(node, verifiably_provides(IOMathFName))

    def test_omath_eqarr(self):
        node = OMathEqArr()
        assert_that(node, validly_provides(IOMathEqArr))
        assert_that(node, verifiably_provides(IOMathEqArr))

    def test_omath_spre(self):
        node = OMathSPre()
        assert_that(node, validly_provides(IOMathSPre))
        assert_that(node, verifiably_provides(IOMathSPre))

    def test_omath_box(self):
        node = OMathBox()
        assert_that(node, validly_provides(IOMathBox))
        assert_that(node, verifiably_provides(IOMathBox))

    def test_omath_group_chr(self):
        node = OMathGroupChr()
        assert_that(node, validly_provides(IOMathGroupChr))
        assert_that(node, verifiably_provides(IOMathGroupChr))

    def test_omath_lim_upp(self):
        node = OMathLimUpp()
        assert_that(node, validly_provides(IOMathLimUpp))
        assert_that(node, verifiably_provides(IOMathLimUpp))

    def test_omath_border_box(self):
        node = OMathBorderBox()
        assert_that(node, validly_provides(IOMathBorderBox))
        assert_that(node, verifiably_provides(IOMathBorderBox))
