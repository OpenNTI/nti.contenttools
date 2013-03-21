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
#from docx import _Paragraph, _TextRun

import renders.LaTeX

# Import our content data types:
from .types import _Node
from .types import Document
from .types import DocumentClass
from .types import Title
from .types import UsePackage
from docx.paragraph import List
from docx.paragraph import Paragraph
from docx.table import Table
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
			doc_body = processBody( element, doc ).render()
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
			me.add_child( Paragraph.process(element, doc, rels = rels) )

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
		if isinstance(list[i], List) and (i + 1 < len(list)) and isinstance(list[i+1], List) and list[i].group == list[i+1].group:
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
			if isinstance(list[i], List):
				list[i].children = _consolidate_lists( list[i].children )
			new_list.append( list[i] )
	return new_list
	

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
