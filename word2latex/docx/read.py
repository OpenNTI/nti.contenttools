#!/usr/bin/python

# word2lyx is a document parsing script used to 
# convert Microsoft Word documents to LyX documents.
# (C) Robert Oakes, 2012. Released under the terms
# of the GNU Lesser General Public License (LGPL).
# Preferred Dependencies: lxml, elyxer

import os, zipfile
from parser import ElementTree as xmlreader


def opendocx(file_name):
	'''Open a docx file, return a document XML tree'''
	zipdoc = zipfile.ZipFile(file_name)
	xmlcontent = zipdoc.read('word/document.xml')
	document = xmlreader.fromstring(xmlcontent)
	return document


def openDocxRelationships(file_name):
	'''Retrieve docx relationships file. The relationships file is a list 
		of the assets that a Word document contains.'''
	zipdoc = zipfile.ZipFile(file_name)
	xmlrels = zipdoc.read('word/_rels/document.xml.rels')
	relationships = xmlreader.fromstring(xmlrels)
	return relationships


def openDocxFootnotesRelationships(file_name):
	'''Retrieve docx relationships file. The relationships file is a list 
		of the assets that a Word document contains.'''
	rel_file = 'word/_rels/footnotes.xml.rels'
	zipdoc = zipfile.ZipFile(file_name)
	try:
		xmlrels = zipdoc.read(rel_file)
		relationships = xmlreader.fromstring(xmlrels)
	except KeyError:
		relationships = None
	return relationships


def openDocxEndnotesRelationships(file_name):
	'''Retrieve docx relationships file. The relationships file is a list 
		of the assets that a Word document contains.'''
	rel_file = 'word/_rels/endnotes.xml.rels'
	zipdoc = zipfile.ZipFile(file_name)
	try:
		xmlrels = zipdoc.read(rel_file)
		relationships = xmlreader.fromstring(xmlrels)
	except KeyError:
		relationships = None
	return relationships


def openDocxStyles(file_name):
	'''Retrieve the docx styles list. The styles list contains information
		about the styles and their properties (including the descriptive name'''
	zipdoc = zipfile.ZipFile(file_name)
	xml_styles = zipdoc.read('word/styles.xml')
	styles = xmlreader.fromstring(xml_styles)
	return styles


def openFontTable(file_name):
	'''Retrieve docx fontTable file. The fontTable file contains information
		about the fonts and styles used in the document.'''
	zipdoc = zipfile.ZipFile(file_name)
	xml_fonts = zipdoc.read('word/fontTable.xml')
	fonts = xmlreader.fromstring(xml_fonts)
	return fonts


def openDocxFootnotes(file_name):
	'''Retrieve the document footnotes.'''
	zipdoc = zipfile.ZipFile(file_name)
	try:
		xml_footnotes = zipdoc.read('word/footnotes.xml')
		footnotes = xmlreader.fromstring(xml_footnotes)
	except KeyError:
                footnotes = None
	return footnotes


def openDocxEndnotes(file_name):
	'''Retrieve the document endnotes.'''
	zipdoc = zipfile.ZipFile(file_name)
	try:
		xml_endnotes = zipdoc.read('word/endnotes.xml')
		endnotes = xmlreader.fromstring(xml_endnotes)
	except KeyError:
                endnotes = None
	return endnotes


def getDocumentImages(document, image_list, dest):
	'''Retrieve a list of images from the specified document, 
	which are then copied to the target destination directory.
	Returns true or false. True if all images were copied correctly. False if otherwise.'''

	# Check Destination Directory to see if it exists, if not create it
	if not os.path.exists(dest):
		os.mkdir(dest)
	media_dir = 'word/media/'
	    
	# Try to retrieve images from the media folder of the document	    
	zipdoc = zipfile.ZipFile(document)
	for image in image_list:
		image_zippath = media_dir+image
		image_data = zipdoc.read(image_zippath)
		image_outfile = open(os.path.join(dest,image), 'wb')
		image_outfile.writelines(image_data)
		image_outfile.close()
	return True
