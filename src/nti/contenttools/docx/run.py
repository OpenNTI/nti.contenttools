#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from IPython.core.debugger import Tracer

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
					me.add_child( Newline() )
				# Look for other runs embedded in this run, process recursively
				elif (element.tag == r_el):
					me.add_child( cls.process(element, doc, fields = fields, rels = rels) )
	
				# Skip elements in IGNORED_TAGS
				elif element.tag in IGNORED_TAGS:
					pass

				elif element.tag == AlternateContent_el:
					for el in element.iterchildren():
						if el.tag == Choice_el:
							choice_el_child = process_choice_el(el,doc)
							if choice_el_child is not None:
								me.add_child(choice_el_child)
							else:
								pass
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
		for element in properties.iterchildren():
			if element.tag == '{'+docx.nsprefixes['w']+'}rStyle':
				self.addStyle(element.attrib['{'+docx.nsprefixes['w']+'}val'])
			elif element.tag == '{'+docx.nsprefixes['w']+'}b':
				self.addStyle('bold')
			# Ignore bold complex script specification
			elif element.tag == '{'+docx.nsprefixes['w']+'}bCs':
				pass
			# Ignore run content color specification
			elif element.tag == '{'+docx.nsprefixes['w']+'}color':
				pass
			elif element.tag == '{'+docx.nsprefixes['w']+'}i':
				self.addStyle('italic')
			# Ignore italic  complex script specification
			elif element.tag == '{'+docx.nsprefixes['w']+'}iCs':
				pass
			elif element.tag == '{'+docx.nsprefixes['w']+'}strike':
				self.addStyle('strike')
			elif element.tag == '{'+docx.nsprefixes['w']+'}u':
				self.addStyle('underline')
			# Ignore run level font specifications
			elif element.tag == '{'+docx.nsprefixes['w']+'}rFonts':
				pass
			# Ignore run level font size specifications
			elif element.tag == '{'+docx.nsprefixes['w']+'}sz':
				pass
			# Ignore run level complex script font size specifications
			elif element.tag == '{'+docx.nsprefixes['w']+'}szCs':
				pass
			# Skip elements in IGNORED_TAGS
			elif element.tag in IGNORED_TAGS:
				pass
			else:
				logger.warn('Unhandled run property: %s' % element.tag)

def process_choice_el(el,doc):
	doc_main_prefix = docx.nsprefixes['w']
	drawing_el = '{%s}drawing' %(doc_main_prefix)
	for child in el:
		if child.tag == drawing_el:
			from paragraph import Image
			image_child = Image.process(child, doc)
			return image_child
	return None