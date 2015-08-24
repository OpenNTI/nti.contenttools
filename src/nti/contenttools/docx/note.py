#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ..types import Note

from . import properties as docx

class Note(Note):	
	type = ''
	rels = None
	notes = None

	@classmethod
	def process(cls, note, doc):
		rels = None
		doc_main_prefix = docx.nsprefixes['w']
		id_el = '{%s}id' %(doc_main_prefix)
		# Retrieve the endnote Id Number
		id = note.attrib[id_el]

		me = cls()
		if (note.tag == '{%s}footnoteReference' %(doc_main_prefix)):
			me.notes = doc.footnotes
			me.rels = doc.footnote_relationships
			me.type = 'footnote'
		elif (note.tag == '{%s}endnoteReference' %(doc_main_prefix)):
			me.notes = doc.endnotes
			me.rels = doc.endnote_relationships
			me.type = 'endnote'
		p_el = '{%s}p' %(doc_main_prefix)
		# Retrieve the endnote text
		for note in me.notes.iterchildren():
			if note.attrib[id_el] == id:
				for element in note.iterchildren():
					# Process paragraphs found in the note
					if element.tag == p_el:
						from .paragraph import Paragraph
						me.add_child(Paragraph.process(element, doc, rels = me.rels))

		return me

