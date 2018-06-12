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

from nti.contenttools.adapters.epub.prmia.finder import find_superscript_node
from nti.contenttools.adapters.epub.prmia.finder import remove_node_from_parent

from nti.contenttools.util import merge_two_dicts

class Paragraph(types.Paragraph):

	UNORDERED_LIST_DEF = ('list-bulleted-first', 'list-bulleted-middle', )
	IMAGE_DEF = ('image', )
	FIGURE_CAPTION_DEF = ('figcap', )
	SIDEBAR_TITLE_DEF = ('side-title', )
	TABLE_DEF = ('tabcap', )

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
	    	elif any(s.lower() in para_class.lower() for s in cls.SIDEBAR_TITLE_DEF):
	    		node = types.Run()
	    		node.element_type = 'Sidebar Title'
	    		node.children = me.children
	    		me = node
	    	elif para_class == 'footnote':
	    		node = types.Footnote()
	    		node.children = me.children
	    		label_dict = {}
	    		label_ref_dict = {}
	    		sup_nodes = {}
	    		find_superscript_node(node, 'Footnote', label_dict, label_ref_dict, sup_nodes)
	    		if sup_nodes and epub:
	    			for item in sup_nodes:
	    				for child in sup_nodes[item]:
	    					remove_node_from_parent(child)
	    			epub.label_refs = merge_two_dicts(epub.label_refs, label_ref_dict)
	    			footnote_id = label_dict['Footnote_Superscript']
	    			epub.footnote_ids[footnote_id] = node
	    			node.label = types.TextNode(footnote_id)
	    			me = types.Run()
	    		else: 
	    			me = node
	    	elif any(s.lower() in para_class.lower() for s in cls.TABLE_DEF):
	    		node = types.Run()
	    		node.element_type = 'Table'
	    		node.children = me.children
	    		me = node
	    	else:
	    		me.styles.extend(styles)
	    return me
