#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: xml_reader.py 58552 2015-01-29 23:10:30Z egawati.panjei $

Read the collection.xml and then build a collection tree object.
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml import etree, html
from lxml.html import XHTMLParser
from .cnx_properties import cnx_prefixes
from .. import types

class CNX_XML(object):
	def read_xml(self, filename):
		tree = etree.parse(filename)
		root = tree.getroot()
		me = types.CNXCollection()
		for child in root:
			if child.tag == cnx_prefixes['metadata']:
				me.metadata = self.extract_metadata(child, {})
			elif child.tag == cnx_prefixes['content']:
				me.content = self.extract_content(child)
		return me

	def extract_metadata(self, metadata, metadata_dict):
		metadata_values = cnx_prefixes.values()
		for element in metadata :
			if element.tag in metadata_values:
				idx = element.tag.find(u'}') + 1
				key = element.tag[idx:]
				logger.info(element.tag)
				if element.text is None or element.text.isspace() or len(element.text) == 0:
					metadata_dict = self.check_metadata_child(element, metadata_dict, key)
				else : metadata_dict[key] = element.text
		return metadata_dict

	def check_metadata_child(self, element, metadata_dict, key):
		metadata_dict_child = {}
		metadata_dict_child =  self.extract_metadata(element, metadata_dict_child)
		metadata_dict[key] = metadata_dict_child
		return metadata_dict


	def extract_module(self, module):
		me = types.CNXModule()
		module_attributes = module.attrib
		if u'document' in module_attributes :  me.document = module_attributes[u'document'] 
		for element in module:
			if element.tag == cnx_prefixes['title']: me.title = element.text
		return me


	def extract_subcolletion(self, subcollection):
		me = types.CNXSubcollection()
		for element in subcollection:
			if element.tag == cnx_prefixes[u'title']:
				me.title = element.text
			elif element.tag == cnx_prefixes[u'content']:
				me.content = self.extract_content(element)
		return me

	def extract_content(self, content):
		me = types.CNXContent()
		for element in content:
			if element.tag == cnx_prefixes[u'module']:
				me.modules.append(self.extract_module(element))
			elif element.tag == cnx_prefixes[u'subcollection']:
				me.subcollections.append(self.extract_subcolletion(element))
			else:
				print('Unhandled ', element.tag) 
		return me

def main():
	cnx_xml = CNX_XML()
	cnx_collection = cnx_xml.read_xml(u'collection.xml')

if __name__ == '__main__':
	main()

