#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
used to process note found in openstax epub
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)
from IPython.core.debugger import Tracer

from ... import types
from lxml.html import HtmlComment
from .exercise import Problem

"""
used to process note found in each chapter of openstax epub
"""
class OpenstaxNote (types.OpenstaxNote):
	@classmethod
	def process(cls, element, epub):
		from . openstax import Run
		me = cls()
		id_ = u''
		if 'id' in element.attrib.keys() :
			id_ = element.attrib['id']
			me.set_label(id_)
		for child in element:
			if child.tag  == 'div' and child.attrib['class'] == 'title':
				title = Run.process(child, epub)
				me.set_title(title)
			elif child.tag == 'div' and child.attrib['class'] == 'body':
				body = OpenstaxNoteBody.process(child, epub)
				me.set_body(body)
			elif isinstance(child, HtmlComment):
				pass
			else:
				logger.warn('Unhandled OpenstaxNote element %s', child.attrib)
				Tracer()()
		return me

class OpenstaxExampleNote (types.OpenstaxExampleNote):
	@classmethod
	def process(cls, element, epub):
		from . openstax import Run
		me = cls()
		id_ = u''
		if 'id' in element.attrib.keys():
			id_ = element.attrib['id']
			me.set_label(id_)
		title = None
		if 'title' in element.attrib.keys():
			title = element.attrib['title']

		for child in element:
			if child.tag == 'div' and child.attrib['class'] == 'title':
				if title is None:
					title = Run.process(child, epub)
			elif child.tag == 'div' and child.attrib['class'] == 'body':
				me.set_body(OpenstaxNoteBody.process(child, epub))
			else:
				logger.warn('Unhandled OpenstaxExampleNote element %s', child.attrib)
		me.set_title(title)
		return me

class OpenstaxNoteBody(types.OpenstaxNoteBody):
	@classmethod
	def process(cls, element, epub):
		from .openstax import Run, Table, Figure, Paragraph, _process_openstax_table, _process_span_elements
		from .equation_image import EquationImage
		from .exercise import process_problem_exercise
		me = cls()
		for child in element:
			class_ = u''
			if 'class' in child.attrib.keys():
				class_ = child.attrib['class']
			if child.tag == 'div' and class_ in ['exercise', 'exercise labeled', 'exercise finger']:
				problem_type = 'problem_exercise_example'
				el = process_problem_exercise(child, epub, problem_type)
				me.add_child(el)
			elif child.tag == 'div' and class_ in ['problem']:
				problem_type = 'problem_exercise_example'
				el = Problem.process(child, epub, problem_type)
				me.add_child(el)
			elif child.tag == 'div' and class_ in ['solution', 'solution labeled', 'solution check-understanding']:
				el = Paragraph.process(child, epub)
				me.add_child(el)
			elif child.tag == 'table':
				el = Table.process(child, epub)
				me.add_child(el)
			elif child.tag == 'div' and class_ in ['figure', 'figure splash', "figure   ", "figure  ","figure span-all", "figure "]:
				el = Figure.process(child, epub)
				me.add_child(el)
			elif child.tag == 'p':
				me.add_child(Paragraph.process(child, epub))
			elif child.tag == 'div' and class_ == 'table':
				me.add_child(_process_openstax_table(child, epub))
			elif child.tag == 'div' and class_ in ['note', 'itemizedlist', 'orderedlist', 'title', 'mediaobject',\
													 'note statistics calculator', 'note finger', 'note Reminder']:
				me.add_child(Paragraph.process(child, epub))
			elif child.tag == 'div' and class_ in ['equation']:
				el = EquationImage.process(child, epub)
				me.add_child(el)
			elif child.tag == 'span':
				el = _process_span_elements(child, epub)
				me.add_child(el)
			elif child.tag == 'div' and class_ in ['orderedlist stepwise']:
				el = Run.process(child, epub)
				me.add_child(el)
			elif isinstance(child, HtmlComment):
				pass
			else:
				logger.warn('Unhandled OpenstaxNoteBody %s', child.attrib)
				logger.warn(child.tag)
		return me


