#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools import types

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.adapters.epub.tcia import check_child
from nti.contenttools.adapters.epub.tcia import check_element_text
from nti.contenttools.adapters.epub.tcia import check_element_tail

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
	    text_align = u''
	    if 'class' in attrib:
	    	para_class = attrib['class'] if 'class' in attrib else u'' 
	    	if any(s.lower() in para_class.lower() for s in cls.CHAPTER_DEF):
	    		me.styles.append('Chapter')
	    		generate_label_from_node_children(me)
	    	elif any(s.lower() in para_class.lower() for s in cls.SECTION_DEF):
	    		me.styles.append('Section')
	    		generate_label_from_node_children(me)
	    	else:
	    		para_class = u'p_%s' % para_class.replace('-', '_')
	    		if epub is not None and para_class in epub.css_dict:
					if 'textAlign' in epub.css_dict[para_class]:
					    if epub.css_dict[para_class]['textAlign'] == u'center':
					        el = types.CenterNode()
					        el.children = me.children
					        me = el
					    elif epub.css_dict[para_class]['textAlign'] == u'left':
					        if 'textIndent' in epub.css_dict[para_class]:
					            if epub.css_dict[para_class]['textIndent'] == u'-45px':
					                el = types.BlockQuote()
					                el.children = me.children
					                me = el
                check_node = render_output(me)
                if u'*' in check_node:
					li = types.Item()
					ul = types.UnorderedList()
					li.add(types.TextNode(check_node.replace(u'*', u'').strip()))
					ul.add(li)
					me = ul
	    return me

def generate_label_from_node_children(base):
	label = types.Run()
	label.children = base.children
	base.label = label