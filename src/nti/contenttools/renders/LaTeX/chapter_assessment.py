#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer

"""
module to render exercise found in each chapter of openstax epub
"""

def chapter_exercise_renderer(self):
	return base_renderer(self)

def exercise_section_renderer(self):
	return base_renderer(self)

def exercise_element_renderer(self):
	return base_renderer(self)

def exercise_renderer(self):
	pass

def problem_renderer(self):
	"""
	render types.Problem
	possible problem_type : 'free_response', 'multiple_choice', and 'ordering'
	"""
	problem_body = u''
	if self.solution == None:
		if self.__parent__.solution is not None:
			self.solution = self.__parent__.solution
	if self.problem_type == 'free_response':
		pass
	elif self.problem_type == 'multiple_choice':
		problem_body = process_multiple_choice(self)
	elif self.problem_type == 'ordering':
		pass

	return u'\\begin{naquestion}\n\\label{ }\n%s\n%s\\end{naquestion}\n' %(self.question, problem_body)

def process_free_response_question(self):
	pass

def process_multiple_choice(self):
	logger.info('process multiple_choice')
	logger.info('number of children %s', len(self.children))
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
	return u'\\begin{naqmultiplechoicepart}\n\\begin{naqchoices}\n%s\\end{naqchoices}\n\\end{naqmultiplechoicepart}\n' % (item_body)

def get_multiple_choice_sol(self):
	solution = self.solution
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
	else:
		logger.warn('Unhandled solution for multiple choices : %s', solution)

def set_multiple_choice_tag(item, solution_check):
	if solution_check:
		return u'\\naqchoice [1] %s \n' %(item)
	else:
		return u'\\naqchoice %s \n' %(item) 

def process_ordering(self):
	pass

def solution_renderer(self):
	return base_renderer(self)

def multiple_choice_renderer(self):
	items = self.choices
	result = []
	for item in items:
		rendered_item = item.render()
		result.append(rendered_item)
	return result