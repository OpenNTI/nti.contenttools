#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: math_adapter.py 58552 2015-01-29 23:10:30Z egawati.panjei $
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
from .image_adapter import Image

class NoteInteractive(types.NoteInteractive):
	@classmethod
	def process(cls, element):
		me = cls()
		notes = Run()
		for child in element:
			if child.tag == u'span':
				data_type = child.attrib[u'data-type'] if u'data-type' in element.attrib else None
				if data_type == u'media':
					me = process_note_interactive_media(me, child)
				else:
					notes.add_child(Run.process(child))
			else :
				notes.add_child(Run.process(child))
		me.notes = notes
		return me

def process_note_interactive_media(note_interactive,element):
	for child in element:
		if child.tag == 'img':
			img = Image.process(child)
			note_interactive.complete_image_path = img.path
			note_interactive.caption = img.caption
	return note_interactive

                      
