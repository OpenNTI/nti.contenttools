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


IGNORED_TAGS = [ '{'+docx.nsprefixes['w']+'}ind',
		 '{'+docx.nsprefixes['w']+'}sectPr',
		 '{'+docx.nsprefixes['w']+'}proofErr',
		 '{'+docx.nsprefixes['w']+'}noProof',
		 '{'+docx.nsprefixes['w']+'}commentReference',
		 '{'+docx.nsprefixes['w']+'}commentRangeEnd',
		 '{'+docx.nsprefixes['w']+'}commentRangeStart',
		 '{'+docx.nsprefixes['w']+'}bookmarkEnd',
		 '{'+docx.nsprefixes['w']+'}bookmarkStart',
		 '{'+docx.nsprefixes['w']+'}shd',
		 '{'+docx.nsprefixes['w']+'}contextualSpacing',
		 '{'+docx.nsprefixes['w']+'}tabs',
		 '{'+docx.nsprefixes['w']+'}highlight',
		 '{'+docx.nsprefixes['w']+'}jc',
		 '{'+docx.nsprefixes['w']+'}keepNext',
		 '{'+docx.nsprefixes['w']+'}outlineLvl',
		 '{'+docx.nsprefixes['w']+'}lastRenderedPageBreak',
		 '{'+docx.nsprefixes['w']+'}shd',
		 '{'+docx.nsprefixes['w']+'}spacing',
		 '{'+docx.nsprefixes['w']+'}autoSpaceDE',
		 '{'+docx.nsprefixes['w']+'}autoSpaceDN',
		 '{'+docx.nsprefixes['w']+'}adjustRightInd',
		 '{'+docx.nsprefixes['w']+'}tab',
		 '{'+docx.nsprefixes['w']+'}rtl']

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
		# Scan the elements in the paragraph and extract information
		for element in paragraph.iterchildren():
				# Process Text Runs
				if element.tag == '{'+docx.nsprefixes['w']+'}r':
					me.add_child(Run.process(element, doc, fields = fields, rels = rels))
				# Process 'Deleted' Text Runs
				elif element.tag == '{'+docx.nsprefixes['w']+'}del':
					me.add_child(Del.process(element, doc, fields = fields, rels = rels))
				# Process 'Inserted' Text Runs
				elif element.tag == '{'+docx.nsprefixes['w']+'}ins':
					me.add_child(Ins.process(element, doc, fields = fields, rels = rels))
				# Look for hyperlinks
				elif (element.tag == '{'+docx.nsprefixes['w']+'}hyperlink'):
					me.add_child(Hyperlink.process(element, doc, rels = rels))
				# Paragraph Properties
				elif element.tag == '{'+docx.nsprefixes['w']+'}pPr':
					me.process_properties( element, doc, rels=rels )
				# Skip elements in IGNORED_TAGS
				elif element.tag in IGNORED_TAGS:
					pass

				#handling math equations
				elif element.tag in '{'+docx.nsprefixes['m']+'}oMath':
					me.add_child(OMath.process(element,doc))
				elif element.tag in '{'+docx.nsprefixes['m']+'}oMathPara':
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
		for element in properties.iterchildren():
			# Look for Paragraph Styles
			if element.tag == '{'+docx.nsprefixes['w']+'}pStyle':
				self.addStyle(element.attrib['{'+docx.nsprefixes['w']+'}val'])
			# We don't care about the paragraph mark character in LaTeX so ignore formattingi it.
			elif element.tag == '{'+docx.nsprefixes['w']+'}rPr':
				pass
			# Look for numbering levels
			elif (element.tag == '{'+docx.nsprefixes['w']+'}numPr'):
				self.numbering = process_numbering( element, doc )
			# Skip elements in IGNORED_TAGS
			elif element.tag in IGNORED_TAGS:
				pass
			elif element.tag == '{'+docx.nsprefixes['w']+'}widowControl':
				logger.info('found widowControl property')
			else:
				logger.warn('Unhandled paragraph property: %s' % element.tag)


class Run( types.Run ):

	@classmethod
	def process( cls, textrun, doc, fields = [], rels=None):
		'''Process a paragraph textrun, parse for character styles'''
	
		if rels is None:
				rels = doc.relationships
	
		me = cls()
		found_text = False
		for element in textrun.iterchildren():
				# Look for run properties
				if element.tag == '{'+docx.nsprefixes['w']+'}rPr':
					me.process_properties( element, doc, rels=rels )
				# Find run text
				elif (element.tag == '{'+docx.nsprefixes['w']+'}t'): 
					# If not character style, append to the end of the paragraph
					found_text = True
					if element.text:
						me.add_child( types.TextNode(element.text) )
				elif element.tag == '{'+docx.nsprefixes['w']+'}drawing':
					me.add_child( Image.process(element, doc, rels=rels ) )
					pass
				# Find 'deleted' text
				elif element.tag == '{'+docx.nsprefixes['w']+'}delText':
					me.addStyle('strike')
					if element.text:
						me.add_child( types.TextNode(element.text) )
				# Look for hyperlinks
				elif (element.tag == '{'+docx.nsprefixes['w']+'}hyperlink'):
					 me.add_child( Hyperlink.process(element, doc, rels = rels) )
				# Look for complex fields
				elif (element.tag == '{'+docx.nsprefixes['w']+'}fldChar'):
					type = element.attrib['{'+docx.nsprefixes['w']+'}fldCharType']
					if 'begin' in type:
						# Push the element onto the field stack
						fields.append(element)
					elif 'end' in type:
						elems = []
						# Pop the element off of the field stack
						while fields:
							if not isinstance( fields[len(fields)-1], Run ) \
									and  '{'+docx.nsprefixes['w']+'}fldChar' in fields[len(fields)-1].tag:
								if 'begin' in fields[len(fields)-1].attrib['{'+docx.nsprefixes['w']+'}fldCharType']:
									# We have found the begining of the field so pop it off and
									# stop searching
									fields.pop()
									break;
								else:
									fields.pop()
							else:
								elems.append(fields.pop())
								me.add_child( processComplexField( elems, doc, rels = rels ) )
					elif 'separate' in type:
						# This node was used to separate the field "command" from the result. It does not seem
						# to make sense with how we are processing the document so it is being ignored.
						pass
	
				# Look for field codes
				elif (element.tag == '{'+docx.nsprefixes['w']+'}instrText'):
					fields.append(element)
	
				# Look for footnotes
				elif (element.tag == '{'+docx.nsprefixes['w']+'}footnoteReference'):
					me.add_child( Note.process(element, doc) )
					pass
				# Look for endnotes
				elif (element.tag == '{'+docx.nsprefixes['w']+'}endnoteReference'):
					me.add_child( Note.process(element, doc) )
					pass
				# Look for carrage returns
				elif (element.tag == '{'+docx.nsprefixes['w']+'}br'):
					me.add_child( Newline() )
				# Look for other runs embedded in this run, process recursively
				elif (element.tag == '{'+docx.nsprefixes['w']+'}r'):
					me.add_child( cls.process(element, doc, fields = fields, rels = rels) )
	
				# Skip elements in IGNORED_TAGS
				elif element.tag in IGNORED_TAGS:
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
	numId = ''
	ilvl = 0
	for sub_element in element.iterchildren():
		if (sub_element.tag == '{'+docx.nsprefixes['w']+'}numId'):
			numId = sub_element.attrib['{'+docx.nsprefixes['w']+'}val']
		elif (sub_element.tag == '{'+docx.nsprefixes['w']+'}ilvl'):
			ilvl = int(sub_element.attrib['{'+docx.nsprefixes['w']+'}val'])

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
		if numbering.levels[str(ilvl)].format in fmt_list:
			el = types.OrderedList()
			el.format = numbering.levels[str(ilvl)].format
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


class Note( types.Note ):
	notes = None
	rels = None
	type = ''

	@classmethod
	def process(cls, note, doc):
		rels = None
		
		# Retrieve the endnote Id Number
		id = note.attrib['{'+docx.nsprefixes['w']+'}id']

		me = cls()
		if (note.tag == '{'+docx.nsprefixes['w']+'}footnoteReference'):
			me.notes = doc.footnotes
			me.rels = doc.footnote_relationships
			me.type = 'footnote'
		elif (note.tag == '{'+docx.nsprefixes['w']+'}endnoteReference'):
			me.notes = doc.endnotes
			me.rels = doc.endnote_relationships
			me.type = 'endnote'
		
		# Retrieve the endnote text
		for note in me.notes.iterchildren():
			if note.attrib['{'+docx.nsprefixes['w']+'}id'] == id:
				for element in note.iterchildren():
					# Process paragraphs found in the note
					if element.tag == '{'+docx.nsprefixes['w']+'}p':
						me.add_child(Paragraph.process(element, doc, rels = me.rels))

		return me


class Hyperlink( types.Hyperlink ):

	@classmethod
	def process(cls, node, doc, rels=None ):
		'''Process a hyperlink element'''

		if rels is None:
			rels = doc.relationships

		me = cls()
		#check first if node.attrib.keys() has '{'+docx.nsprefixes['r']+'}id'
		if '{'+docx.nsprefixes['r']+'}id' in node.attrib.keys():
			rId = node.attrib['{'+docx.nsprefixes['r']+'}id']
			rel_type, me.target = relationshipProperties(rId, doc, rels)
		else:
			pass
		for element in node.iterchildren():
			# Look for footnotes
			if (element.tag == '{'+docx.nsprefixes['w']+'}footnoteReference'):
				me.add_child(Note.process(element, doc))
			# Look for endnotes
			elif (element.tag == '{'+docx.nsprefixes['w']+'}endnoteReference'):
				me.add_child(Note.process(element, doc))
			# Look for embedded runs
			if (element.tag == '{'+docx.nsprefixes['w']+'}r'):
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


class Image( types.Image ):
	target = ''
	type = ''
	height = 0
	width = 0

	@classmethod
	def process( cls, image, doc, rels=None ):
		me = cls()
		# Iterate through the image properties and process
		for element in image.iter():
			# Search for Image Properties, contained in blipFill
			if element.tag == '{'+docx.nsprefixes['pic']+'}blipFill':
						me.process_properties( element, doc, rels )
			elif element.tag == '{'+docx.nsprefixes['wp']+'}inline':
						me.process_properties( element, doc, rels )
				
			return me

	def process_properties( self, properties, doc, rels=None ):
		# Retrieve the Image rId and filename
		for element in properties.iter():
			if element.tag == '{'+docx.nsprefixes['a']+'}blip':
				id = element.attrib['{'+docx.nsprefixes['r']+'}embed']
				self.type, self.target = relationshipProperties(id, doc, rels)
				doc.image_list.append(os.path.basename(self.target))
			elif element.tag == '{'+docx.nsprefixes['a']+'}ext':
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

class OMath(types.OMath):
	@classmethod
	def process(cls, omath, doc):
		me = cls()
		for element in omath.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn('Unhandled <o:math> element %s',element.tag)
		return me

class OMathRun(types.OMathRun):
	@classmethod
	def process(cls, mathrun, doc, rels=None):
		me = cls()
		for element in mathrun.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}t':
				if element.text:
					me.add_child(types.TextNode(element.text))
			elif element.tag == '{'+docx.nsprefixes['w']+'}rPr':
				pass
			elif element.tag in IGNORED_TAGS:
				pass
			else:
				logger.warn ('Unhandled <m:r> element %s', element.tag)
		return me

class OMathFrac(types.OMathFrac):
	@classmethod
	def process(cls, mathfrac, doc):
		me = cls()
		for element in mathfrac.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}num':
				me.add_child(OMathNumerator.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}den':
				me.add_child(OMathDenominator.process(element, doc))
		return me

class OMathNumerator(types.OMathNumerator):
	@classmethod
	def process(cls, mathnum, doc):
		me = cls()
		for element in mathnum.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn('Unhandled <m:num> element %s',element.tag)
		return me


class OMathDenominator(types.OMathDenominator):
	@classmethod
	def process(cls, mathden, doc):
		me = cls()
		for element in mathden.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn('Unhandled <m:den> element %s', element.tag)
		return me

class OMathRadical(types.OMathRadical):
	@classmethod
	def process(cls, mathrad, doc):
		me = cls()
		for element in mathrad.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}radPr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}deg':
				me.add_child(OMathDegree.process(element,doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element,doc))
		return me

class OMathDegree(types.OMathDegree):
	@classmethod
	def process(cls, mathdeg, doc):
		me = cls()
		for element in mathdeg.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn('Unhandled <m:deg> element %s', element.tag)
		return me

class OMathBase(types.OMathBase):
	@classmethod
	def process(cls, mathbase, doc):
		me = cls()
		for element in mathbase.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn('Unhandled <m:e> element %s', element.tag)
		return me

class OMathSuperscript(types.OMathSuperscript):
	@classmethod
	def process(cls, mathsup, doc):
		me = cls()
		for element in mathsup.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}sSupPr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sup':
				me.add_child(OMathSup.process(element,doc))
			else:
				logger.warn('Unhandled <m:sSup> element %s', element.tag)
		return me

class OMathSup(types.OMathSup):
	@classmethod
	def process(cls, msup, doc):
		me = cls()
		for element in msup.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn("Unhandled <m:sup> %s", element.tag)
		return me

class OMathSubscript(types.OMathSubscript):
	@classmethod
	def process(cls, mathsub, doc):
		me = cls()
		for element in mathsub.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}sSubPr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sub':
				me.add_child(OMathSub.process(element,doc))
			else:
				logger.warn('Unhandled <m:sSup> element %s', element.tag)
		return me

class OMathSub(types.OMathSub):
	@classmethod
	def process(cls, msub, doc):
		me = cls()
		for element in msub.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn("Unhandled <m:sup> %s", element.tag)
		return me


class OMathSubSup(types.OMathSubSup):
	@classmethod
	def process(cls, msubsup, doc):
		me = cls()
		for element in msubsup.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}sSubSupPr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sub':
				me.add_child(OMathSub.process(element,doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sup':
				me.add_child(OMathSub.process(element,doc))
			else:
				logger.warn('Unhandled <m:sSubSup> element %s', element.tag)
		return me

class OMathNary(types.OMathNary):
	@classmethod
	def process(cls, mnary, doc):
		me = cls()
		for element in mnary.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}naryPr':
				me.add_child(OMathNaryPr.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sub':
				me.add_child(OMathSub.process(element,doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}sup':
				me.add_child(OMathSub.process(element,doc))
			else:
				logger.warn('Unhandled <m:naryPr> element %s', element, tag)
		return me

class OMathNaryPr(types.OMathNaryPr):
	@classmethod
	def process(cls,mnarypr, doc):
		me = cls()
		for element in mnarypr.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}chr':
				me.add_child(process_omath_chr_attributes(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}ctrlPr':
				pass
			else:
				logger.warn('Unhandled <m:naryPr> element %s',element.tag)
		return me

def process_omath_chr_attributes(element, doc):
	chr_val = element.attrib['{'+docx.nsprefixes['m']+'}val']
	el = types.TextNode(chr_val)
	return el

class OMathDelimiter(types.OMathDelimiter):
	@classmethod
	def process(cls, md, doc):
		me = cls()
		for element in md.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}dPr':
				me.add_child(OMathDPr.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			else:
				logger.warn('Unhandled <m:d> element %s',element.tag)
		return me

class OMathDPr(types.OMathDPr):
	@classmethod
	def process(cls, mdpr, doc):
		me = cls()
		for element in mdpr.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}begChr':
				begChr = element.attrib['{'+docx.nsprefixes['m']+'}val']
				me.set_beg_char(begChr)
				#me.add_child(types.TextNode(begChr))
			elif element.tag == '{'+docx.nsprefixes['m']+'}endChr':
				endChr = element.attrib['{'+docx.nsprefixes['m']+'}val']
				me.set_end_char(endChr)
				#me.add_child(types.TextNode(endChr))
			elif element.tag == '{'+docx.nsprefixes['m']+'}ctrlPr':
				pass
			else:
				logger.warn('Unhandled <m:dPr> element %s', element.tag)
		return me

class OMathLimLow(types.OMathLimLow):
	@classmethod
	def process(cls, mlimlow, doc):
		me =cls()
		for element in mlimlow.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}lim':
				me.add_child(OMathLim.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}limLowPr':
				pass
			else:
				logger.warn('Unhandled <m:limlow> element %s', element.tag)
		return me

class OMathLim(types.OMathLim):
	@classmethod
	def process(cls, mlim, doc):
		me = cls()
		for element in mlim.iterchildren():
			new_child = OMathElement.create_child(element,doc)
			if new_child is not None:
				me.add_child(new_child)
			else:
				logger.warn('Unhandled <m:lim> element %s', element.tag)
		return me

class OMathBar(types.OMathBar):
	@classmethod
	def process(cls, mbar, doc):
		me = cls()
		for element in mbar.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}barPr':
				pass
			else:
				logger.warn('Unhandled <m:bar> element %s', element.tag)
		return me

class OMathAcc(types.OMathAcc):
	@classmethod
	def process(cls, macc, doc):
		me = cls()
		for element in macc.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			elif element.tag == '{'+docx.nsprefixes['m']+'}accPr':
				pass
			else:
				logger.warn('Unhandled <m:bar> element %s', element.tag)
		return me

class OMathPara(types.OMathPara):
	@classmethod
	def process(cls, mpara, doc):
		me = cls()
		for element in mpara.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}oMathParaPr':
				pass
			elif element.tag == '{'+docx.nsprefixes['m']+'}oMath':
				me.add_child(OMath.process(element,doc))
			else:
				logger.warn('Unhandled <m:oMathPara> element %s', element.tag)
		return me

class OMathMatrix(types.OMathMatrix):
	@classmethod
	def process(cls, mm, doc):
		me = cls()
		number_of_row = 0
		number_of_col = 0
		for element in mm.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}mPr':
				number_of_col = process_matrix_property(element,doc)
				me.set_number_of_col(number_of_col)
			elif element.tag == '{'+docx.nsprefixes['m']+'}mr':
				number_of_row = number_of_row + 1
				me.add_child(OMathMr.process(element,doc))
			else:
				logger.warn('Unhandled <m:m> element %s', element.tag)
		me.set_number_of_row(number_of_row)
		return me

def process_matrix_property(element, doc):
	number_of_col = 0
	for sub_element in element.iterchildren():
		if sub_element.tag == '{'+docx.nsprefixes['m']+'}ctrlPr':
			pass
		elif sub_element.tag == '{'+docx.nsprefixes['m']+'}mcs':
			for el in sub_element.iterchildren():
				if el.tag == '{'+docx.nsprefixes['m']+'}mc':
					number_of_col = process_mc(el, doc)
		else:
			logger.warn('Unhandled <mPr> element %s', sub_element.tag)
	return number_of_col

def process_mc(element, doc):
	number_of_col = 0
	for sub_element in element.iterchildren():
		if sub_element.tag == '{'+docx.nsprefixes['m']+'}mcPr':
			for el in sub_element.iterchildren():
				if el.tag == '{'+docx.nsprefixes['m']+'}count':
					number_of_col = el.attrib['{'+docx.nsprefixes['m']+'}val']
		else:
			logger.warn('Unhandled <m:mcs> element %s', sub_element.tag)
	return number_of_col


class OMathMr(types.OMathMr):
	@classmethod
	def process(cls, mr, doc):
		me = cls()
		for element in mr.iterchildren():
			if element.tag == '{'+docx.nsprefixes['m']+'}e':
				me.add_child(OMathBase.process(element, doc))
			else:
				logger.warn('Unhandled <m:e> element %s', element.tag)
		return me

class OMathElement(object):
	@classmethod
	def create_child(cls,element,doc):
		if element.tag == '{'+docx.nsprefixes['m']+'}r':
			return(OMathRun.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}f':
			return(OMathFrac.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}rad':
			return(OMathRadical.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}sSup':
			return(OMathSuperscript.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}sSub':
			return(OMathSubscript.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}sSubSup':
			return(OMathSubSup.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}nary':
			return(OMathNary.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}d':
			return(OMathDelimiter.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}limLow':
			return(OMathLimLow.process(element, doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}t':
			if element.text:
				return types.TextNode(element.text)
		elif element.tag == '{'+docx.nsprefixes['m']+'}ctrlPr':
			pass
		elif element.tag == '{'+docx.nsprefixes['m']+'}bar':
			return(OMathBar.process(element,doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}acc':
			return(OMathAcc.process(element,doc))
		elif element.tag == '{'+docx.nsprefixes['m']+'}m':
			return(OMathMatrix.process(element, docx))
		else:
			logger.warn('Unhandled omath element %s', element.tag)
			return None