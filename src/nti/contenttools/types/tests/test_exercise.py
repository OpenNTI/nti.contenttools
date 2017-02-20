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

from nti.contenttools.types.interfaces import IExample
from nti.contenttools.types.interfaces import IProblem
from nti.contenttools.types.interfaces import IExercise
from nti.contenttools.types.interfaces import ISolution
from nti.contenttools.types.interfaces import IExerciseDiv
from nti.contenttools.types.interfaces import IExerciseCheck
from nti.contenttools.types.interfaces import IChapterExercise
from nti.contenttools.types.interfaces import IExerciseSection
from nti.contenttools.types.interfaces import IExerciseElement
from nti.contenttools.types.interfaces import IMultipleChoices
from nti.contenttools.types.interfaces import IProblemExercise
from nti.contenttools.types.interfaces import IEndOfChapterSolution

from nti.contenttools.types.exercise import Example
from nti.contenttools.types.exercise import Problem
from nti.contenttools.types.exercise import Exercise
from nti.contenttools.types.exercise import Solution
from nti.contenttools.types.exercise import ExerciseDiv
from nti.contenttools.types.exercise import ExerciseCheck
from nti.contenttools.types.exercise import MultipleChoices
from nti.contenttools.types.exercise import ChapterExercise
from nti.contenttools.types.exercise import ExerciseSection
from nti.contenttools.types.exercise import ExerciseElement
from nti.contenttools.types.exercise import ProblemExercise
from nti.contenttools.types.exercise import EndOfChapterSolution

from nti.contenttools.tests import ContentToolsTestCase


class TestExercise(ContentToolsTestCase):

    def test_exercise(self):
        node = Exercise()
        assert_that(node, validly_provides(IExercise))
        assert_that(node, verifiably_provides(IExercise))
        assert_that(node, has_property('solution', is_(None)))
        assert_that(node, has_property('problem', is_(None)))

    def test_problem(self):
        node = Problem()
        assert_that(node, validly_provides(IProblem))
        assert_that(node, verifiably_provides(IProblem))
        assert_that(node, has_property('question', is_(None)))
        assert_that(node, has_property('solution', is_(None)))
        assert_that(node, has_property('label', is_(None)))
        assert_that(node, has_property('problem_type', is_(None)))

    def test_solution(self):
        node = Solution()
        assert_that(node, validly_provides(ISolution))
        assert_that(node, verifiably_provides(ISolution))
        assert_that(node, has_property('solution', is_(None)))
        assert_that(node, has_property('label', is_(None)))
        assert_that(node, has_property('problem_type', is_(None)))

    def test_multiple_choices(self):
        node = MultipleChoices()
        assert_that(node, validly_provides(IMultipleChoices))
        assert_that(node, verifiably_provides(IMultipleChoices))
        assert_that(node, has_property('solution', is_(None)))
        assert_that(node, has_property('choices', is_(None)))

    def test_chapter_exercise(self):
        node = ChapterExercise()
        assert_that(node, validly_provides(IChapterExercise))
        assert_that(node, verifiably_provides(IChapterExercise))

    def test_exercise_section(self):
        node = ExerciseSection()
        assert_that(node, validly_provides(IExerciseSection))
        assert_that(node, verifiably_provides(IExerciseSection))

    def test_exercise_element(self):
        node = ExerciseElement()
        assert_that(node, validly_provides(IExerciseElement))
        assert_that(node, verifiably_provides(IExerciseElement))

    def test_exercise_div(self):
        node = ExerciseDiv()
        assert_that(node, validly_provides(IExerciseDiv))
        assert_that(node, verifiably_provides(IExerciseDiv))

    def test_problem_exercise(self):
        node = ProblemExercise()
        assert_that(node, validly_provides(IProblemExercise))
        assert_that(node, verifiably_provides(IProblemExercise))
        assert_that(node, has_property('problem_type', is_(None)))
        assert_that(node, has_property('title', is_(None)))
        assert_that(node, has_property('label', is_(None)))

    def test_example(self):
        node = Example()
        assert_that(node, validly_provides(IExample))
        assert_that(node, verifiably_provides(IExample))

    def test_exercise_check(self):
        node = ExerciseCheck()
        assert_that(node, validly_provides(IExerciseCheck))
        assert_that(node, verifiably_provides(IExerciseCheck))
        assert_that(node, has_property('title', is_(None)))
        assert_that(node, has_property('solution', is_(None)))

    def test_end_of_chapter_solution(self):
        node = EndOfChapterSolution()
        assert_that(node, validly_provides(IEndOfChapterSolution))
        assert_that(node, verifiably_provides(IEndOfChapterSolution))
        assert_that(node, has_property('title', is_(None)))
        assert_that(node, has_property('label', is_(None)))
        assert_that(node, has_property('body', is_(None)))
