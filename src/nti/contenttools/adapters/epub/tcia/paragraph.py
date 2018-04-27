#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import copy

from nti.contenttools import types

from nti.contenttools.adapters.epub.tcia import check_child
from nti.contenttools.adapters.epub.tcia import check_element_text
from nti.contenttools.adapters.epub.tcia import check_element_tail

from nti.contenttools.types import Chapter
from nti.contenttools.types import Section

class Paragraph(types.Paragraph):
	CHAPTER_DEF = ('CL-CHPTR-HEADS', )
	SECTION_DEF = ('CL-SUBHEADS', )
	CAPTION_DEF = ('CL-CAPTIONS', )

	@classmethod
	def process(cls, element, styles=(), epub=None):
	    me = cls()
	    me = check_element_text(me, element)
	    me = check_child(me, element, epub)
	    me = check_element_tail(me, element)

	    attrib = element.attrib
	    if 'class' in attrib:
	    	para_class = attrib['class'] if 'class' in attrib else u'' 
	    	if any(s.lower() in para_class.lower() for s in cls.CHAPTER_DEF):
	    		me.styles.append('Chapter')
	    	elif any(s.lower() in para_class.lower() for s in cls.SECTION_DEF):
	    		me.styles.append('Section')

	    	if 'Chapter' in me.styles or 'Section' in me.styles:
	    		label = types.Run()
	    		label.children = me.children
	    		me.label = label

	    return me