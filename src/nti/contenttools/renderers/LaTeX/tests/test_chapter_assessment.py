#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.chapter_assessment import ChapterExercise
from nti.contenttools.types.chapter_assessment import ExerciseSection
from nti.contenttools.types.chapter_assessment import ExerciseElement
from nti.contenttools.types.chapter_assessment import Problem

from nti.contenttools.types.run import Run
from nti.contenttools.types.text import TextNode

from nti.contenttools.tests import ContentToolsTestCase


class TestChapterAssessment(ContentToolsTestCase):

    def test_chapter_assessment(self):
        node = ChapterExercise()
        run = Run()
        run.add(TextNode(u'Chapter Exercise'))
        node.add(run)
        output = render_output(node)
        assert_that(output, is_(u'Chapter Exercise'))

    def test_exercise_section(self):
        node = ExerciseSection()
        run = Run()
        run.add(TextNode(u'Exercise Section'))
        node.add(run)
        output = render_output(node)
        assert_that(output, is_(u'Exercise Section'))

    def test_exercise_element(self):
        node = ExerciseElement()
        run = Run()
        run.add(TextNode(u'Exercise Element'))
        node.add(run)
        output = render_output(node)
        assert_that(output, is_(u'Exercise Element'))
    
    def test_problem(self):
        node = Problem()
        run = Run()
        run.add(TextNode(u'Problem'))
        node.add(run)
        output = render_output(node)
        assert_that(output, is_(u'\\begin{naquestion}\n\\end{naquestion}\n'))
    
    def test_problem_free_response(self):
        node = Problem()
        node.problem_type = u'free_response'
        run_question = Run()
        run_question.add(TextNode(u'1 + 1 = ?'))
        node.question = run_question
        
        run_solution = Run()
        run_solution.add(TextNode(u'2'))
        node.solution = run_solution
        
        output = render_output(node)
        assert_that(output, is_(u'\\begin{naquestion}\n\\begin{naqfreeresponsepart}\n$1 + 1 =$ ?\n\\begin{naqsolutions}\n\\naqsolution [1] 2\n\\end{naqsolutions}\n\\end{naqfreeresponsepart}\n\\end{naquestion}\n'))
