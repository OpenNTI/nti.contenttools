#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

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
				else: logger.warn('%s has no child', Choice_el)
			else : logger.warn('Unhandled AlternateContent element : %s', child.tag)
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
	inline_el = '{%s}inline' %(drawing_prefix) 
	el = None
	for child in element.iterchildren():
		if child.tag == anchor_el:
			el = process_anchor_el(child, doc)
		elif child.tag == inline_el:
			el =  process_anchor_el(child, doc)
		else:
			logger.warn("Unhandled drawing element : %s", child.tag)
	return el


def process_inline_el(element, doc):
	main_image_prefix = docx.nsprefixes['a']
	graphic_el = '{%s}graphic' %(main_image_prefix)
	graphic_data_el = '{%s}graphicData' %(main_image_prefix)


def process_anchor_el(element, doc):
	main_image_prefix = docx.nsprefixes['a']
	graphic_el = '{%s}graphic' %(main_image_prefix)
	graphic_data_el = '{%s}graphicData' %(main_image_prefix) 

	drawing_prefix = docx.nsprefixes['wpd']
	sizeRelH = '{%s}sizeRelH' %(drawing_prefix)
	sizeRelV = '{%s}sizeRelV' %(drawing_prefix)
	simplePos = '{%s}simplePos' %(drawing_prefix)
	positionH = '{%s}positionH' %(drawing_prefix)
	positionV = '{%s}positionV' %(drawing_prefix)
	extent = '{%s}extent' %(drawing_prefix)
	effectExtent = '{%s}effectExtent' %(drawing_prefix)
	wrapTopAndBottom = '{%s}wrapTopAndBottom' %(drawing_prefix)
	IGNORED_CHILD_2010 = [sizeRelH, sizeRelV, simplePos, positionH, positionV, extent, effectExtent, wrapTopAndBottom]

	drawing_prefix = docx.nsprefixes['wp']
	sizeRelH_ = '{%s}sizeRelH' %(drawing_prefix)
	sizeRelV_ = '{%s}sizeRelV' %(drawing_prefix)
	simplePos_ = '{%s}simplePos' %(drawing_prefix)
	positionH_ = '{%s}positionH' %(drawing_prefix)
	positionV_ = '{%s}positionV' %(drawing_prefix)
	extent_ = '{%s}extent' %(drawing_prefix)
	effectExtent_ = '{%s}effectExtent' %(drawing_prefix)
	wrapTopAndBottom_ = '{%s}wrapTopAndBottom' %(drawing_prefix)
	wrapSquare_ = '{%s}wrapSquare' %(drawing_prefix)
	docPr_ = '{%s}docPr' %(drawing_prefix)
	cNvGraphicFramePr_ = '{%s}cNvGraphicFramePr' %(drawing_prefix)

	IGNORED_CHILD_2006 = [sizeRelH_, sizeRelV_, simplePos_, positionH_, positionV_, extent_, effectExtent_, wrapTopAndBottom_, wrapSquare_, docPr_, cNvGraphicFramePr_]

	el = None
	for child in element.iterchildren():
		if child.tag == graphic_el:
			for sub_el in child.iterchildren():
				if sub_el.tag == graphic_data_el:
					el = process_graphic_data_el(sub_el, doc)
				else:
					logger.warn('Unhandled graphic element : %s', sub_el.tag)
		elif child.tag in IGNORED_CHILD_2010: pass
		elif child.tag in IGNORED_CHILD_2006: pass
		else:
			logger.warn('Unhandled anchor_el : %s', child.tag)
	return el

def process_graphic_data_el(element, doc):
	wps_prefix = docx.nsprefixes['wps']
	wsp_el = '{%s}wsp' %(wps_prefix)
	wpg_prefix = docx.nsprefixes['wpg']
	wgp_el = '{%s}wgp' %(wpg_prefix)
	el = None
	for child in element:
		if child.tag == wsp_el:
			el = process_wsp_el(child, doc)
		elif child.tag == wgp_el :
			el = process_wgp_el(child, doc)
		else:
			logger.warn('Unhandled graphicData element %s', child.tag)
	return el 

def process_wsp_el(element, doc):
	wps_prefix = docx.nsprefixes['wps']
	cNvPr = '{%s}cNvPr' %(wps_prefix)
	cNvSpPr = '{%s}cNvSpPr' %(wps_prefix)
	spPr = '{%s}spPr' %(wps_prefix)
	bodyPr = '{%s}bodyPr' %(wps_prefix)
	IGNORED_EL = [cNvSpPr, spPr, bodyPr, cNvPr]

	txbx_el = '{%s}txbx' %(wps_prefix)
	el = None
	for sub_el in element.iterchildren():
		if sub_el.tag == txbx_el:
			el = process_txbx_el(sub_el, doc)
		elif sub_el.tag in IGNORED_EL:
			pass
		else:
			logger.warn('Unhandled wsp element %s', sub_el.tag)
	return el

def process_wgp_el(element, doc):
	wpg_prefix = docx.nsprefixes['wpg']
	grpSp_el = '{%s}grpSp' %(wpg_prefix)
	el = None
	for child in element : 
		if child.tag == grpSp_el:
			el = process_grpSp_el(child, doc)
	return el

def process_grpSp_el(element, doc):
	wps_prefix = docx.nsprefixes['wps']
	wsp_el = '{%s}wsp' %(wps_prefix)
	el = None
	for child in element:
		if child.tag == wsp_el:
			el = process_wsp_el(child, doc)
	return el

def process_txbx_el(element, doc):
	doc_main_prefix = docx.nsprefixes['w']
	txbx_content_el = '{%s}txbxContent' %(doc_main_prefix)
	el = None
	for child in element:
		if child.tag == txbx_content_el:
			el = Sidebar.process(child, doc)
		else:
			logger.warn('Unhandled txbxContent element child %s', child.tag)
	return el

from .paragraph import Paragraph
from .table import Table
class TextBoxContent(types.TextBoxContent):
	@classmethod
	def process(cls, element, doc):
		me = cls ()
		doc_main_prefix = docx.nsprefixes['w']
		p_el = '{%s}p' %(doc_main_prefix)
		for child in element.iterchildren():
			if child.tag == p_el:
				me.add_child(Paragraph.process(child,doc))
			else:
				logger.warn ('Unhandled TextBoxContent child element : %s', child.tag)
		return me

class Sidebar(types.Sidebar):
	@classmethod
	def process(cls, element, doc):
		me = cls ()
		doc_main_prefix = docx.nsprefixes['w']
		p_el = '{%s}p' %(doc_main_prefix)
		tbl_el = '{%s}tbl' %(doc_main_prefix)
		for child in element.iterchildren():
			if child.tag == p_el:
				me.add_child(Paragraph.process(child,doc))
			elif child.tag == tbl_el:
				me.add_child(Table.process(child, doc))
		me.title = me.children[0]
		me.remove_child(me.children[0])
		return me
