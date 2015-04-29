#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: cnx_parser.py 58552 2015-01-29 23:10:30Z egawati.panjei $

Parse each index.cnxml.html found in each module to latex format

"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .xml_reader import CNX_XML
from .. import types
import os


class CNXParser(object):
	def __init__(self, filename):
		cnx_xml = CNX_XML()
		self.collection = cnx_xml.read_xml(filename)
		self.image_list = u''
		self.folder_list = u''
		self.latex_filenames = []

		head, tail = os.path.split(filename)
		self.cnx_directory = head

	def process_collection(self):
		collection = self.collection
		metadata = collection.metadata
		content = collection.content
		
		if u'title' in metadata : main_file_tex  = metadata[u'title']

		if content.modules: 
			self.process_modules(content.modules, type_ = u'collection')

		subcollections = content.subcollections
		if subcollections :
			for subcollection in subcollections:
				self.process_subcollection(subcollection)

	def process_modules(self, modules, type_ = None, latex_filename = None):
		for module in modules:
			if type_ == u'collection':
				self.latex_filenames.append(module.title)
			self.process_document(module.document)

	def process_document(self,document_folder):
		cnxml_html_file = u'%s/%s/index.cnxml.html' % (self.cnx_directory, document_folder)
		#TODO : call the cnx html adapter here
		#Build the latex content

	def process_subcollection(self, subcollection):
		tex = subcollection.title
		self.latex_filenames.append(tex) 
		result = []
		content = subcollection.content
		if content.modules :
			self.process_modules(content.modules, type_ = u'subcollection', latex_filename = tex) 

def main():
	cnx_parser = CNXParser(u'collection.xml')
	result =  cnx_parser.process_collection()
	print cnx_parser.latex_filenames

if __name__ == '__main__':
	main()