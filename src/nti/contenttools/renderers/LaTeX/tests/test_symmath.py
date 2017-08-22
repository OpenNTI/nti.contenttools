#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.symmath import NaqSymmath
from nti.contenttools.types.symmath import NaqSymmathPart
from nti.contenttools.types.symmath import NaqSymmathPartSolution
from nti.contenttools.types.symmath import NaqSymmathPartSolutionValue
from nti.contenttools.types.symmath import NaqSymmathPartSolutionExplanation

from nti.contenttools.types.run import Run

from nti.contenttools.tests import ContentToolsTestCase

class TestNaqSymmath(ContentToolsTestCase):
    def test_simple_naqsymmath(self):
        node = NaqSymmath()
        output = render_output(node)
        assert_that(output, is_('\\begin{naquestion}[individual=true]\n\\end{naquestion}\n'))

    def test_simple_naqsymmathpart(self):
        node = NaqSymmathPart()
        output = render_output(node)
        assert_that(output, is_('\\begin{naqsymmathpart}\n\\end{naqsymmathpart}\n'))

    def test_simple_naqsymmathpartsolution(self):
        node = NaqSymmathPartSolution()
        output = render_output(node)
        assert_that(output, is_('\\begin{naqsolutions}\n\\end{naqsolutions}\n'))

    def test_simple_naqsymmathpartsolutionvalue(self):
        node = NaqSymmathPartSolutionValue()
        output = render_output(node)
        assert_that(output, is_('\\naqsolution[1] '))

    def test_simple_naqsymmathpartsolutionexplanation(self):
        node = NaqSymmathPartSolutionExplanation()
        output = render_output(node)
        assert_that(output, is_('\\begin{naqsolexplanation}\n\\end{naqsolexplanation}\n'))