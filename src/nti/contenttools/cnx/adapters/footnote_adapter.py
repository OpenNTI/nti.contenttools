#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: footnote_adapter.py 64523 2015-05-04 21:18:24Z egawati.panjei $
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

class CNXFootnoteSection(object):
	"""
	There is no need to create new section of Footnote list
	"""
	def __init__(self):
		self.type_ = 'footnote-section'
	def process(self, element):
		el = Run()
		el = retrieve_footnote_element(el, element)
		return el

def retrieve_footnote_element(el, element):
	for child in element:
		if child.tag == 'ol':
			el = retrieve_footnote_element(el, child)
		elif child.tag == 'li':
			el = retrieve_footnote_element(el, child)
		elif child.tag == 'a':
			el = process_footnote_anchor_element(el,child)
		else:
			continue
	return el

def process_footnote_anchor_element(el, element):
	data_type = element.attrib[u'data-type'] if 'data-type' in element.attrib else u''
	if data_type == u'footnote-ref':
		el.add_child(FootnoteText.process(element))
	else:
		additional_el = Run()
		ref = element.attrib[u'href'] if 'href' in element.attrib else u''
		ref = types.TextNode(ref)
		ref_node = Run()
		ref_node.add_child(ref)
		ref_node = check_element_tail(ref_node, element)
		if isinstance(el.children[-1], types.FootnoteText):
			el.children[-1].add_child(ref_node)
	return el


