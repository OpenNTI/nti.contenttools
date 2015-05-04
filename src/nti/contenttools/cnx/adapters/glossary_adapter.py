#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: glossary_adapter.py 51866 2014-10-23 17:34:06Z egawati.panjei $
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
			
class CNXGlossary(types.CNXGlossary):
	@classmethod
	def process(cls, element):
		me = cls()
		for child in element:
			if child.tag == u'h2' : continue
			data_type = child.attrib[u'data-type'].strip() if u'data-type' in child.attrib else u''
			if data_type == u'definition': me.add_child(GlossaryDefinition.process(child))
			else : 
				logger.warn('Unhandled CNX glossary data type : %s',data_type)
		return me


