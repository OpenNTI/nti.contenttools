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

from . import process_border
from . import properties as docx
from ..types import _Node
from .. import types
from .omath import OMathPara, OMath
from .run import Run
from .ignored_tags import IGNORED_TAGS

class Paragraph( types.Paragraph ):

	def __init__(self):
		super( Paragraph, self ).__init__()
		self.numbering = None

	@classmethod
	def process(cls, paragraph, doc, rels=None):
		'''Processes the text of a given paragraph into insets and text.'''
		
		if rels is None:
				rels = doc.relationships
	
		me = cls()
		fields = []
		doc_main_prefix = docx.nsprefixes['w']
		r_el = '{%s}r' %(doc_main_prefix)
		del_el = '{%s}del' %(doc_main_prefix)
		ins_el = '{%s}ins' %(doc_main_prefix)
		hyperlink_el = '{%s}hyperlink' %(doc_main_prefix)
		pPr_el = '{%s}pPr' %(doc_main_prefix)

		doc_math_prefix = docx.nsprefixes['m']
		oMath_el = '{%s}oMath' %(doc_math_prefix)
		oMathPara_el = '{%s}oMathPara' %(doc_math_prefix)

		# Scan the elements in the paragraph and extract information
		for element in paragraph.iterchildren():
				# Process Text Runs
				if element.tag == r_el:
					me.add_child(Run.process(element, doc, fields = fields, rels = rels))
				# Process 'Deleted' Text Runs
				elif element.tag == del_el:
					me.add_child(Del.process(element, doc, fields = fields, rels = rels))
				# Process 'Inserted' Text Runs
				elif element.tag == ins_el:
					me.add_child(Ins.process(element, doc, fields = fields, rels = rels))
				# Look for hyperlinks
				elif element.tag == hyperlink_el:
					me.add_child(Hyperlink.process(element, doc, rels = rels))
				# Paragraph Properties
				elif element.tag == pPr_el:
					me.process_properties( element, doc, rels=rels )
				# Skip elements in IGNORED_TAGS
				elif element.tag in IGNORED_TAGS:
					pass

				#handling math equations
				elif element.tag == oMath_el:
					me.add_child(OMath.process(element,doc))
				elif element.tag == oMathPara_el:
					me.add_child(OMathPara.process(element,doc))

				# We did not handle the element
				else:
					logger.warn('Did not handle paragraph element: %s' % element.tag)
	
		# Check to see if we found the document title
		if 'Title' in me.styles:
				me.removeStyle('Title')
				doc.title = me.raw().strip()
				me = None
		else:
				# Check for NTI Tags
				s,v = doc.tagparser.parse_line( me.raw() )
				if s != 'IDLE':
					me = None
				if v:
					me = v
	
		if me is not None and hasattr(me, 'numbering') and me.numbering is not None:
				item = types.Item()
				item.add_child(me)
				me.numbering.add_child( item )
				me = me.numbering

		return me

	def process_properties( self, properties, doc, rels=None ):
		doc_main_prefix = docx.nsprefixes['w']
		pStyle_el = '{%s}pStyle' %(doc_main_prefix)
		rPr_el = '{%s}rPr' %(doc_main_prefix)
		numPr_el = '{%s}numPr' %(doc_main_prefix)
		widowControl_el = '{%s}widowControl' %(doc_main_prefix)
		att_val = '{%s}val' %(doc_main_prefix)
		textAlignment = '{%s}textAlignment' %(doc_main_prefix)

		self.vert_alignment = u''

		for element in properties.iterchildren():
			# Look for Paragraph Styles
			if element.tag == pStyle_el:
				self.addStyle(element.attrib[att_val])
			# We don't care about the paragraph mark character in LaTeX so ignore formattingi it.
			elif element.tag == rPr_el:
				pass
			# Look for numbering levels
			elif element.tag == numPr_el:
				self.numbering = process_numbering( element, doc )
			# Skip elements in IGNORED_TAGS
			elif element.tag in IGNORED_TAGS:
				pass
			elif element.tag == widowControl_el:
				#logger.info('found widowControl property')
				pass
			elif element.tag == textAlignment:
				self.vert_alignment = element.attrib[att_val]
			else:
				logger.warn('Unhandled paragraph property: %s' % element.tag)


class Del( Run ):
	pass


class Ins( Run ):

	@classmethod
	def process( cls, element, doc, fields=None, rels=None ):
		me = super( Ins, cls ).process( element, doc, fields, rels )
		me.addStyle('inserted')
		return me

class Newline( types.Note ):
	pass


def process_numbering( element, doc ):
	doc_main_prefix = docx.nsprefixes['w']
	numId_el = '{%s}numId' %(doc_main_prefix)
	ilvl_el = '{%s}ilvl' %(doc_main_prefix)
	att_val = '{%s}val' %(doc_main_prefix)
	numId = ''
	ilvl = 0
	for sub_element in element.iterchildren():
		if (sub_element.tag == numId_el):
			numId = sub_element.attrib[att_val]
		elif (sub_element.tag == ilvl_el):
			ilvl = int(sub_element.attrib[att_val])

	if numId in doc.numbering_collection:
		if ilvl < len(doc.numbering_collection[numId]):
			doc.numbering_collection[numId][ilvl].append( _Node() )
			if ilvl > 0:
				doc.numbering_collection[numId][ilvl-1][-1].add_child(doc.numbering_collection[numId][ilvl][-1])
		else:
			doc.numbering_collection[numId].append([])
			doc.numbering_collection[numId][ilvl].append( _Node() )
			if ilvl > 0:
				doc.numbering_collection[numId][ilvl-1][-1].add_child(doc.numbering_collection[numId][ilvl][-1])
	else:
		doc.numbering_collection[numId] = []
		doc.numbering_collection[numId].append( [] )
		doc.numbering_collection[numId][ilvl].append( _Node() )

	fmt_list = [ 'decimal', 'lowerLetter', 'upperLetter', 'lowerRoman', 'upperRoman' ]
	if numId in doc.numbering:
		numbering = doc.numbering[numId]
		if len(numbering.levels) > 0:
			if numbering.levels[str(ilvl)].format in fmt_list:
				el = types.OrderedList()
				el.format = numbering.levels[str(ilvl)].format
			else:
				el = types.UnorderedList()
		else:
			el = types.UnorderedList()	
	else:
		el = types.UnorderedList()

	if ilvl > 0:
		el.start = len(doc.numbering_collection[numId][ilvl][-1].__parent__.children)
	else:
		el.start = len(doc.numbering_collection[numId][ilvl])
	el.group = numId
	el.level = str(ilvl)
	return el


class Hyperlink( types.Hyperlink ):

	@classmethod
	def process(cls, node, doc, rels=None ):
		'''Process a hyperlink element'''

		if rels is None:
			rels = doc.relationships

		me = cls()
		doc_rels_prefix = docx.nsprefixes['r']
		id_el = '{%s}id' %(doc_rels_prefix)
		#check first if node.attrib.keys() has '{'+docx.nsprefixes['r']+'}id'
		if id_el in node.attrib.keys():
			rId = node.attrib['{'+docx.nsprefixes['r']+'}id']
			rel_type, me.target = relationshipProperties(rId, doc, rels)
		else:
			pass

		doc_main_prefix = docx.nsprefixes['w']
		fnref_el = '{%s}footnoteReference' %(doc_main_prefix)	
		enref_el = '{%s}endnoteReference' %(doc_main_prefix)
		r_el = '{%s}r' %(doc_main_prefix)	
		for element in node.iterchildren():
			# Look for footnotes
			if (element.tag == fnref_el):
				me.add_child(Note.process(element, doc))
			# Look for endnotes
			elif (element.tag == enref_el):
				me.add_child(Note.process(element, doc))
			# Look for embedded runs
			if (element.tag == r_el):
				me.add_child(Run.process(element, doc, rels = rels))

		return me

	def process_target(self):
		text = self.raw()

		if 'YouTube Video' in text:
			scheme = ''
			netloc = 'www.youtube.com'
			path = '/embed'
			query = { 'html5': '1', 'rel': '0' }
			parsed_url = urlparse.urlsplit( self.target )

			if len(parsed_url.path.split('/')) > 2:
				# Then assume that we were passed a more complete URL
				path = parsed_url.path
			else:
				# Assume we were given a 'shortened' URL.
				path = path + parsed_url.path

			# Add any query args to ours
			query.update( urlparse.parse_qsl(parsed_url.query) )
			self.target = urlparse.urlunsplit( (scheme, netloc, path, urllib.urlencode(query), '') )
			self.type = 'YouTube'
		elif 'Thumbnail' in text:
			self.type = 'Thumbnail'
		else:
			self.type = 'Normal'


class Image( types.DocxImage ):
	target = ''
	type = ''
	height = 0
	width = 0

	@classmethod
	def process( cls, image, doc, rels=None ):
		me = cls()
		drawing_el = '{%s}drawing' %(docx.nsprefixes['w'])
		blipFill_el = '{%s}blipFill' %(docx.nsprefixes['pic'])
		inline_el = '{%s}inline' %(docx.nsprefixes['wp'])
		# Iterate through the image properties and process
		for element in image.iter():
			# Search for Image Properties, contained in blipFill
			if element.tag == blipFill_el:
				me.process_properties( element, doc, rels )
			elif element.tag == inline_el:
				me.process_properties( element, doc, rels )
			elif element.tag == drawing_el:
				me.process_properties(element, doc, rels)
			else:
				logger.warn('Unhandled image element %s', element.tag)
			return me

	def process_properties( self, properties, doc, rels=None ):
		# Retrieve the Image rId and filename
		blip_el = '{%s}blip' %(docx.nsprefixes['a'])
		embed_att = '{%s}embed' %(docx.nsprefixes['r'])
		ext_el = '{%s}ext' % docx.nsprefixes['a']
		for element in properties.iter():
			if element.tag == blip_el:
				id = element.attrib[embed_att]
				self.type, self.target = relationshipProperties(id, doc, rels)
				doc.image_list.append(os.path.basename(self.target))
			elif element.tag == ext_el:
				# Convert EMU to inches and then to pixels.
				# 1 inch = 914400 EMU, 72 pixels = 1 inch 
				if 'cy' in element.attrib:
					self.height = int(float(element.attrib['cy']) / 914400 * 72)
				if 'cx' in element.attrib:
					self.width = int(float(element.attrib['cx']) / 914400 * 72)
		# Set the image path
		self.path = os.path.join( doc.image_dir , os.path.splitext( os.path.basename(self.target) )[0] )


def processField( field, doc, result, rels=None ):
	if rels is None:
		rels = doc.relationships

	_t = None
	field_code = field.split()
	if field_code and field_code[0] == 'HYPERLINK':
		_t = Hyperlink()
		_t.add_child(result)
		_t.target = field_code[len(field_code)-1].replace('"','')
		_t.process_target()
	else:
		_t = Run()
		logger.warn( 'Unhandled field: %s. Field body: %s' % ( field, str(result) ) )
	return _t

def processComplexField( elements, doc, rels=None ):
	if rels is None:
		rels = doc.relationships

	field = ''
	result = Run()
	for element in elements:
		if isinstance( element, Run ):
			result.add_child( element )
		elif element.tag == '{'+docx.nsprefixes['w']+'}instrText':
			field = field + types.TextNode( element.text )
	return processField( field, doc, result )

def relationshipProperties( rId, doc, rels=None ):
	'''Parse the document relationships to retrieve the type and target for a 
	specified document element.'''

	if rels is None:
		rels = doc.relationships

	# Search through rels to retrieve relationship properties
	for relationship in rels.iter():
		try:
			if relationship.attrib['Id'] == rId:
				return relationship.attrib['Type'], relationship.attrib['Target']
		except:
			pass
