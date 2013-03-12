#!/usr/bin/python

# word2lyx is a document parsing script used to 
# convert Microsoft Word documents to LyX documents.
# (C) Robert Oakes, 2012. Released under the terms
# of the GNU Lesser General Public License (LGPL).
# Preferred Dependencies: lxml, elyxer

# Import docx library and supporting tools
import math
import sys 
import os
import tempfile
import shutil
import codecs
import urllib
import urlparse

# Import docx parsing classes
from docx.read import DocxFile
from docx import properties as docx
from docx.table import Table
from docx import _Paragraph, _TextRun

# Import our content data types:
from .types import *
from .types import _Node
from .types import _List
from .tag_parser import NTITagParser

##------------ Global Structures ------------## 

CHARSTYLE_LIST = []

IMAGE_FOLDER = 'Images'


##------------ Class Methods ------------## 

CONTAINERS = { 'blockquote': 'quote',
	       'center': 'center' }

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
		 '{'+docx.nsprefixes['w']+'}lastRenderedPageBreak']

PACKAGES = [ 'graphicx',
	     'hyperref',
	     'ulem',
	     'ntilatexmacros',
	     'ntiassessment']

def processDocument( doc ):
	'''Method that parses the input document and translates it to a valid LyX structure. 
	Returns a text string with XML structures translated to equivalent LyX insets. 
	It uses the layouts in article and book as a base. If there are character styles 
	not defined in article or book, it will create placeholder styles using flex:inset.
	These may be modified at a later point by the user.'''

	# Create output strings
	doc_header = []
	doc_body = u''

	doc.tagparser = NTITagParser()
	doc.numbering_collection = {}

	# Iterate over the structure of the document, process document body
	for element in doc.document.iterchildren():

		# Process Elements in Document Body
		if element.tag == '{'+docx.nsprefixes['w']+'}body':
			doc_body = unicode( processBody( element, doc ) )
		else:
			print('Did not handle document element: %s' % element.tag)

	# Create the document header
	# Set the document class
	doc_header.append( DocumentClass('book') )

	# Add packages
	for package in PACKAGES:
		doc_header.append( UsePackage( package ) )

	if hasattr(doc, 'title'):
		doc_header.append( Title( doc.title ) )

	# Combine the document header and body and then return
	return u'\n'.join(doc_header) + '\n' + doc_body

def processBody( body, doc, rels=None ):
	"""Process the content of a WordprocessingML body tag."""

	if rels is None:
		rels = doc.relationships

	me = Document()
	for element in body.iterchildren():

		# P (paragraph) Elements
		if element.tag == '{'+docx.nsprefixes['w']+'}p':
			me.add_child( processParagraph(element, doc, rels = rels) )

		# T (table) Elements
		elif element.tag == '{'+docx.nsprefixes['w']+'}tbl':
			me.add_child( Table.process(element, doc, rels = rels) )

		# Skip elements in IGNORED_TAGS
		elif element.tag in IGNORED_TAGS:
			pass

		else:
			print('Did not handle body element: %s' % element.tag)

	me.children = _consolidate_lists( me.children )

	return me

def _consolidate_lists( list = [] ):
	new_list = []
	for i in range(len(list)):
		if isinstance(list[i], _List) and (i + 1 < len(list)) and isinstance(list[i+1], _List) and list[i].group == list[i+1].group:
			if list[i].level == list[i+1].level:
				for child in list[i+1].children:
					list[i].add_child( child )
				list[i+1] = list[i]
			elif list[i].level < list[i+1].level:
				list[i].add_child( list[i+1] )
				list[i+1] = list[i]
			else:
				list[i].children = _consolidate_lists( list[i].children )
				new_list.append( list[i] )
		else:
			if isinstance(list[i], _List):
				list[i].children = _consolidate_lists( list[i].children )
			new_list.append( list[i] )
	return new_list
	

def processParagraph(paragraph, doc, rels=None ):
	'''Processes the text of a given paragraph into insets and text.'''
	
	if rels is None:
		rels = doc.relationships

	numbering = None
	me = _Paragraph()
	fields = []
	# Scan the elements in the paragraph and extract information
	for element in paragraph.iterchildren():

		# Process Text Runs
		if element.tag == '{'+docx.nsprefixes['w']+'}r':
			me.add_child(processTextRun(element, doc, fields = fields, rels = rels))
			image_text = processRelationship(element, doc)
			if len(image_text) > 0:
				me.add_child(image_text)
		
		# Process 'Deleted' Text Runs
		elif element.tag == '{'+docx.nsprefixes['w']+'}del':
			me.add_child(process_del(element, doc, fields = fields, rels = rels))
		
		# Process 'Inserted' Text Runs
		elif element.tag == '{'+docx.nsprefixes['w']+'}ins':
			me.add_child(process_ins(element, doc, fields = fields, rels = rels))
		
		# Look for hyperlinks
		elif (element.tag == '{'+docx.nsprefixes['w']+'}hyperlink'):
			me.add_child(processHyperlink(element, doc, rels = rels))

		# Paragraph Properties
		elif element.tag == '{'+docx.nsprefixes['w']+'}pPr':
			for sub_element in element.iterchildren():
				# Look for Paragraph Styles
				if sub_element.tag == '{'+docx.nsprefixes['w']+'}pStyle':
					me.addStyle(sub_element.attrib['{'+docx.nsprefixes['w']+'}val'])

				# We don't care about the paragraph mark character in LaTeX so ignore formattingi it.
				elif sub_element.tag == '{'+docx.nsprefixes['w']+'}rPr':
					pass

				# Look for numbering levels
				elif (sub_element.tag == '{'+docx.nsprefixes['w']+'}numPr'):
					numbering = process_numbering( sub_element, doc )

				# Skip elements in IGNORED_TAGS
				elif sub_element.tag in IGNORED_TAGS:
					pass

				else:
					print('Unhandled paragraph property: %s' % sub_element.tag)

		# Skip elements in IGNORED_TAGS
		elif element.tag in IGNORED_TAGS:
			pass

		# We did not handle the element
		else:
			print('Did not handle paragraph element: %s' % element.tag)

	if 'Caption' in me.styles:
		print( 'Caption: ' + unicode(me) )

	if 'ListParagraph' in me.styles:
		print( 'ListParagraph: ' + unicode(me) )

	# Check to see if we found the document title
	if 'Title' in me.styles:
		me.removeStyle('Title')
		doc.title = str(me).strip()
		me = ''
	else:
		# Check for NTI Tags
		s,v = doc.tagparser.parse_line( me.raw() )
		if s != 'IDLE':
			me = ''
		if v:
			me = v

	if numbering is not None:
		numbering.add_child( Item( str(me) ) )
		me = numbering

	return me

def process_del( element, doc, fields=None, rels=None ):
	me = _TextRun()
	for sub_element in element.iterchildren():
		if sub_element.tag == '{'+docx.nsprefixes['w']+'}r':
			me.add_child(processTextRun(sub_element, doc, fields = fields, rels = rels))
			image_text = processRelationship(sub_element, doc)
			if len(image_text) > 0:
				me.add_child(image_text)

		# Skip elements in IGNORED_TAGS
		elif sub_element.tag in IGNORED_TAGS:
			pass

		# We did not handle the element
		else:
			print('Did not handle del element: %s' % sub_element.tag)
	return me

def process_ins( element, doc, fields=None, rels=None ):
	me = _TextRun()
	for sub_element in element.iterchildren():
		if sub_element.tag == '{'+docx.nsprefixes['w']+'}r':
			run = processTextRun(sub_element, doc, fields = fields, rels = rels)
			run.addStyle('inserted')
			me.add_child(run)
			image_text = processRelationship(element, doc)
			if len(image_text) > 0:
				me.add_child(image_text)

		# Skip elements in IGNORED_TAGS
		elif sub_element.tag in IGNORED_TAGS:
			pass

		# We did not handle the element
		else:
			print('Did not handle ins element: %s' % sub_element.tag)
	return me

def processTextRun(textrun, doc, fields = [], rels=None ):
	'''Process a paragraph textrun, parse for character styles'''

	if rels is None:
		rels = doc.relationships

	me = _TextRun()

	for element in textrun.iterchildren():

		# Look for run properties
		if element.tag == '{'+docx.nsprefixes['w']+'}rPr':
			for sub_element in element.iterchildren():
				if sub_element.tag == '{'+docx.nsprefixes['w']+'}rStyle':
					me.addStyle(sub_element.attrib['{'+docx.nsprefixes['w']+'}val'])

				elif sub_element.tag == '{'+docx.nsprefixes['w']+'}b':
                                        me.addStyle('bold')

				# Ignore bold complex script specification
				elif sub_element.tag == '{'+docx.nsprefixes['w']+'}bCs':
                                        pass

				# Ignore run content color specification
				elif sub_element.tag == '{'+docx.nsprefixes['w']+'}color':
                                        pass

				elif sub_element.tag == '{'+docx.nsprefixes['w']+'}i':
                                        me.addStyle('italic')

				# Ignore italic  complex script specification
				elif sub_element.tag == '{'+docx.nsprefixes['w']+'}iCs':
                                        pass

				elif sub_element.tag == '{'+docx.nsprefixes['w']+'}strike':
                                        me.addStyle('strike')

				elif sub_element.tag == '{'+docx.nsprefixes['w']+'}u':
                                        me.addStyle('underline')

				# Ignore run level font specifications
				elif sub_element.tag == '{'+docx.nsprefixes['w']+'}rFonts':
                                        pass

				# Ignore run level font size specifications
				elif sub_element.tag == '{'+docx.nsprefixes['w']+'}sz':
                                        pass

				# Ignore run level complex script font size specifications
				elif sub_element.tag == '{'+docx.nsprefixes['w']+'}szCs':
                                        pass

				# Skip elements in IGNORED_TAGS
				elif sub_element.tag in IGNORED_TAGS:
					pass

				else:
					print('Unhandled run property: %s' % sub_element.tag)

		# Find run text
		elif (element.tag == '{'+docx.nsprefixes['w']+'}t'): 
			# If not character style, append to the end of the paragraph
			if element.text:
				me.add_child( TextNode(element.text) )

		# Find 'deleted' text
		elif element.tag == '{'+docx.nsprefixes['w']+'}delText':
			me.addStyle('strike')
			if element.text:
				me.add_child( TextNode(element.text) )

		# Look for hyperlinks
		elif (element.tag == '{'+docx.nsprefixes['w']+'}hyperlink'):
			me.add_child( processHyperlink(element, doc, rels = rels) )

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
					if not isinstance( fields[len(fields)-1], _TextRun ) \
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
			me.add_child( processFootnote(element, doc) )

		# Look for endnotes
		elif (element.tag == '{'+docx.nsprefixes['w']+'}endnoteReference'):
			me.add_child( processEndnote(element, doc) )

		# Look for carrage returns
		elif (element.tag == '{'+docx.nsprefixes['w']+'}br'):
			me.add_child( Newline() )

		# Look for other runs embedded in this run, process recursively
		elif (element.tag == '{'+docx.nsprefixes['w']+'}r'):
			me.add_child( processTextRun(element, doc, fields = fields, rels = rels) )

		# Skip elements in IGNORED_TAGS
		elif element.tag in IGNORED_TAGS:
			pass

		# We did not handle the element
		else:
			print('Did not handle run element: %s' % element.tag)

	# Remove styles handled in other manners:
	if 'Hyperlink' in me.styles:
		me.removeStyle('Hyperlink')

	if fields:
		fields.append( me )
		return _TextRun()
	else:
		return me

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
			el = Enumerate()
			el.format = numbering.levels[str(ilvl)].format
		else:
			el = Itemize()
	else:
		el = Itemize()

	if ilvl > 0:
		el.start = len(doc.numbering_collection[numId][ilvl][-1].__parent__.children)
	else:
		el.start = len(doc.numbering_collection[numId][ilvl])
	el.group = numId
	el.level = str(ilvl)

	return el

def _buildHref( url, text ):
	if 'YouTube Video' in text:
		scheme = ''
		netloc = 'www.youtube.com'
		path = '/embed'
		query = { 'html5': '1', 'rel': '0' }
		parsed_url = urlparse.urlsplit( url )

		if len(parsed_url.path.split('/')) > 2:
			#Then assume that we were passed a more complete URL
			path = parsed_url.path
		else:
			#Assume we were given a 'shortened' URL.
			path = path + parsed_url.path

		# Add any query args to ours
		query.update( urlparse.parse_qsl(parsed_url.query) )
		target = urlparse.urlunsplit( (scheme, netloc, path, urllib.urlencode(query), '') )
		text = NTIIncludeVideo( target )
	elif 'Thumbnail' in text:
		text = NTIImageHref( url )
	else:
		text = href( url, text)

	return text

def processHyperlink(node, doc, rels=None ):
	'''Process a hyperlink element'''

	if rels is None:
		rels = doc.relationships

	text = ''

	rId = node.attrib['{'+docx.nsprefixes['r']+'}id']
	rel_type, rel_target = relationshipProperties(rId, doc, rels)

	for element in node.iterchildren():
		# Look for footnotes
		if (element.tag == '{'+docx.nsprefixes['w']+'}footnoteReference'):
			text = text + processFootnote(element, doc)

		# Look for endnotes
		if (element.tag == '{'+docx.nsprefixes['w']+'}endnoteReference'):
			text = text + processEndnote(element, doc)

		# Look for embedded runs
		if (element.tag == '{'+docx.nsprefixes['w']+'}r'):
			_t = processTextRun(element, doc, rels = rels).raw()
			text = text + _t

	if text:
		text = _buildHref( rel_target, text )
	else:
		text = ''

	return text

def processField( field, doc, result, rels=None ):
	if rels is None:
		rels = doc.relationships

	text = _TextRun()
	field_code = field.split()

	if field_code and  field_code[0] == 'HYPERLINK':
		text.add_child( _buildHref( field_code[len(field_code)-1].replace('"',''), str(result) ) )
	else:
		print( (field, str(result) ) )
	return text

def processComplexField( elements, doc, rels=None ):
	if rels is None:
		rels = doc.relationships

	field = ''
	result = _TextRun()
	for element in elements:
		if isinstance( element, _TextRun ):
			result.add_child( element )
		elif element.tag == '{'+docx.nsprefixes['w']+'}instrText':
			field = field + TextNode( element.text )
	return processField( field, doc, result )

def processFootnote(footnote_ref, doc):
	'''Locate footnote and write a footnote inset.'''

	# Retrieve the footnote Id Number
	id = footnote_ref.attrib['{'+docx.nsprefixes['w']+'}id']
	text = u''

	# Retrieve the footnote text
	for footnote in doc.footnotes.iterchildren():
		if footnote.attrib['{'+docx.nsprefixes['w']+'}id'] == id:
			for foot_sub in footnote.iterchildren():
				# Process paragraphs found in the note
				if foot_sub.tag == '{'+docx.nsprefixes['w']+'}p':
					text = text + unicode(processParagraph(foot_sub, doc, rels = doc.footnote_relationships))

	# SAJ: In NTI LaTeX footnotes and endnotes are handled identically.
	return Footnote( text )

def processEndnote(endnote_ref, doc):
	'''Locate endnote and write a endnote tag.'''

	# Retrieve the endnote Id Number
	id = endnote_ref.attrib['{'+docx.nsprefixes['w']+'}id']
	text = u''

	# Retrieve the endnote text
	for endnote in doc.endnotes.iterchildren():
		if endnote.attrib['{'+docx.nsprefixes['w']+'}id'] == id:
			for end_sub in endnote.iterchildren():
				# Process paragraphs found in the note
				if end_sub.tag == '{'+docx.nsprefixes['w']+'}p':
					text = text + unicode(processParagraph(end_sub, doc, rels = doc.endnote_relationships))

	# SAJ: In NTI LaTeX footnotes and endnotes are handled identically.
	return Footnote( text )

def processRelationship(relationship, doc):
	'''Process relationships in the document. '''
	rel_text = u''
	
	# Iterate through the relationship properties, process
	for element in relationship.iter():
		if element.tag == '{'+docx.nsprefixes['w']+'}drawing':
			rel_text = processImage(element, doc)
	return rel_text


def processImage(image, doc):
	'''Process images in the document. Specify that image should be copied from the 
		zip archive to a destination directory. Add a LyX image inset to the document. 
		The method ignores Microsoft specific charts and other files that have been 
		embedded.'''

	data = {}

	# Iterate through the image properties, process
	for element in image.iter():
		# Search for Image Properties, contained in blipFill
		if element.tag == '{'+docx.nsprefixes['pic']+'}blipFill':

			# Retrieve the Image rId and filename
			for imageprop in element.iter():
				if imageprop.tag == '{'+docx.nsprefixes['a']+'}blip':
					data['id'] = imageprop.attrib['{'+docx.nsprefixes['r']+'}embed']
					data['type'], data['target'] = relationshipProperties(data['id'], doc)
					doc.image_list.append(os.path.basename(data['target']))
					break
		elif element.tag == '{'+docx.nsprefixes['wp']+'}inline':
			for imageprop in element.iter():
				if imageprop.tag == '{'+docx.nsprefixes['a']+'}ext':
					# Convert EMU to inches. 1 inch = 914400 EMU
					if 'cy' in imageprop.attrib:
						data['height'] = (float(imageprop.attrib['cy']) / 914400)
					if 'cx' in imageprop.attrib:
						data['width'] = (float(imageprop.attrib['cx']) / 914400)
			
	# SAJ: We are width constrained. If we only set the width attribute LaTeX will make sure 
	# we preserve aspect ratio.
	parms = None
	if 'width' in data:
		# SAJ: The constant 72 is for 72 dpi which is what ghostscript assumes for pixel / inch 
		# conversions. Because the number of pixels needs to be and integer, take the ceiling of
		# the result and then force to an int.
		width = int(math.ceil(data['width'] * 72))
		# SAJ: Cap width at our max width. Need to make this a constant variable.
		if width > 600:
			width = 600
		parms = 'width=%spx' % width

	# Write inset to file, ignore charts and other types of files
	if 'type' in data and data['type'] == docx.nsprefixes['wordimage']:
		text = '\n'  + \
		    Image( os.path.join( IMAGE_FOLDER , os.path.splitext( os.path.basename(data['target']) )[0] ), 
			      parms) + \
		    '\n\n'
	else:
		text = ''

	return text


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


def processStyleAttributes(charstyle, doc_styles, doc_fonts):
	'''Look at the document style information and font information to find relevant'''
	
	# Create Property Lists
	shape = []
	series = []
	misc = []
	
	# Locate the info for the charstyle
	for style in doc_styles.iterchildren():
		if style.tag == '{'+docx.nsprefixes['w']+'}style':
			# Parse the general properties for the style
			if style.attrib['{'+docx.nsprefixes['w']+'}styleId'] == charstyle.styleName:
				
				# Iterate through the style properties
				for style_prop in style.iterchildren():

					# Retrieve the Parent Style Information
					if style_prop.tag == '{'+docx.nsprefixes['w']+'}basedOn':
						charstyle.fontData['ParentStyle'] = style_prop.attrib['{'+docx.nsprefixes['w']+'}val']

					# Look at the run properties (rPr) to determine text shape and series
					if style_prop.tag == '{'+docx.nsprefixes['w']+'}rPr':

						# Iterate through property elements
						for rPr in style_prop.iterchildren():

							# Bold Weight
							if rPr.tag == '{'+docx.nsprefixes['w']+'}b':
								if checkStyleAttrib(rPr.attrib): series.append('Bold')
							
							# Italic
							if rPr.tag == '{'+docx.nsprefixes['w']+'}i':
								if checkStyleAttrib(rPr.attrib): shape.append('Italic')

							# Uppercase
							if rPr.tag == '{'+docx.nsprefixes['w']+'}caps':
								if checkStyleAttrib(rPr.attrib): shape.append('Up')

							# Small Caps
							if rPr.tag == '{'+docx.nsprefixes['w']+'}smallCaps':
								if checkStyleAttrib(rPr.attrib): shape.append('SmallCaps')

							# Font Properties
							if rPr.tag == '{'+docx.nsprefixes['w']+'}rFonts':
								if '{'+docx.nsprefixes['w']+'}cs' in rPr.attrib.keys():
									charstyle.fontData['fontname'] = rPr.attrib['{'+docx.nsprefixes['w']+'}cs']
								elif '{'+docx.nsprefixes['w']+'}ascii' in rPr.attrib.keys():
									charstyle.fontData['fontname'] = rPr.attrib['{'+docx.nsprefixes['w']+'}ascii']
								elif '{'+docx.nsprefixes['w']+'}hAnsi' in rPr.attrib.keys():
									charstyle.fontData['fontname'] = rPr.attrib['{'+docx.nsprefixes['w']+'}hAnsi']
								else:
									charstyle.fontData['fontname'] = ''

	# Look for font characteristsics: family, size
	if charstyle.fontData['fontname'] is not '':

		# Iterate through document fonts to find match
		for font in doc_fonts:
			if charstyle.fontData['fontname'] == font.attrib['{'+docx.nsprefixes['w']+'}name']:
				
				# Parse properties looking for the font-family
				for fontprop in font.iterchildren():
					
					# Translate the family classification from Word to LyX
					if fontprop.tag == '{'+docx.nsprefixes['w']+'}family':
						charstyle.fontData['lyx_family'] = \
							FONT_FAMILIES[fontprop.attrib['{'+docx.nsprefixes['w']+'}val']]

	charstyle.fontData['lyx_series'] = ', '.join(series)
	charstyle.fontData['lyx_shape'] = ', '.join(shape)
	return charstyle

def checkStyleAttrib(attrib):
	'''Check style attributes to determine if a value is disable (val == 0). If disabled, 
	return False. Otherwise, return True.'''
	# Check to see if there are attributes
	if len(attrib) > 0:
		# If the attrib is disabled (val == 0), return false
		if attrib['{'+docx.nsprefixes['w']+'}val'] == '0': return False
	else: return True


#------------ Main Program ------------## 


def main():
	# Get input and output file
	try:
		inputfile = sys.argv[1]
		# Check to see if the file exists
		if not os.path.exists(inputfile):
			print 'Error: Unable to locate input file'
			exit()
		# Check to see if the file is a docx file
		basename = os.path.basename(inputfile)
		fileext = basename.split('.')[len(basename.split('.'))-1]
		if fileext != 'docx':
			print 'Error: Invalid input file. word2lyx only supports docx files.'
			exit()
		outputfile = sys.argv[2]

	# If there is an error encoutered, return general error message
	except:
		print 'lyx2word encountered an error with the file' 
		exit()

	doc = DocxFile( inputfile )

	# Open document from input string
	print "Beginning Conversion of " + inputfile

	lyxoutput = codecs.open(outputfile, 'w', 'utf-8')
	doc_body = processDocument( doc )
	lyxoutput.write(doc_body)
	lyxoutput.close()

	# Copy Document Images to Subfolder
	img_exportfolder = os.path.join(os.path.abspath(os.path.dirname(outputfile)), IMAGE_FOLDER)
	doc.get_images( img_exportfolder )
	
	print 'Conversion successful, output written to ' + outputfile

if __name__ == '__main__': # pragma: no cover
	main()
