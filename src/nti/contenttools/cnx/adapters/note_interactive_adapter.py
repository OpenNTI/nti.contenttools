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

class NoteInteractive(types.NoteInteractive):
	@classmethod
	def process(cls, element):
		me = cls()
		for child in element:
			if child.tag == u'span':
				data_type = element.attrib[u'data-type'] if u'data-type' in element.attrib else None
				if data_type == u'media':
					el = Run.process(child)
					me = process_note_interactive_media(me, el)
				else:
					me.add_child(Run.process(child))
			else :
				me.add_child(Run.process(child))
		return me

def process_note_interactive_media(note_interactive, media):
	for child in media.children:
		if isinstance(child, types.Image):
			note_interactive.complete_image_path = child.path
			note_interactive.caption = child.caption
	return note_interactive 
                      
