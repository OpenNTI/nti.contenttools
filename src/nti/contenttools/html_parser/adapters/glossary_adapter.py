#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)
from ... import types
from .run_adapter import check_child
from .run_adapter import check_element_text
from .run_adapter import check_element_tail
from .run_adapter import Run

class GlossaryTerm(types.GlossaryTerm):
	@classmethod
	def process(cls, element):
		me = cls()
		me = check_element_text(me, element)
		me = check_child(me, element)
		el = Run()
		el.add_child(me)
		el = check_element_tail(el, element)
		return el

class GlossaryDefinition(types.GlossaryDefinition):
	@classmethod
	def process(cls, element):
		me = cls()
		if element.tag == 'dl':
			me = process_glossary_dl_element(me, element)
		else:
			for child in element:
				data_type = child.attrib[u'data-type'] if u'data-type' in child.attrib else u''
				el = Run()
				el = check_element_text(el, child)
				el = check_child(el, child)
				el = check_element_tail(el, child)
				if data_type == u'term' : me.term = el
				elif data_type == u'meaning' : me.meaning = el
				else : logger.warn(u'Unhandled data type %s', data_type)
		return me

def process_glossary_dl_element(glossary_def_node,element):
	for child in element :
		if child.tag == 'dt':
			glossary_def_node.term = Run.process(child)
		elif child.tag == 'dd':
			glossary_def_node.meaning = Run.process(child)
		else:
			logger.warn('Unhandled glossary dl element child %s', child.tag)
	return glossary_def_node


