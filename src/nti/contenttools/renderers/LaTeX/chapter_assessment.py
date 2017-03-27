#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
from nti.contenttools.renders.LaTeX.chapter_assessment import set_solution_tag
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_children

from nti.contenttools.types.interfaces import IChapterExercise
from nti.contenttools.types.interfaces import IExerciseSection
from nti.contenttools.types.interfaces import IExerciseElement
from nti.contenttools.types.interfaces import IProblem

from nti.contenttools.renderers.LaTeX.utils import create_label
from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value

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

def render_problem(context, node):
    context.write(u'\\begin{naquestion}\n')
    if node.label:  
        context.write(create_label(u'qid', node.label))
        context.write(u'\n')
    
    if node.problem_type == u'free_response':
        render_free_response(context, node)
    elif node.problem_type == u'multiple_choice':
        render_multiple_choice(context, node)
    elif node.problem_type == u'ordering':
        render_ordering(context, node)
    elif node.problem_type == u'essay':
        render_essay(context, node)
    elif node.problem_type in (u'problem_exercise', u'problem_exercise_example'):
        pass
    
    context.write(u'\\end{naquestion}\n')
    return node

def set_solution_tag(context, solution_list):
    context.write(u'\\begin{naqsolutions}\n')
    for item in solution_list:
        context.write(u'\\naqsolution [1] ')
        context.write(item)
        context.write(u'\n')
    context.write(u'\\end{naqsolutions}\n')

def render_free_response(context, node):
    context.write(u'\\begin{naqfreeresponsepart}\n')
    question = get_variant_field_string_value(node.question)
    context.write(question.rstrip())
    context.write(u'\n')
    solution = [get_variant_field_string_value(node.solution)]
    set_solution_tag(context, node, solution)
    context.write(u'\\end{naqfreeresponsepart}\n')
    return node

def render_multiple_choice(context, node):
    pass

def render_ordering(context, node):
    pass

def render_essay(context, node):
    context.write(u'\\begin{naqessaypart}\n')
    question = get_variant_field_string_value(node.question)
    context.write(question.rstrip())
    context.write(u'\n\\end{naqessaypart}')
    return node


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
    
@component.adapter(IProblem)
class ProblemRenderer(RendererMixin):
    func = staticmethod(render_problem)
