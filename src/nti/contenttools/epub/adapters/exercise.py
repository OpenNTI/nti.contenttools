#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
used to process exercises found in each chapter of openstax epub

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml.html import HtmlComment

from ... import types

from .openstax import Run
from .openstax import SubSection

def _process_exercise_div(element, epub, problem_type=None):
	
	class_ = u''
	if 'class' in element.attrib.keys():
		class_ = element.attrib['class']

	el = None
	if class_ in ['title']:
		el = SubSection.process(element, epub)
	elif class_ in ['section empty']:
		el = Run.process(element, epub)
	elif class_ in ['section']:
		el = ExerciseSection.process(element, epub, problem_type)
	else:
		if isinstance(element,HtmlComment):
			pass
		else:
			logger.warn('Unhanled exercise div: %s', element.tag)
	return el

def _process_exercise_section(element, epub, problem_type = None):
	
	class_ = u''
	if 'class' in element.attrib.keys():
		class_ = element.attrib['class']

	el = None
	if class_ in ['title']:
		pass
	elif class_ in ['body']:
		el = ExerciseDiv.process(element, epub, problem_type)
	else:
		if isinstance(element,HtmlComment):
			pass
		else:
			logger.warn('Unhanled exercise section: %s', class_)
	return el

def _process_exercise(element, epub, problem_type=None):
	class_ = u''
	if 'class' in element.attrib.keys():
		class_ = element.attrib['class']
	el = None
	if class_ in ['exercise', 'exercise section-quiz', 'exercise short-answer', 'exercise shortanswer', 'exercise shortanswers']:
		el = ExerciseElement.process(element, epub, problem_type)
	else:
		if isinstance(element,HtmlComment):
			pass
		else:
			logger.warn('Unhanled exercise: %s',element.tag)
	return el

def _process_exercise_element(element, epub, problem_type=None):
	class_ = u''
	if 'class' in element.attrib.keys():
		class_ = element.attrib['class']

	el = None
	if class_ in ['title']:
		pass
	elif class_ in ['body']:
		el = Exercise.process(element, epub, problem_type)
	else:
		if isinstance(element,HtmlComment):
			pass
		else:
			logger.warn('Unhanled exercise element: %s', element.tag)
	return el

class ExerciseCheck(types.ExerciseCheck):
	
	@classmethod
	def process(cls, element, epub, problem_type = None, title = u''):
		me = cls()
		me.set_title(title)
		for child in element:
			if child.tag == 'div' and child.attrib['class'] == 'title':
				pass
			elif child.tag == 'div' and child.attrib['class'] == 'body':
				me.add_child(Exercise.process(child, epub, problem_type))
			else:
				if isinstance(child,HtmlComment):
					pass
				else:
					logger.warn('Unhanled exercise check: %s', child.tag)
		return me

class ExerciseElement(types.ExerciseElement):

	@classmethod
	def process(cls, element, epub, problem_type=None):
		me = cls()
		for child in element:
			me.add_child(_process_exercise_element(child, epub, problem_type))
		return me

class ExerciseDiv(types.ExerciseDiv):

	@classmethod
	def process(cls, element, epub, problem_type=None):
		me = cls()
		for child in element:
			me.add_child(_process_exercise(child, epub, problem_type))
		return me

class ExerciseSection(types.ExerciseSection):

	@classmethod
	def process(cls, element, epub, problem_type=None):
		me = cls()
		for child in element:
			me.add_child(_process_exercise_section(child, epub, problem_type))
		return me

class ChapterExercise(types.ChapterExercise):

	@classmethod
	def process(cls, element, epub, problem_type=None):
		me = cls()
		for child in element:
			if child.tag == 'div':
				me.add_child(_process_exercise_div(child, epub, problem_type))
		return me

class Exercise(types.Exercise):

	@classmethod
	def process(cls, element, epub, problem_type=None):
		me = cls()
		for child in element:
			if child.tag == 'div' and child.attrib['class'] == 'problem':
				problem = Problem.process(child, epub, problem_type)
				me.set_problem(problem)
			elif child.tag == 'div' and child.attrib['class'] in ['solution labeled', 'solution', 'solution labeled section-quiz']:
				solution = Solution.process(child, epub)
				me.set_solution(solution)
			else:
				if isinstance(child,HtmlComment):
					pass
				else:
					logger.warn('Unhanled exercise process: %s', child.tag)
		return me

from .openstax import Paragraph
		
class Problem(types.Problem):

	@classmethod
	def process(cls, element, epub, problem_type = None):
		me = cls()
		count_ordered_list = 0 
		for child in element:
			if child.tag == 'div' and child.attrib['class'] == 'orderedlist':
				me.add_child(MultipleChoices.process(child, epub))
				count_ordered_list = count_ordered_list + 1
			elif child.tag == 'p':
				question  = Paragraph.process(child, epub)
				me.set_question(question)
			elif child.tag == 'span':
				label = child.attrib['id']
				me.set_label(label)
			elif child.tag == 'div' and child.attrib['class'] in ['solution labeled', 'solution']:
				solution = Solution.process(child, epub)
				me.set_solution(solution)
				logger.info('found solution inside problem')
			else:
				pass
		if count_ordered_list == 0 and problem_type == 'free_response':
			me.set_problem_type('free_response')
		elif count_ordered_list == 1 and problem_type == 'free_response':
			me.set_problem_type('free_response')
		elif count_ordered_list == 1 and problem_type == 'multiple_choice':
			me.set_problem_type('multiple_choice')
		elif count_ordered_list == 2:
			me.set_problem_type('ordering')
		elif count_ordered_list == 0 and problem_type == 'essay':
			me.set_problem_type('essay')
		return me

class MultipleChoices(types.MultipleChoices):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		for child in element:
			if child.tag == 'ol' :
				me.set_choices(_process_multiple_choice_items(child, epub))
			elif child.tag == 'span':
				pass
			else:
				logger.warn('Unhandled multiple choice tag %s', child.tag)
		return me

def _process_multiple_choice_items (element, epub):
	result = []
	for child in element:
		if child.tag == 'li' :
			item = Run.process(child, epub)
			result.append(item)
		else:
			logger.warn("Unhandled multiple choice item %s", child.tag)
	return result

class Solution(types.Solution):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.set_label(element.attrib['id'])
		for child in element:
			if child.tag == 'div' and child.attrib['class'] == 'title':
				pass
			elif child.tag == 'div' and child.attrib['class'] == 'body':
				solution = Run.process(child, epub)
				me.set_solution(solution)
		return me
