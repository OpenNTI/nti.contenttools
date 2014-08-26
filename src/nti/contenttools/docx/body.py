#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import properties as docx

from .. import types
from .paragraph import Paragraph
from .table import Table

IGNORED_TAGS = [ '{'+docx.nsprefixes['w']+'}sectPr']

class Body( types.Body ):

	@classmethod
	def process(cls, body, doc, rels=None ):
		"""
		Process the content of a WordprocessingML body tag.
		"""
	
		if rels is None:
				rels = doc.relationships
	
		me = cls()
		doc_main_prefix = docx.nsprefixes['w']
		p_el = '{%s}p' %(doc_main_prefix)
		tbl_el = '{%s}tbl' %(doc_main_prefix)
		for element in body.iterchildren():
	
				# P (paragraph) Elements
				if element.tag == p_el:
					me.add_child( Paragraph.process(element, doc, rels = rels) )
	
				# T (table) Elements
				elif element.tag == tbl_el:
					me.add_child( Table.process(element, doc, rels = rels) )

				elif element.tag in IGNORED_TAGS:
					pass
	
				else:
					logger.warn('Did not handle body element: %s' % element.tag)
	
		me.children = _consolidate_lsts( me.children )
	
		return me

def _consolidate_lsts( lst = [] ):
	new_lst = []
	for i in range(len(lst)):
		if isinstance(lst[i], list) and (i + 1 < len(lst)) and isinstance(lst[i+1], list) and lst[i].group == lst[i+1].group:
			if lst[i].level == lst[i+1].level:
				for child in lst[i+1].children:
					lst[i].add_child( child )
					lst[i+1] = lst[i]
			elif lst[i].level < lst[i+1].level:
				lst[i].add_child( lst[i+1] )
				lst[i+1] = lst[i]
			else:
				lst[i].children = _consolidate_lsts( lst[i].children )
				new_lst.append( lst[i] )
		else:
			if isinstance(lst[i], list):
				lst[i].children = _consolidate_lsts( lst[i].children )
			new_lst.append( lst[i] )
	return new_lst
	
