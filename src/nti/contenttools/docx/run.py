#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import urllib
import urlparse

from . import properties as docx
from .. import types
from .ignored_tags import IGNORED_TAGS
from .note import Note

class Run( types.Run ):

	@classmethod
	def process( cls, textrun, doc, fields = [], rels=None):
		'''Process a paragraph textrun, parse for character styles'''
	
		if rels is None:
				rels = doc.relationships
	
		me = cls()
		found_text = False
		doc_main_prefix = docx.nsprefixes['w']
		rPr_el = '{%s}rPr' %(doc_main_prefix)
		t_el = '{%s}t' %(doc_main_prefix)
		tab_el = '{%s}tab' %(doc_main_prefix)
		drawing_el = '{%s}drawing' %(doc_main_prefix)
		delText_el = '{%s}delText' %(doc_main_prefix)
		hyperlink_el = '{%s}hyperlink' %(doc_main_prefix)
		fldChar_el = '{%s}fldChar' %(doc_main_prefix)
		fldCharType_att = '{%s}fldCharType' %(doc_main_prefix)
		instrText_el = '{%s}instrText' %(doc_main_prefix)
		footnoteReference_el = '{%s}footnoteReference' %(doc_main_prefix)
		endnoteReference_el = '{%s}endnoteReference' %(doc_main_prefix)
		br_el = '{%s}br' %(doc_main_prefix)
		r_el = '{%s}r' %(doc_main_prefix)

		mc_prefix = docx.nsprefixes['mc']
		AlternateContent_el = '{%s}AlternateContent' %(mc_prefix)
		Choice_el = '{%s}Choice' %(mc_prefix)

		for element in textrun.iterchildren():
				# Look for run properties
				if element.tag == rPr_el:
					me.process_properties( element, doc, rels=rels )
				# Find run text
				elif (element.tag == t_el): 
					# If not character style, append to the end of the paragraph
					found_text = True
					if element.text:
						me.add_child( types.TextNode(element.text) )
				elif (element.tag == tab_el):
					me.add_child(types.TextNode(u'\t')) 
				elif element.tag == drawing_el:
					from .paragraph import Image
					me.add_child( Image.process(element, doc, rels=rels ) )
				# Find 'deleted' text
				elif element.tag == delText_el:
					me.addStyle('strike')
					if element.text:
						me.add_child( types.TextNode(element.text) )
				# Look for hyperlinks
				elif (element.tag == hyperlink_el):
					from .paragraph import Hyperlink
					me.add_child( Hyperlink.process(element, doc, rels = rels) )
				# Look for complex fields
				elif (element.tag == fldChar_el):
					type = element.attrib[fldCharType_att]
					if 'begin' in type:
						# Push the element onto the field stack
						fields.append(element)
					elif 'end' in type:
						elems = []
						# Pop the element off of the field stack
						while fields:
							if not isinstance( fields[len(fields)-1], Run ) \
									and  fldChar_el in fields[len(fields)-1].tag:
								if 'begin' in fields[len(fields)-1].attrib[fldCharType_att]:
									# We have found the begining of the field so pop it off and
									# stop searching
									fields.pop()
									break;
								else:
									fields.pop()
							else:
								elems.append(fields.pop())
								from .paragraph import processComplexField
								me.add_child( processComplexField( elems, doc, rels = rels ) )
					elif 'separate' in type:
						# This node was used to separate the field "command" from the result. It does not seem
						# to make sense with how we are processing the document so it is being ignored.
						pass
	
				# Look for field codes
				elif (element.tag == instrText_el):
					fields.append(element)
	
				# Look for footnotes
				elif (element.tag == footnoteReference_el):
					me.add_child( Note.process(element, doc) )
					pass
				# Look for endnotes
				elif (element.tag == endnoteReference_el):
					me.add_child( Note.process(element, doc) )
					pass
				# Look for carrage returns
				elif (element.tag == br_el):
					from .paragraph import Newline
					me.add_child( types.Newline() )
				# Look for other runs embedded in this run, process recursively
				elif (element.tag == r_el):
					me.add_child( cls.process(element, doc, fields = fields, rels = rels) )
	
				# Skip elements in IGNORED_TAGS
				elif element.tag in IGNORED_TAGS:
					pass

				elif element.tag == AlternateContent_el:
					from .alternate_content import AlternateContent
					me.add_child(AlternateContent.process(element, doc))
					
				# We did not handle the element
				else:
					logger.warn('Did not handle run element: %s', element.tag)
	
		# Remove styles handled in other manners:
		if 'Hyperlink' in me.styles:
			me.removeStyle('Hyperlink')
		elif 'FootnoteReference' in me.styles:
			me.removeStyle('FootnoteReference')
		elif 'FootnoteText' in me.styles:
			me.removeStyle('FootnoteText')
		
		if fields and found_text:
			fields.append( me )
			return me
		elif fields and found_text == False:
			fields.append( me )
			return cls()
		else:
			return me

	def process_properties( self, properties, doc, rels=None ):
		doc_main_prefix = docx.nsprefixes['w']
		att_val = '{%s}val' %(doc_main_prefix)
		rStyle = '{%s}rStyle' %(doc_main_prefix)
		b = '{%s}b' %(doc_main_prefix)
		bCs = '{%s}bCs' %(doc_main_prefix)
		color = '{%s}color' %(doc_main_prefix)
		i = '{%s}i' %(doc_main_prefix)
		iCs = '{%s}iCs' %(doc_main_prefix)
		strike = '{%s}strike' %(doc_main_prefix)
		u = '{%s}u' %(doc_main_prefix)
		rFonts = '{%s}rFonts' %(doc_main_prefix)
		sz = '{%s}sz' %(doc_main_prefix)
		szCs = '{%s}szCs' %(doc_main_prefix)
		w = '{%s}w' %(doc_main_prefix)
		vertAlign = '{%s}vertAlign' %(doc_main_prefix)
		position = '{%s}position' %(doc_main_prefix)

		#this for attribute values (for examine whether we need to set a text bold or not)
		att_val = '{%s}val' %(doc_main_prefix)

		for element in properties.iterchildren():
			if element.tag == rStyle:
				self.addStyle(element.attrib[att_val])
			elif element.tag == b:
				if att_val in element.attrib:
					if element.attrib[att_val] == '0':
						pass
					else:
						self.addStyle('bold')
				else:
					self.addStyle('bold')
			# Ignore bold complex script specification
			elif element.tag == bCs:
				pass
			# Ignore run content color specification
			elif element.tag == color:
				pass
			elif element.tag == i:
				self.addStyle('italic')
			# Ignore italic  complex script specification
			elif element.tag == iCs:
				pass
			elif element.tag == strike:
				self.addStyle('strike')
			elif element.tag == u:
				self.addStyle('underline')
			# Ignore run level font specifications
			elif element.tag == rFonts:
				pass
			# Ignore run level font size specifications
			elif element.tag == sz:
				pass
			# Ignore run level complex script font size specifications
			elif element.tag == szCs:
				pass
			elif element.tag == w:
				pass
			elif element.tag == position:
				pass
			elif element.tag == vertAlign:
				self.addStyle(element.attrib[att_val])
			# Skip elements in IGNORED_TAGS
			elif element.tag in IGNORED_TAGS:
				pass
			else:
				logger.warn('Unhandled run property: %s' % element.tag)






