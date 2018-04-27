#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re
import copy

from nti.contenttools.renderers.LaTeX.base import render_output
from nti.contenttools.renderers.LaTeX.base import render_children_output

from nti.contenttools.renderers.LaTeX.utils import create_label
from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value
from nti.contenttools.renderers.LaTeX.utils import search_run_node_and_remove_styles

from nti.contenttools.types import Run
from nti.contenttools.types import Figure
from nti.contenttools.types import Sidebar
from nti.contenttools.types import TextNode

from nti.contenttools.types.interfaces import IImage
from nti.contenttools.types.interfaces import IParagraph


def search_image_thubms_up_down(root):
	if IImage.providedBy(root):
		if root.inline_image == True and u'Thumbs' in root.path:
			sidebar = Sidebar()
			node = root.__parent__.__parent__.__parent__.__parent__
			parent =  node.__parent__
			index = parent.children.index(node)
			
			parent.remove(node)
			parent.children.insert(index, sidebar)

			figure_thumb = Figure()
			figure_thumb.centered = False
			figure_thumb.floating = True
			figure_thumb.icon = True
			figure_thumb.add(root)
			sidebar.title = Run()
			sidebar.title.add(figure_thumb)	

			next_sibling = parent.children[index+1]
			headers = [] 
			headers = search_chapter_do_dont(next_sibling, headers)
			if headers:
				for item in headers:
					sidebar.title.add(item)
				parent.remove(next_sibling)
				sidebar.add(next_sibling)
	elif hasattr(root, u'children'):
		for child in root:
			search_image_thubms_up_down(child)

def search_chapter_do_dont(root, headers):
	if IParagraph.providedBy(root):
		if 'Chapter' in root.styles:
			check = render_output(root)
			if "{do}" in check.lower() or "{don't}" in check.lower():
				root.styles.remove('Chapter')
				parent = root.__parent__
				parent.remove(root)
				headers.append(root)
	elif hasattr(root, u'children'):
		for child in root:
			search_chapter_do_dont(child, headers)
	return headers

