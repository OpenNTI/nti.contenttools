#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
used to process glossary found in openstax epub

.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml.html import HtmlComment

from ... import types

class Glossary(types.Glossary):

	@classmethod
	def process(cls, element, epub):
		from .openstax import _process_div_elements
		me = cls()
		for child in element:
			if child.tag == 'dl':
				me.add_child(GlossaryList.process(child, epub))
			elif child.tag == 'div' and child.attrib['class'] == 'titlepage':
				me.set_title(_process_div_elements(child, epub))
			else:
				logger.warn('Unhandled Glossary element : %s', child.tag)
		return me

class GlossaryList( types.GlossaryList ):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		me.add_child(GlossaryItem.process(element, epub))
		return me

class GlossaryItem( types.GlossaryItem ):

	@classmethod
	def process(cls, element, epub):
		me = cls()
		count_child = -1
		for child in element:
			if child.tag == 'dt':
				me.add_child(GlossaryDT.process(child, epub))
				count_child = count_child + 1
			elif child.tag == 'dd':
				if me.children[count_child].desc == None:
					desc = []
					desc.append(GlossaryDD.process(child, epub))
					me.children[count_child].set_description(desc)
				else:
					desc = me.children[count_child].desc
					desc.append(GlossaryDD.process(child, epub))
					me.children[count_child].set_description(desc)
			elif child.tag == 'a':
				pass
			else:
				if isinstance(child,HtmlComment):
					pass
				else:
					logger.warn('Unhandled <dl> element child: %s.',child.tag)
		return me


class GlossaryDT(types.GlossaryDT):
	@classmethod
	def process(cls, element, epub):
		from .openstax import _process_p_elements
		from .openstax import _process_sub_elements 
		from .openstax import _process_sup_elements
		from .openstax import _process_span_elements
		me = cls()
		if element.text:
			if element.text.isspace():
				pass
			else:
				new_el_text = element.text.rstrip() + u' '
				me.add_child(types.TextNode(new_el_text))
		for sub_el in element:
			if sub_el.tag == 'p':
				me.add_child(_process_p_elements(sub_el, epub))
			elif sub_el.tag ==  'span':
				me.add_child(_process_span_elements(sub_el, epub))
			elif sub_el.tag ==  'sub':
				me.add_child(_process_sub_elements(sub_el, epub))
			elif sub_el.tag ==  'sup':
				me.add_child(_process_sup_elements(sub_el, epub))
			else:
				if isinstance(sub_el,HtmlComment):
					pass
				else:
					logger.warn('Unhandled Glossary <dt> child: %s.',sub_el.tag)
		return me



class GlossaryDD(types.GlossaryDD):
	@classmethod
	def process(cls, element, epub):
		from .openstax import _process_p_elements
		from .openstax import _process_div_elements
		me = cls()
		if element.text:
			if element.text.isspace():
				pass
			else:
				new_el_text = element.text.rstrip() + u' '
				me.add_child(types.TextNode(new_el_text))
		for sub_el in element:
			if sub_el.tag == 'p':
				me.add_child(_process_p_elements(sub_el, epub))
			elif sub_el.tag == 'div':
				me.add_child(_process_div_elements(sub_el, epub))
			else:
				if isinstance(sub_el,HtmlComment):
					pass
				else:
					logger.warn('Unhandled Glossary <dd> child: %s.',sub_el.tag)
		return me


class GlossaryTerm(types.GlossaryTerm):
	@classmethod
	def process(cls, element, epub):
		from .openstax import Run		
		me = cls()
		for child in element:
			me.add_child(Run.process(child, epub))
		return me
