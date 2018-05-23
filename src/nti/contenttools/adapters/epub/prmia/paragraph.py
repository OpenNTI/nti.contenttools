#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.adapters.epub.prmia import check_child
from nti.contenttools.adapters.epub.prmia import check_element_text
from nti.contenttools.adapters.epub.prmia import check_element_tail

from nti.contenttools import types

from nti.contenttools.types.note import BlockQuote
from nti.contenttools.types.note import CenterNode

from nti.contenttools.types.lists import Item
from nti.contenttools.types.lists import UnorderedList

class Paragraph(types.Paragraph):

	UNORDERED_LIST_DEF = ('list-bulleted-first', 'list-bulleted-middle', )
	IMAGE_DEF = ('image', )
	FIGURE_CAPTION_DEF = ('figcap', )

	@classmethod
	def process(cls, element, styles=(), epub=None):
	    me = cls()
	    me = check_element_text(me, element)
	    me = check_child(me, element, epub)
	    me = check_element_tail(me, element)

	    attrib = element.attrib
	    if 'class' in attrib:
	    	para_class = attrib['class'] if 'class' in attrib else u'' 
	    	if para_class == 'center':
	    		center_node = CenterNode()
	    		center_node.children = me.children
	    		me = center_node
	    	elif any(s.lower() in para_class.lower() for s in cls.UNORDERED_LIST_DEF):
	    		item = Item()
	    		bullet_class = UnorderedList()
	    		item.children = me.children
	    		bullet_class.children = [item]
	    		me = bullet_class
	    	elif any(s.lower() in para_class.lower() for s in cls.IMAGE_DEF):
	    		node = types.Run()
	    		node.element_type = 'Figure Image'
	    		node.children = me.children
	    		me = node
	    	elif any(s.lower() in para_class.lower() for s in cls.FIGURE_CAPTION_DEF):
	    		node = types.Run()
	    		node.element_type = 'Figure Caption'
	    		node.children = me.children
	    		me = node
	    return me
