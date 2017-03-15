#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_property
does_not = is_not

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import IMtr
from nti.contenttools.types.interfaces import IMtd
from nti.contenttools.types.interfaces import IMath
from nti.contenttools.types.interfaces import IMRow
from nti.contenttools.types.interfaces import IMSup
from nti.contenttools.types.interfaces import IMSub
from nti.contenttools.types.interfaces import IMFrac
from nti.contenttools.types.interfaces import IMRoot
from nti.contenttools.types.interfaces import IMOver
from nti.contenttools.types.interfaces import IMsqrt
from nti.contenttools.types.interfaces import IMText
from nti.contenttools.types.interfaces import IMUnder
from nti.contenttools.types.interfaces import IMSpace
from nti.contenttools.types.interfaces import IMTable
from nti.contenttools.types.interfaces import IMathRun
from nti.contenttools.types.interfaces import IMFenced
from nti.contenttools.types.interfaces import IMSubSup
from nti.contenttools.types.interfaces import IMMenclose
from nti.contenttools.types.interfaces import IMUnderover
from nti.contenttools.types.interfaces import IMLabeledTr
from nti.contenttools.types.interfaces import IMMprescripts
from nti.contenttools.types.interfaces import IMMultiscripts

from nti.contenttools.types.math import Mtr
from nti.contenttools.types.math import Mtd
from nti.contenttools.types.math import Math
from nti.contenttools.types.math import MRow
from nti.contenttools.types.math import MSup
from nti.contenttools.types.math import MSub
from nti.contenttools.types.math import MFrac
from nti.contenttools.types.math import MRoot
from nti.contenttools.types.math import MOver
from nti.contenttools.types.math import Msqrt
from nti.contenttools.types.math import MText
from nti.contenttools.types.math import MUnder
from nti.contenttools.types.math import MSpace
from nti.contenttools.types.math import Mtable
from nti.contenttools.types.math import MathRun
from nti.contenttools.types.math import MFenced
from nti.contenttools.types.math import MSubSup
from nti.contenttools.types.math import MMenclose
from nti.contenttools.types.math import MUnderover
from nti.contenttools.types.math import MLabeledTr
from nti.contenttools.types.math import MMprescripts
from nti.contenttools.types.math import MMultiscripts

from nti.contenttools.tests import ContentToolsTestCase


class TestMath(ContentToolsTestCase):

    def test_math(self):
        node = Math()
        assert_that(node, validly_provides(IMath))
        assert_that(node, verifiably_provides(IMath))
        assert_that(node, has_property('equation_type', is_(None)))

    def test_mrow(self):
        node = MRow()
        assert_that(node, validly_provides(IMRow))
        assert_that(node, verifiably_provides(IMRow))

    def test_sup(self):
        node = MSup()
        assert_that(node, validly_provides(IMSup))
        assert_that(node, verifiably_provides(IMSup))

    def test_sub(self):
        node = MSub()
        assert_that(node, validly_provides(IMSub))
        assert_that(node, verifiably_provides(IMSub))

    def test_sub_sup(self):
        node = MSubSup()
        assert_that(node, validly_provides(IMSubSup))
        assert_that(node, verifiably_provides(IMSubSup))

    def test_math_run(self):
        node = MathRun()
        assert_that(node, validly_provides(IMathRun))
        assert_that(node, verifiably_provides(IMathRun))

    def test_mfenced(self):
        node = MFenced()
        assert_that(node, validly_provides(IMFenced))
        assert_that(node, verifiably_provides(IMFenced))
        assert_that(node, has_property('opener', is_(u'')))
        assert_that(node, has_property('close', is_(u'')))
        assert_that(node, has_property('separators', is_(u'')))

    def test_mspace(self):
        node = MSpace()
        assert_that(node, validly_provides(IMSpace))
        assert_that(node, verifiably_provides(IMSpace))
        assert_that(node, has_property('width', is_(0)))
        assert_that(node, has_property('height', is_(0)))

    def test_mtable(self):
        node = Mtable()
        assert_that(node, validly_provides(IMTable))
        assert_that(node, verifiably_provides(IMTable))
        assert_that(node, has_property('number_of_col', is_(0)))
    
    def test_mlabeledtr(self):
        node = MLabeledTr()
        assert_that(node, validly_provides(IMLabeledTr))
        assert_that(node, verifiably_provides(IMLabeledTr))

    def test_mtd(self):
        node = Mtd()
        assert_that(node, validly_provides(IMtd))
        assert_that(node, verifiably_provides(IMtd))

    def test_mtr(self):
        node = Mtr()
        assert_that(node, validly_provides(IMtr))
        assert_that(node, verifiably_provides(IMtr))
        assert_that(node, has_property('number_of_col', is_(0)))

    def test_MFrac(self):
        node = MFrac()
        assert_that(node, validly_provides(IMFrac))
        assert_that(node, verifiably_provides(IMFrac))

    def test_msqrt(self):
        node = Msqrt()
        assert_that(node, validly_provides(IMsqrt))
        assert_that(node, verifiably_provides(IMsqrt))

    def test_root(self):
        node = MRoot()
        assert_that(node, validly_provides(IMRoot))
        assert_that(node, verifiably_provides(IMRoot))

    def test_munder(self):
        node = MUnder()
        assert_that(node, validly_provides(IMUnder))
        assert_that(node, verifiably_provides(IMUnder))

    def test_munderover(self):
        node = MUnderover()
        assert_that(node, validly_provides(IMUnderover))
        assert_that(node, verifiably_provides(IMUnderover))

    def test_mover(self):
        node = MOver()
        assert_that(node, validly_provides(IMOver))
        assert_that(node, verifiably_provides(IMOver))

    def test_menclose(self):
        node = MMenclose()
        assert_that(node, validly_provides(IMMenclose))
        assert_that(node, verifiably_provides(IMMenclose))
        assert_that(node, has_property('notation', is_(None)))

    def test_mprescripts(self):
        node = MMprescripts()
        assert_that(node, validly_provides(IMMprescripts))
        assert_that(node, verifiably_provides(IMMprescripts))
        assert_that(node, has_property('sub', is_(None)))
        assert_that(node, has_property('sup', is_(None)))

    def test_mmultiscripts(self):
        node = MMultiscripts()
        assert_that(node, validly_provides(IMMultiscripts))
        assert_that(node, verifiably_provides(IMMultiscripts))
        assert_that(node, has_property('base', is_(None)))
        assert_that(node, has_property('prescripts', is_(None)))

    def test_mtext(self):
        node = MText()
        assert_that(node, validly_provides(IMText))
        assert_that(node, verifiably_provides(IMText))
