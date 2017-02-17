#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ... import types
from lxml.html import HtmlComment
import os
import codecs
from ... import scoped_registry
from ... import types
from .run_adapter import Run
from .run_adapter import check_element_text
from .run_adapter import check_element_tail
from .image_adapter import Image

class NoteInteractive(types.NoteInteractive):
	@classmethod
	def process(cls, element):
		me = cls()
		notes = Run()
		me.label = element.attrib['id'] if 'id' in element.attrib else None
		for child in element:
			if child.tag == u'span':
				data_type = child.attrib[u'data-type'] if u'data-type' in element.attrib else None
				if data_type == u'media':
					me = process_note_interactive_media(me, child)
				else:
					me, desc = process_nticard_notes(me, child)
					notes.add_child(desc)
			else :
				me, desc = process_nticard_notes(me, child)
				notes.add_child(desc)
		me.notes = notes
		return me

def process_note_interactive_media(note_interactive,element):
	for child in element:
		if child.tag == 'img':
			img = Image.process(child)
			note_interactive.complete_image_path = img.path
			note_interactive.caption = img.caption
	return note_interactive

def process_nticard_notes(note_interactive, element):
	notes = Run()
	notes = check_element_text(notes, element)
	for child in element:
		if child.tag == 'a':
			if 'href' in child.attrib : 
				note_interactive.link = child.attrib['href']
				notes = check_element_tail(notes, child)
		else:
			notes.add_child(Run.process(child))
	notes = check_element_tail(notes, element)
	return note_interactive, notes



                      
