#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: exercise.py 49555 2014-09-18 15:31:30Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from IPython.core.debugger import Tracer

from ... import types

from lxml import etree

from lxml.html import HtmlComment

"""
used to process exercises found in each chapter of openstax epub
"""

def _process_exercise_div(element, epub):
    from .openstax import SubSection, Run
    class_ = u''
    if 'class' in element.attrib.keys():
        class_ = element.attrib['class']

    el = None
    if class_ in ['title']:
        el = SubSection.process(element, epub)
    elif class_ in ['section empty']:
        el = Run.process(element, epub)
    elif class_ in ['section']:
        el = ExerciseSection.process(element, epub)
    else:
        if isinstance(element,HtmlComment):
            pass
        else:
            logger.warn('Unhanled exercise div: %s', element.tag)
    return el


def _process_exercise_section(element, epub):
    from .openstax import Run
    class_ = u''
    if 'class' in element.attrib.keys():
        class_ = element.attrib['class']

    el = None
    if class_ in ['title']:
        el = Run.process(element, epub)
    elif class_ in ['body']:
    	el = _process_exercise(element, epub)
    else:
        if isinstance(element,HtmlComment):
            pass
        else:
            logger.warn('Unhanled exercise section: %s', class_)
    return el

def _process_exercise(element, epub):
    el = None
    for child in element:
        class_ = u''
        if 'class' in child.attrib.keys():
        	class_ = child.attrib['class']
        el = None
        if class_ in ['exercise']:
        	el = ExerciseElement.process(child, epub)
        else:
            if isinstance(child,HtmlComment):
                pass
            else:
                logger.warn('Unhanled exercise: %s',child.tag)
    return el

def _process_exercise_element(element, epub):
    from .openstax import Run
    class_ = u''
    if 'class' in element.attrib.keys():
        class_ = element.attrib['class']

    el = None
    if class_ in ['title']:
        el = Run.process(element, epub)
    elif class_ in ['body']:
    	el = Exercise.process(element, epub)
    else:
        if isinstance(element,HtmlComment):
            pass
        else:
            logger.warn('Unhanled exercise element: %s', element.tag)
    return el

class ExerciseElement(types.ExerciseElement):
	@classmethod
	def process(cls, element, epub):
		me = cls()
		for child in element:
			me.add_child(_process_exercise_element(child, epub))
		return me

class ExerciseSection(types.ExerciseSection):
	@classmethod
	def process(cls, element, epub):
		me = cls()
		for child in element:
			me.add_child(_process_exercise_section(child, epub))
		return me

class ChapterExercise(types.ChapterExercise):
    @classmethod
    def process(cls, element, epub):
        me = cls()
        for child in element:
            if child.tag == 'div':
                me.add_child(_process_exercise_div(child, epub))
        return me


class Exercise(types.Exercise):
    @classmethod
    def process(cls, element, epub):
    	from .openstax import Run
        me = cls()
        for child in element:
            if child.tag == 'div' and child.attrib['class'] == 'problem':
            	problem = Problem.process(child, epub)
            	me.set_problem(problem)
                logger.info('found div problem')
            elif child.tag == 'div' and child.attrib['class'] in ['solution labeled', 'solution']:
                solution = Solution.process(child, epub)
                me.set_solution(solution)
            else:
                if isinstance(child,HtmlComment):
                    pass
                else:
                    Tracer()()
                    logger.warn('Unhanled exercise process: %s', child.tag)
        return me

class Problem(types.Problem):
    @classmethod
    def process(cls, element, epub):
    	from .openstax import Paragraph
        me = cls()
        count_ordered_list = 0 
        for child in element:
        	if child.tag == 'div' and child.attrib['class'] == 'orderedlist':
        		me.add_child(MultipleChoices.process(child, epub))
        		count_ordered_list = count_ordered_list + 1
        	elif child.tag == 'p':
        		question  = Paragraph.process(child, epub)
        		me.set_question(question)
        	elif child.tag == 'div' and child.attrib['class'] in ['solution labeled', 'solution']:
        		solution = Solution.process(child, epub)
        		me.set_solution(solution)
        	else:
        		pass
        if count_ordered_list == 0:
        	me.set_problem_type('free_response')
        if count_ordered_list == 1:
        	me.set_problem_type('multiple_choice')
        elif count_ordered_list == 2:
        	me.set_problem_type('ordering')
        return me

class MultipleChoices(types.MultipleChoices):
    @classmethod
    def process(cls, element, epub):
        me = cls()
        for child in element:
        	if child.tag == 'ol' :
        		me.set_choices(_process_multiple_choice_items(child, epub))
        	else:
        		logger.warn('Unhandled multiple choice tag %s', child.tag)
        return me


def _process_multiple_choice_items (element, epub):
    from .openstax import Item
    result = []
    for child in element:
    	if child.tag == 'li' :
            item = Item.process(child, epub)
            result.append(item)
            logger.info('found multiple choice item')
    	else:
    		logger.warn("Unhandled multiple choice item %s", child.tag)
    return result


class Solution(types.Solution):
    @classmethod
    def process(cls, element, epub):
    	from .openstax import Run
        me = cls()
        for child in element:
        	if child.tag == 'div' and child.attrib['class'] == 'title':
        		pass
        	elif child.tag == 'div' and child.attrib['class'] == 'body':
        		solution = Run.process(child, epub)
        		me.set_solution(solution)
        return me


    	
