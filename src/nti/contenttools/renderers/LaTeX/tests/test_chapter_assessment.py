#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

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
        assert_that(output, u'Chapter Exercise')

    def test_exercise_section(self):
        node = ExerciseSection()
        run = Run()
        run.add(TextNode(u'Exercise Section'))
        node.add(run)
        output = render_output(node)
        assert_that(output, u'Exercise Section')

    def test_exercise_element(self):
        node = ExerciseElement()
        run = Run()
        run.add(TextNode(u'Exercise Element'))
        node.add(run)
        output = render_output(node)
        assert_that(output, u'Exercise Element')
    
    def test_problem(self):
        node = Problem()
        run = Run()
        run.add(TextNode(u'Problem'))
        node.add(run)
        output = render_output(node)
        assert_that(output, u'Problem')
