#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
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

from nti.contenttools.types import TextNode

from nti.contenttools.tests import ContentToolsTestCase


class TestNaqSymmath(ContentToolsTestCase):

    def test_simple_naqsymmath(self):
        node = NaqSymmath()
        output = render_output(node)
        assert_that(output,
                    is_('\\begin{naquestion}[individual=true]\n\\end{naquestion}\n\n'))

    def test_naqsymmath(self):
        naqsymmath = NaqSymmath()
        node = NaqSymmathPart()
        solution = NaqSymmathPartSolution()
        solution_value = NaqSymmathPartSolutionValue()
        solution_value.value = TextNode(u'Solution A')
        solution.add(solution_value)
        node.solution = solution
        explanation = NaqSymmathPartSolutionExplanation()
        child = TextNode(u'This is symmath explanation')
        explanation.add(child)
        node.explanation = explanation
        naqsymmath.add(node)
        output = render_output(naqsymmath)
        assert_that(output,
                    is_('\\begin{naquestion}[individual=true]\n\\begin{naqsymmathpart}\n\\begin{naqsolutions}\n\\naqsolution[1] Solution A\n\n\\end{naqsolutions}\n\n\\begin{naqsolexplanation}\nThis is symmath explanation\n\\end{naqsolexplanation}\n\n\\end{naqsymmathpart}\n\\end{naquestion}\n\n'))

    def test_simple_naqsymmathpart(self):
        node = NaqSymmathPart()
        output = render_output(node)
        assert_that(output,
                    is_('\\begin{naqsymmathpart}\n\\end{naqsymmathpart}\n'))

    def test_naqsymmathpart(self):
        node = NaqSymmathPart()
        solution = NaqSymmathPartSolution()
        solution_value = NaqSymmathPartSolutionValue()
        solution_value.value = TextNode(u'Solution A')
        solution.add(solution_value)
        node.solution = solution
        explanation = NaqSymmathPartSolutionExplanation()
        child = TextNode(u'This is symmath explanation')
        explanation.add(child)
        node.explanation = explanation
        output = render_output(node)
        assert_that(output,
                    is_('\\begin{naqsymmathpart}\n\\begin{naqsolutions}\n\\naqsolution[1] Solution A\n\n\\end{naqsolutions}\n\n\\begin{naqsolexplanation}\nThis is symmath explanation\n\\end{naqsolexplanation}\n\n\\end{naqsymmathpart}\n'))

    def test_naqsymmathpart_with_solution_only(self):
        node = NaqSymmathPart()
        solution = NaqSymmathPartSolution()
        solution_value = NaqSymmathPartSolutionValue()
        solution_value.value = TextNode(u'Solution A')
        solution.add(solution_value)
        node.solution = solution

        output = render_output(node)
        assert_that(output,
                    is_('\\begin{naqsymmathpart}\n\\begin{naqsolutions}\n\\naqsolution[1] Solution A\n\n\\end{naqsolutions}\n\n\\end{naqsymmathpart}\n'))

    def test_simple_naqsymmathpartsolution(self):
        node = NaqSymmathPartSolution()
        output = render_output(node)
        assert_that(output,
                    is_('\\begin{naqsolutions}\n\n\\end{naqsolutions}\n'))

    def test_naqsymmathpartsolution(self):
        node = NaqSymmathPartSolution()
        child = NaqSymmathPartSolutionValue()
        child.value = TextNode(u'Solution A')
        node.add(child)
        output = render_output(node)
        assert_that(output,
                    is_('\\begin{naqsolutions}\n\\naqsolution[1] Solution A\n\n\\end{naqsolutions}\n'))

    def test_simple_naqsymmathpartsolutionvalue(self):
        node = NaqSymmathPartSolutionValue()
        output = render_output(node)
        assert_that(output, is_('\\naqsolution[1] '))

    def test_naqsymmathpartsolutionvalue(self):
        node = NaqSymmathPartSolutionValue()
        node.value = TextNode(u'Solution A')
        output = render_output(node)
        assert_that(output, is_('\\naqsolution[1] Solution A\n'))

    def test_simple_naqsymmathpartsolutionexplanation(self):
        node = NaqSymmathPartSolutionExplanation()
        output = render_output(node)
        assert_that(output,
                    is_('\\begin{naqsolexplanation}\n\n\\end{naqsolexplanation}\n'))

    def test_naqsymmathpartsolutionexplanation(self):
        node = NaqSymmathPartSolutionExplanation()
        child = TextNode(u'This is symmath explanation')
        node.add(child)
        output = render_output(node)
        assert_that(output,
                    is_('\\begin{naqsolexplanation}\nThis is symmath explanation\n\\end{naqsolexplanation}\n'))
