#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: footnote_adapter.py 81888 2016-01-28 16:35:07Z carlos.sanchez $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ... import types
from .run_adapter import check_child
from .run_adapter import check_element_text
from .run_adapter import check_element_tail
from .run_adapter import Run

class Footnote(types.Footnote):
	@classmethod
	def process(cls, element):
		me = cls()
		el = Run()
		el = check_element_tail(el, element)
		me.text = el 
		if element.text : me.label = element.text
		return me

class FootnoteText(types.FootnoteText):
	@classmethod
	def process(cls, element):
		me = cls()
		el = Run()
		el = check_child(el, element)
		el = check_element_tail(el, element)
		me.text = el 
		me.label = element.attrib[u'name'] if u'name' in element.attrib else None
		if element.text : me.num = element.text
		return me

class FootnoteMark(types.FootnoteMark):
	@classmethod
	def process(cls, element):
		el = Run()
		me = cls()
		me.label = element.attrib[u'href'].replace(u'#', u'') if u'href' in element.attrib else None
		for child in element:
			if child.tag == u'sup':
				me.num = child.text 
			else :
				logger.warn('Unhandled FootnoteMark child element :%s', child)
		el.add_child(me)
		el = check_element_tail(el, element)
		return el

