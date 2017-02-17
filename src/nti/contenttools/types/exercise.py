#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: media.py 106584 2017-02-15 04:19:57Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IExercise
from nti.contenttools.types.interfaces import IProblem
from nti.contenttools.types.interfaces import ISolution
from nti.contenttools.types.interfaces import IMultipleChoices
from nti.contenttools.types.interfaces import IChapterExercise
from nti.contenttools.types.interfaces import IExerciseSection
from nti.contenttools.types.interfaces import IExerciseElement
from nti.contenttools.types.interfaces import IExerciseDiv
from nti.contenttools.types.interfaces import IExample
from nti.contenttools.types.interfaces import IProblemExercise
from nti.contenttools.types.interfaces import IExerciseCheck
from nti.contenttools.types.interfaces import IEndOfChapterSolution

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties

@interface.implementer(IExercise)
class Exercise(DocumentStructureNode):
    createFieldProperties(IExercise)

    def set_problem(self, problem):
        self.problem = problem

    def set_solution(self, solution):
        self.solution = solution

    def set_label(self, label):
        self.label = label

@interface.implementer(IProblem)
class Problem (DocumentStructureNode):
    createFieldProperties(IProblem)

    def set_question(self, question):
        self.question = question

    def set_problem_type(self, problem_type):
        self.problem_type = problem_type

    def set_solution(self, solution):
        self.solution = solution

    def set_label(self, label):
        self.label = label

@interface.implementer(ISolution)
class Solution (DocumentStructureNode):
    createFieldProperties(ISolution)

    def set_solution(self, solution):
        self.solution = solution

    def set_label(self, label):
        self.label = label

    def set_problem_type(self, problem_type):
        self.problem_type = problem_type

@interface.implementer(IMultipleChoices)
class MultipleChoices(DocumentStructureNode):
    createFieldProperties(IMultipleChoices)

    def set_solution(self, solution):
        self.solution = solution

    def set_choices(self, choices):
        self.choices = choices

@interface.implementer(IChapterExercise)
class ChapterExercise(DocumentStructureNode):
    createFieldProperties(IChapterExercise)

@interface.implementer(IExerciseSection)
class ExerciseSection(DocumentStructureNode):
    createFieldProperties(IExerciseSection)

@interface.implementer(IExerciseElement)
class ExerciseElement(DocumentStructureNode):
    createFieldProperties(IExerciseElement)

@interface.implementer(IExerciseDiv)
class ExerciseDiv(DocumentStructureNode):
    createFieldProperties(IExerciseDiv)

@interface.implementer(IExample)
class Example(DocumentStructureNode):
    createFieldProperties(IExample)

@interface.implementer(IProblemExercise)
class ProblemExercise(DocumentStructureNode):
    createFieldProperties(IProblemExercise)

@interface.implementer(IExerciseCheck)
class ExerciseCheck(DocumentStructureNode):
    createFieldProperties(IExerciseCheck)

    def set_title(self, title):
        self.title = title

    def set_solution(self, solution):
        self.solution = solution

@interface.implementer(IEndOfChapterSolution)
class EndOfChapterSolution(DocumentStructureNode):
    createFieldProperties(IEndOfChapterSolution)

