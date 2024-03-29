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

from nti.contenttools.adapters.epub.prmia.finder import find_href_node_index

from nti.contenttools.util import merge_two_dicts

class Paragraph(types.Paragraph):

	UNORDERED_LIST_DEF = ('list-bulleted-first', 'list-bulleted-middle', 'list-bulleted-last', 'list-bulleted')
	IMAGE_DEF = ('image', )
	FIGURE_CAPTION_DEF = ('figcap', )
	SIDEBAR_TITLE_DEF = ('side-title', )
	TABLE_DEF = ('tabcap', )
	INDEX_DEF = ('indexmain', 'indexsub')
	FOOTNOTE_SUB_DEF = ('footnote-s1', 'footnote-bull-s1', 'sfootnotebull', 'footnote-bull', 'footnote-bull1')
	CENTER_DEF = ('eq-image', 'center',)

	@classmethod
	def process(cls, element, styles=(), epub=None):
	    me = cls()
	    me = check_element_text(me, element)
	    me = check_child(me, element, epub)
	    me = check_element_tail(me, element)

	    attrib = element.attrib
	    if 'class' in attrib:
	    	para_class = attrib['class'] if 'class' in attrib else u'' 
	    	if any(s.lower() in para_class.lower() for s in cls.CENTER_DEF):
	    		center_node = CenterNode()
	    		center_node.children = me.children
	    		me = center_node
	    	elif para_class.lower() == 'source':
	    		node = types.Run()
	    		node.element_type = 'Source'
	    		node.children = me.children
	    		me = node
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
	    	elif para_class == 'blockquote':
	    		node = BlockQuote()
	    		node.children = me.children
	    		me = node
	    	elif para_class == 'footnote' or para_class == 'sfootnote':
	    		node = types.Footnote()
	    		node.children = me.children
	    		label_dict = {}
	    		label_ref_dict = {}
	    		sup_nodes = {}
	    		find_superscript_node(node, 'Footnote', label_dict, label_ref_dict, sup_nodes)
	    		if sup_nodes and epub:
	    			for item in sup_nodes:
	    				remove_node_from_parent(sup_nodes[item])
	    			epub.label_refs = merge_two_dicts(epub.label_refs, label_ref_dict)
	    			footnote_id = label_dict['Footnote_Superscript']
    				epub.footnote_ids[footnote_id] = node
    				epub.last_footnote_id = footnote_id
    				node.label = types.TextNode(footnote_id)
    				me = types.Run()
	    		else: 
	    			me = node
	    	elif any(s.lower() in para_class.lower() for s in cls.FOOTNOTE_SUB_DEF):
	    		if epub:
	    			node = types.Run()
	    			node.element_type == 'Sub FNote'
	    			if epub.last_footnote_id:
	    				if 'bull' in para_class.lower():
	    					sub_node = types.BlockQuote()
	    					node.add_child(types.TextNode('\n'))
	    					node.add_child(sub_node)
	    				else:
	    					sub_node = types.Run()
	    					node.add_child(types.TextNode('\\\\\n'))
	    					node.add_child(sub_node)
	    				sub_node.children = me.children
	    				last_footnote_node = epub.footnote_ids[epub.last_footnote_id]
	    				last_footnote_node.add_child(node)
	    				me = types.Run()
	    	elif any(s.lower() in para_class.lower() for s in cls.TABLE_DEF):
	    		node = types.Run()
	    		node.element_type = 'Table'
	    		node.children = me.children
	    		me = node
	    	elif any(s.lower() in para_class.lower() for s in cls.INDEX_DEF):
	    		targets = []
	    		find_href_node_index(me, targets)
	    		if 'sub' in para_class:
	    			index_node = BlockQuote()
	    		else:
	    			index_node = types.Paragraph()

	    		text = render_output(me)
	    		index_node.add_child(types.TextNode(text))
	    		for i, item in enumerate(targets):
	    			if item[0] in epub.page_numbers:
	    				node = types.Hyperlink()
	    				node.type = 'ntiidref'
	    				node.target = epub.page_numbers[item[0]]
	    			else:
	    				node = types.Run()
	    			if i == 0:
	    				node.add_child(types.TextNode(item[0]))
	    				if len(item[1].children) > 1:
	    					node.children = node.children + item[1].children[1:]
	    			else:
	    				node.add_child(types.TextNode(item[0]))
	    				if len(item[1].children) > 1:
	    					node.children = node.children + item[1].children[1:]
	    			index_node.add_child(node)
	    		me = index_node
	    	else:
	    		me.styles.extend(styles)
	    return me

def generate_index_reference_description(number):
	node = types.Run()
	node.styles.append('sup')
	node.add_child(types.TextNode(number))
	return node
