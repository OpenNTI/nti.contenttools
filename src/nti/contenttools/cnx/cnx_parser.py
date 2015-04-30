#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: cnx_parser.py 58552 2015-01-29 23:10:30Z egawati.panjei $

Parse each index.cnxml.html found in each module to latex format

"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml import etree, html
from .xml_reader import CNX_XML
from .. import types
import os
import codecs
from .adapters.run_adapter import adapt
from ..util.string_replacer import rename_filename

class CNXParser(object):
	def __init__(self, input_file, output_directory):
		cnx_xml = CNX_XML()
		self.collection = cnx_xml.read_xml(input_file)
		self.image_list = []
		self.latex_filenames = []
		self.content_folder = [] #will be use to retrieve images or pdf
		self.latex_main_files = u''

		head, tail = os.path.split(input_file)
		self.cnx_directory = head
		self.output_directory = output_directory

	def process_collection(self):
		collection = self.collection
		self.metadata = collection.metadata
		content = collection.content
		
		if u'title' in self.metadata : self.latex_main_files  = u'MAIN_%s.tex' %rename_filename(self.metadata[u'title'])

		if content.modules: self.process_modules(content.modules, type_ = u'collection')

		subcollections = content.subcollections
		if subcollections :
			for subcollection in subcollections:
				self.process_subcollection(subcollection)

		self.create_main_latex()

	def process_modules(self, modules, type_ = None, latex_filename = None):
		result = []
		result_append = result.append
		for module in modules:
			doc_content = self.process_document(module.document)
			if type_ == u'collection':
				tex_filename = u'%s.tex' %rename_filename(module.title)
				self.latex_filenames.append(tex_filename)
				#self.write_to_file(u'content test', tex_filename)
			elif type_ == u'subcollection': result_append(doc_content)
		if type_ == u'subcollection' : return u''.join(result)
			

	def process_document(self,document_folder):
		folder = u'%s/%s' %(self.cnx_directory, document_folder)
		self.content_folder.append(folder)
		cnxml_html_file = u'%s/index.cnxml.html' %(folder)
		if os.path.exists(cnxml_html_file):
			with codecs.open( cnxml_html_file, 'r', 'utf-8' ) as file_:
				doc_fragment = html.fromstring(file_.read())
			cnx_html_body = adapt(doc_fragment, self)
		#TODO : render the cnx_html_body
		#return u'only for test.\n' 

	def process_subcollection(self, subcollection):
		tex_filename = u'%s.tex' %rename_filename(subcollection.title)
		self.latex_filenames.append(tex_filename) 
		result = []
		content = subcollection.content
		if content.modules :
			subcollection_content = self.process_modules(content.modules, type_ = u'subcollection', latex_filename = tex_filename) 
			self.write_to_file(subcollection_content, tex_filename)

	def write_to_file(self, content, filename, type_= None):
		if type_ is None : filepath = u'%s/%s' %(self.output_directory, filename) 
		with codecs.open(filepath,'w', 'utf-8') as file_:
			file_.write(content)

	def create_main_latex(self):
		main_tex_content = generate_main_tex_content(self.metadata, self.latex_filenames)
		self.write_to_file(main_tex_content, self.latex_main_files)


def get_packages():
	LATEX_PACKAGES = [u'graphix', 
				 u'hyperref', 
				 u'ulem', 
				 u'Tabbing', 
				 u'textgreek', 
				 u'amsmath', 
				 u'nticourse', 
				 u'ntilatexmacros', 
				 u'ntiassessment',
				 u'ntislidedeck',
				 u'ntiglossary']
	package_list = []
	package_list_append = package_list.append
	for package in LATEX_PACKAGES:
		string = u'\\usepackage{%s}\n' %(package)
		package_list_append(string)
	return u''.join(package_list)

def get_included_tex(included_tex_list):
	result = []
	result_append = result.append
	for tex in included_tex_list:
		inc = u'\\include{%s}\n' %(tex)
		result_append(inc)
	return u''.join(result)


def generate_main_tex_content(metadata, included_tex_list):
	title = u'\\title{%s}\n' %metadata[u'title'] if 'title' in metadata else u''
	author = u'\\author{%s}\n' %metadata[u'author'] if 'author' in metadata else u''
	package = get_packages()
	latex = get_included_tex(included_tex_list)
	return u'\\documentclass{book}\n%s%s%s\\begin{document}\n%s\\end{document}' %(package, title, author, latex)


def main():
	cnx_parser = CNXParser(u'collection.xml')
	result =  cnx_parser.process_collection()
	logger.info(cnx_parser.latex_main_files)
	logger.info(cnx_parser.latex_filenames)
	logger.info(cnx_parser.content_folder)

if __name__ == '__main__':
	main()