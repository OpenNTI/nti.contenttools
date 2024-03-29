#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import INaqSymmath
from nti.contenttools.types.interfaces import INaqSymmathPart
from nti.contenttools.types.interfaces import INaqSymmathPartSolution
from nti.contenttools.types.interfaces import INaqSymmathPartSolutionValue
from nti.contenttools.types.interfaces import INaqSymmathPartSolutionExplanation

from nti.contenttools.types.symmath import NaqSymmath
from nti.contenttools.types.symmath import NaqSymmathPart
from nti.contenttools.types.symmath import NaqSymmathPartSolution
from nti.contenttools.types.symmath import NaqSymmathPartSolutionValue
from nti.contenttools.types.symmath import NaqSymmathPartSolutionExplanation

from nti.contenttools.tests import ContentToolsTestCase


class TestNaqSymmath(ContentToolsTestCase):

    def test_naqsymmath(self):
        node = NaqSymmath()
        assert_that(node, validly_provides(INaqSymmath))
        assert_that(node, verifiably_provides(INaqSymmath))


class TestNaqSymmathPart(ContentToolsTestCase):

    def test_naqsymmathpart(self):
        node = NaqSymmathPart()
        assert_that(node, validly_provides(INaqSymmathPart))
        assert_that(node, verifiably_provides(INaqSymmathPart))


class TestNaqSymmathPartSolution(ContentToolsTestCase):

    def test_naqsymmathpartsolution(self):
        node = NaqSymmathPartSolution()
        assert_that(node, validly_provides(INaqSymmathPartSolution))
        assert_that(node, verifiably_provides(INaqSymmathPartSolution))


class TestNaqSymmathPartSolutionValue(ContentToolsTestCase):

    def test_naqsymmathpartsolutionvalue(self):
        node = NaqSymmathPartSolutionValue()
        assert_that(node, validly_provides(INaqSymmathPartSolutionValue))
        assert_that(node, verifiably_provides(INaqSymmathPartSolutionValue))


class TestNaqSymmathPartSolutionExplanation(ContentToolsTestCase):
    def test_naqsymmathpartsolutionexplanation(self):
        node = NaqSymmathPartSolutionExplanation()
        assert_that(node, validly_provides(INaqSymmathPartSolutionExplanation))
        assert_that(node,
                    verifiably_provides(INaqSymmathPartSolutionExplanation))
