# word2lyx is a document parsing script used to 
# convert Microsoft Word documents to LyX documents.
# (C) Robert Oakes, 2012. Released under the terms
# of the GNU Lesser General Public License (LGPL).
# Preferred Dependencies: lxml, elyxer

import os

from zipfile import ZipFile
from parser import ElementTree

from .document import Document
from .numbering import process_numbering
from ..tag_parser import NTITagParser

DEFAULT_RELATIONSHIPS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>
"""

DEFAULT_FOOTNOTES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
"""

class DocxFile( object ):

    def __init__( self, filename, image_dir='Images' ):
        self.zip = ZipFile( filename )
        self.image_dir = image_dir
        self.title = u''
	_document = ElementTree.fromstring(self.zip.read('word/document.xml'))
	self.relationships = ElementTree.fromstring(self.zip.read('word/_rels/document.xml.rels'))
	try:
            self.footnotes = ElementTree.fromstring(self.zip.read('word/footnotes.xml'))
	except KeyError:
            self.footnotes = None
	try:
	    self.footnote_relationships = ElementTree.fromstring(self.zip.read('word/_rels/footnotes.xml.rels'))
	except KeyError:
	    self.footnote_relationships = ElementTree.fromstring(DEFAULT_RELATIONSHIPS)
        try:
            self.endnotes = ElementTree.fromstring(self.zip.read('word/endnotes.xml'))
        except KeyError:
            self.endnotes = None
        try:
            self.endnote_relationships = ElementTree.fromstring(self.zip.read('word/_rels/endnotes.xml.rels'))
        except KeyError:
            self.endnote_relationships = ElementTree.fromstring(DEFAULT_RELATIONSHIPS)
	try:
            a, n = process_numbering(ElementTree.fromstring(self.zip.read('word/numbering.xml')))
            self.abstract_numbering = a
            self.numbering = n
	except KeyError:
            self.abstract_numbering = {}
            self.numbering = {}
	self.styles = ElementTree.fromstring(self.zip.read('word/styles.xml'))
	self.fonts = ElementTree.fromstring(self.zip.read('word/fontTable.xml'))

        self.image_list = []

        # The numbering_collection attribute is used to determine what the next list item's number is
        self.numbering_collection = {}
        self.tagparser = NTITagParser()
        # This call needs to be last, because we rely on other parts of this object to be initialized first
        self.document = Document.process( _document, self )
        self.document.title = self.title

    def get_images( self, dest ):
	'''Retrieve a list of images from the specified document, 
	which are then copied to the target destination directory.
	Returns true or false. True if all images were copied correctly. False if otherwise.'''

	# Check Destination Directory to see if it exists, if not create it
	if not os.path.exists(dest):
		os.mkdir(dest)
	media_dir = 'word/media/'
	    
	# Try to retrieve images from the media folder of the document
	for image in self.image_list:
		image_zippath = media_dir+image
		image_data = self.zip.read(image_zippath)
		image_outfile = open(os.path.join(dest,image), 'wb')
		image_outfile.writelines(image_data)
		image_outfile.close()
	return True

    def render(self):
        return self.document.render()
