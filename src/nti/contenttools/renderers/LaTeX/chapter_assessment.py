#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: math.py 108937 2017-03-15 16:50:32Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_children

from nti.contenttools.types.interfaces import IChapterExercise
from nti.contenttools.types.interfaces import IExerciseSection
from nti.contenttools.types.interfaces import IExerciseElement

from nti.contenttools.renderers.interfaces import IRenderer

"""
types.ChapterExercise.render = chapter_exercise_renderer
types.ExerciseSection.render = exercise_section_renderer
types.ExerciseElement.render = exercise_element_renderer
types.Exercise.render = exercise_renderer
types.Problem.render = problem_renderer
types.Solution.render = solution_renderer
types.MultipleChoices.render = multiple_choice_renderer
types.ExerciseCheck.render = exercise_check_renderer
types.ProblemExercise.render = problem_exercise_renderer
types.EndOfChapterSolution.render = chapter_solution_renderer
"""


def render_chapter_exercise(context, node):
    return render_children(context, node)


def render_exercise_section(context, node):
    return render_children(context, node)


def render_exercise_element(context, node):
    return render_children(context, node)


@interface.implementer(IRenderer)
class RendererMixin(object):

    func = None

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None):
        node = self.node if node is None else node
        return self.func(context, node)
    __call__ = render


@component.adapter(IChapterExercise)
class ChapterExerciseRenderer(RendererMixin):
    func = staticmethod(render_chapter_exercise)


@component.adapter(IExerciseSection)
class ExerciseSectionRenderer(RendererMixin):
    func = staticmethod(render_exercise_section)


@component.adapter(IExerciseElement)
class ExerciseElementRenderer(RendererMixin):
    func = staticmethod(render_exercise_element)
