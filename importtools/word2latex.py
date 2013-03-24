#!/usr/bin/python

# word2lyx is a document parsing script used to 
# convert Microsoft Word documents to LyX documents.
# (C) Robert Oakes, 2012. Released under the terms
# of the GNU Lesser General Public License (LGPL).
# Preferred Dependencies: lxml, elyxer

# Import docx library and supporting tools
import sys 
import os
import codecs

# Import docx parsing classes
from docx.read import DocxFile
from docx import properties as docx

import renders.LaTeX

# Import our content data types:
from .types import DocumentClass
from .types import Title
from .types import UsePackage
from docx.body import Body
from .tag_parser import NTITagParser

##------------ Global Structures ------------## 

IMAGE_FOLDER = 'Images'

##------------ Class Methods ------------## 

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
	doc.IMAGE_FOLDER = IMAGE_FOLDER

	# Iterate over the structure of the document, process document body
	for element in doc.document.iterchildren():

		# Process Elements in Document Body
		if element.tag == '{'+docx.nsprefixes['w']+'}body':
			doc_body = Body.process( element, doc ).render()
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

	output = codecs.open(outputfile, 'w', 'utf-8')
	doc_body = processDocument( doc )
	output.write(doc_body)
	output.close()

	# Copy Document Images to Subfolder
	img_exportfolder = os.path.join(os.path.abspath(os.path.dirname(outputfile)), IMAGE_FOLDER)
	doc.get_images( img_exportfolder )
	
	print 'Conversion successful, output written to ' + outputfile

if __name__ == '__main__': # pragma: no cover
	main()
