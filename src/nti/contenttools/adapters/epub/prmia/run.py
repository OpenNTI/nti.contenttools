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

from nti.contenttools.adapters.epub.prmia.finder import search_a_label_node
from nti.contenttools.adapters.epub.prmia.finder import remove_node_from_parent
from nti.contenttools.adapters.epub.prmia.finder import search_run_node_with_element_type

from nti.contenttools.renderers.LaTeX.base import render_output

def process_div_elements(element, parent, epub=None):
    el = Run.process(element, epub=epub)
    attrib = element.attrib
    if 'class' in attrib:
    	div_class = attrib['class']
    	if div_class == 'group':
            caption_node = []
            search_run_node_with_element_type(el, 'Figure Caption', caption_node)
            table_caption = []
            search_run_node_with_element_type(el, 'Table', table_caption)
            if caption_node:
                image_node = []
                search_run_node_with_element_type(el, 'Figure Image', image_node)
                if image_node:
                    figure = types.Figure()
                    figure.caption = types.Run()
                    figure.caption.children = caption_node
                    inode = types.Run()
                    inode.children = image_node
                    figure.label = get_label_from_node(inode)
                    figure.add_child(inode)
                    el = figure
                    if epub:
                        epub.labels[figure.label] = 'Figure'
            elif table_caption:
                image_node = []
                search_run_node_with_element_type(el, 'Figure Image', image_node, option=True)
                table = types.Table()
                label = get_label_from_node(el)
                table.label = u'\\label{%s}' %(label)
                table.caption = types.Run()
                table.caption.children = table_caption
                table.number_of_col_header = len(image_node)
                table.children = image_node
                if epub:
                    epub.labels[label] = 'Table'
                el = table
        elif div_class == 'sidebar':
            sidebar = types.Sidebar()
            sidebar_title_node = []
            search_run_node_with_element_type(el, 'Sidebar Title', sidebar_title_node)
            label = None
            if sidebar_title_node: 
                sidebar.title = types.Run()
                sidebar.title.children = sidebar_title_node
                label = get_label_from_node(sidebar.title)
                if label:
                    sidebar.label = label
                    if epub:
                        epub.labels[label] = 'Sidebar'
                for node in sidebar_title_node:
                    remove_node_from_parent(node)
            sidebar.children = el.children
            el = sidebar
    return el

def process_sup_elements(element, parent, epub=None):
    el = Run.process(element, styles=('sup',), epub=epub)
    el.element_type = 'Superscript'
    return el

def process_span_elements(element, epub=None):
    el = Run.process(element, epub=epub)
    return el

def get_label_from_node(node):
    label = search_a_label_node(node, None)
    label_text = render_output(label)
    remove_node_from_parent(label)
    return label_text