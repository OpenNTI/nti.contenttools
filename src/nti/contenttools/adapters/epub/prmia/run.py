#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools import types

from nti.contenttools.adapters.epub.generic.run import Run

from nti.contenttools.adapters.epub.prmia.finder import remove_node_from_parent
from nti.contenttools.adapters.epub.prmia.finder import search_label_node_in_list
from nti.contenttools.adapters.epub.prmia.finder import search_run_node_with_element_type

def process_div_elements(element, parent, epub=None):
    el = Run.process(element, epub=epub)
    attrib = element.attrib
    if 'class' in attrib:
    	div_class = attrib['class']
    	if div_class == 'group':
            image_node = []
            search_run_node_with_element_type(el, 'Figure Image', image_node)
            caption_node = []
            search_run_node_with_element_type(el, 'Figure Caption', caption_node)
            if image_node and caption_node:
            	figure = types.Figure()
            	figure.caption = types.Run()
            	figure.caption.children = caption_node
                figure.children.append(image_node[0].children[1])
                figure.label = image_node[0].children[0]
                el = figure
        elif div_class == 'sidebar':
            sidebar = types.Sidebar()
            sidebar_title_node = []
            search_run_node_with_element_type(el, 'Sidebar Title', sidebar_title_node)
            label = None
            if sidebar_title_node: 
                title_node = sidebar_title_node[0]
                label = search_label_node_in_list(title_node.children[0].children, label)
                sidebar.title = types.Run()
                sidebar.title.children = sidebar_title_node
                if label:
                    sidebar.label = label
                for node in sidebar_title_node:
                    remove_node_from_parent(node)
            sidebar.children = el.children
            el = sidebar
    return el

def process_span_elements(element, epub=None):
    el = Run.process(element, epub=epub)
    return el