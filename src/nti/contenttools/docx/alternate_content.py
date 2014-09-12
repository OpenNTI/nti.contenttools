#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

###from IPython.core.debugger import Tracer

logger = __import__('logging').getLogger(__name__)
from . import properties as docx
from .. import types

class AlternateContent(types.AlternateContent):
	@classmethod
	def process(cls, element, doc):
		me = cls()
		mc_prefix = docx.nsprefixes['mc']
		Choice_el = '{%s}Choice' %(mc_prefix)
		for child in element.iterchildren():		
			if child.tag == Choice_el:
				choice_el_child = process_choice_el(child,doc)
				if choice_el_child is not None:
					me.add_child(choice_el_child)
				else:
					logger.warn('Unhandled AlternateContent element : %s', child.tag)
		return me

def process_choice_el(element,doc):
	doc_main_prefix = docx.nsprefixes['w']
	drawing_el = '{%s}drawing' %(doc_main_prefix)
	el = None
	for child in element.iterchildren():
		if child.tag == drawing_el:
			el = process_drawing_el(child, doc)
		else:
			logger.warn('Unhandled element choice of AlternateContent : %s',child.tag)
	return el

def process_drawing_el(element, doc):
	drawing_prefix = docx.nsprefixes['wp']
	anchor_el = '{%s}anchor' %(drawing_prefix) 
	el = None
	for child in element.iterchildren():
		if child.tag == anchor_el:
			el = process_anchor_el(child, doc)
		else:
			logger.warn("Unhandled drawing element : %s", child.tag)
	return el

def process_anchor_el(element, doc):
	main_image_prefix = docx.nsprefixes['a']
	graphic_el = '{%s}graphic' %(main_image_prefix)
	graphic_data_el = '{%s}graphicData' %(main_image_prefix) 
	el = None
	for child in element.iterchildren():
		if child.tag == graphic_el:
			for sub_el in child.iterchildren():
				if sub_el.tag == graphic_data_el:
					el = process_graphic_data_el(sub_el, doc)
				else:
					logger.warn('Unhandled graphic element : %s', sub_el.tag)
		else:
			logger.warn('Unhandled anchor_el : %s', child.tag)
	return el

def process_graphic_data_el(element, doc):
	wps_prefix = docx.nsprefixes['wps']
	wsp_el = '{%s}wsp' %(wps_prefix)
	txbx_el = '{%s}txbx' %(wps_prefix)
	el = None
	for child in element:
		if child.tag == wsp_el:
			for sub_el in child.iterchildren():
				if sub_el.tag == txbx_el:
					el = process_txbx_el(sub_el, doc)
				else:
					logger.warn('Unhandled wsp element %s', sub_el.tag)
		else:
			logger.warn('Unhandled graphicData element %s', child.tag)
	return el 


def process_txbx_el(element, doc):
	doc_main_prefix = docx.nsprefixes['w']
	txbx_content_el = '{%s}txbxContent' %(doc_main_prefix)
	el = None
	for child in element:
		if child.tag == txbx_content_el:
			el = TextBoxContent.process(child, doc)
		else:
			logger.warn('Unhandled txbxContent element child %s', child.tag)
	return el

class TextBoxContent(types.TextBoxContent):
	@classmethod
	def process(cls, element, doc):
		me = cls ()
		doc_main_prefix = docx.nsprefixes['w']
		p_el = '{%s}p' %(doc_main_prefix)
		from .paragraph import Paragraph
		for child in element.iterchildren():
			if child.tag == p_el:
				me.add_child(Paragraph.process(child,doc))
		return me


