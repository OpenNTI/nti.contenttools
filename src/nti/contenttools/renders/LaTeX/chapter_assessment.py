#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from IPython.core.debugger import Tracer

from .base import base_renderer
from ... import types

"""
module to render exercise found in each chapter of openstax epub
"""

def chapter_exercise_renderer(self):
	"""
	to render types.ChapterExercise
	"""
	return base_renderer(self)

def exercise_section_renderer(self):
	"""
	to render types.ExerciseSection
	"""
	return base_renderer(self)

def exercise_element_renderer(self):
	"""
	to render types.ExerciseElement
	"""
	return base_renderer(self)

def exercise_check_renderer(self):
	"""
	to render types.ExerciseCheck
	"""
	return base_renderer(self)

def problem_exercise_renderer(self):
	"""
	to render types.ProblemExercise
	"""
	body = base_renderer(self)
	title = self.title.render()
	label = self.label
	if label is not None:
		return u'\\newline \\\paragraph{\\label{%s} %s } \\newline %s\n' %(label, title, body)
	else:
		return u'\\newline %s \\newline %s\n' %(title, body)


def exercise_renderer(self):
	"""
	to render types.Exercise
	"""
	if self.solution is not None:
		if self.problem.solution is None:
			self.problem.set_solution(self.solution)
			self.problem.solution.set_problem_type(self.problem.problem_type)
	problem = self.problem.render()
	return u'\n%s\n' %(problem)

def problem_renderer(self):
	"""
	render types.Problem
	possible problem_type : 'free_response', 'multiple_choice', 'ordering', 'essay'
	"""
	problem_body = u''
	if self.problem_type == 'free_response':
		problem_body = free_response_renderer(self)
	elif self.problem_type == 'multiple_choice':
		problem_body = process_multiple_choice(self)
	elif self.problem_type == 'ordering':
		pass
	elif self.problem_type == 'essay':
		problem_body = essay_renderer(self)
	elif self.problem_type == 'problem_exercise':
		problem_body = get_question(self.question)
	label = self.label

	if self.problem_type == 'problem_exercise':
		return u'%s\n' %(problem_body)
	else:
		return u'\\begin{naquestion}\n\\label{%s}\n%s\\end{naquestion}\n' %(label, problem_body)

def get_question(questions):
	list_of_question = []
	for question in questions:
		list_of_question.append(question.render().rstrip())
	result = u''.join(list_of_question)
	return result

def free_response_renderer(self):
	"""
	render free response question
	"""
	if len(self.children) > 0 :
		list_of_sol = process_free_response_solution(self)
		return process_multiple_question(self, list_of_sol)
	else:	
		free_response_question = get_question(self.question)
		solution = self.solution.render()
		return set_free_response_tag(free_response_question, solution)

def process_free_response_solution(self):
	"""
	render multiple free_response solution
	"""
	solution = self.solution.solution
	result = []
	if isinstance(solution.children[0], types.Run) and len (solution.children[0].children) > 0:
		solutions_list = solution.children[0].children
		for item in solution_list:
			result.append(item.render())
	return result

def process_multiple_question(self, list_of_sol):
	"""
	used when free response has more than one question (point)
	"""
	points = None
	result = []
	index = 0
	question = get_question(self.question)
	if len(self.children) == 1 :
		if isinstance(self.children[0], types.MultipleChoices) :
			points = multiple_choice_renderer(self.children[0])
			for item in points:
				result.append(set_free_response_tag(question, item))
	join_result = u''.join(result)
	return join_result
				

def set_free_response_tag(question, solution):
	question = question.rstrip()
	solution_temp = []
	solution_temp.append(solution)
	solution_tag = set_solution_tag(solution_temp)
	return u'\\begin{naqfreeresponsepart}\n%s\n%s\\end{naqfreeresponsepart}\n' %(question, solution_tag)

def set_solution_tag(solution_list):
	result = []
	for item in solution_list:
		string = u'\\naqsolution [1] %s\n' %(item)
		result.append(string)
	join_result = u''.join(result)
	return u'\\begin{naqsolutions}\n%s\\end{naqsolutions}\n' %(join_result)

def essay_renderer(self):
	essay_question = get_question(self.question)
	essay_question = essay_question.rstrip()
	return u'\\begin{naqessaypart}\n%s\n\\end{naqessaypart}' %(essay_question)


def process_multiple_choice(self):
	choices = None
	if len(self.children) == 1:
		choices = self.children[0].render()
	else:
		logger.warn('multiple choice should only have one child')

	item_rendered = []
	solution = get_multiple_choice_sol(self)
	if isinstance(choices, list):
		for choice in choices:
			solution_check = False
			if solution == choices.index(choice):
				solution_check = True
			item_rendered.append(set_multiple_choice_tag(choice, solution_check))
	else:
		logger.warn('we need to make sure that choices var is a list')

	item_body = u''.join(item_rendered)
	question = get_question(self.question)
	question = question.rstrip()

	return u'\\begin{naqmultiplechoicepart}\n%s\n\\begin{naqchoices}\n%s\\end{naqchoices}\n\\end{naqmultiplechoicepart}\n' % (question,item_body)

def get_multiple_choice_sol(self):
	solution = u''
	if self.solution is not None:
		solution = self.solution.render()
	solution = solution.rstrip()
	if solution == 1 or solution == 'A' or solution == 'a':
		return 0
	elif solution == 2 or solution == 'B' or solution == 'b':
		return 1
	elif solution == 3 or solution == 'C' or solution == 'c':
		return 2
	elif solution == 4 or solution == 'D' or solution == 'd':
		return 3
	elif solution == 5 or solution == 'E' or solution == 'e':
		return 4
	elif solution == 6 or solution == 'F' or solution == 'f':
		return 5
	elif solution == u'':
		logger.warn('No solution')
	else:
		logger.warn('Unhandled solution for multiple choices : %s', solution)

def set_multiple_choice_tag(item, solution_check):
	item = item.rstrip()
	if solution_check:
		return u'\\naqchoice [1] %s \n' %(item)
	else:
		return u'\\naqchoice %s \n' %(item) 

def solution_renderer(self):
	if self.problem_type == 'multiple_choice':
		return base_renderer(self.solution)

def solve_multiple_solution(solution):
	pass


def multiple_choice_renderer(self):
	items = self.choices
	result = []
	for item in items:
		rendered_item = item.render()
		result.append(rendered_item)
	return result

def chapter_solution_renderer(self):
	label = self.label
	title = self.title.render().rstrip()
	body = self.body.render().rstrip()
	return u'\\newline \\\paragraph{\\label{%s} %s } \\newline %s\n' %(label, title, body)




