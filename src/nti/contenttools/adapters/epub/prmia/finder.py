#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six

text_type = six.text_type

from nti.contenttools.types.interfaces import IRunNode
from nti.contenttools.types.interfaces import IImage
from nti.contenttools.types.interfaces import IHyperlink
from nti.contenttools.types.interfaces import ISection
from nti.contenttools.types.interfaces import IChapter
from nti.contenttools.types.interfaces import IRealPageNumber

from nti.contenttools.renderers.LaTeX.base import render_output
from nti.contenttools.renderers.LaTeX.base import render_children_output

def search_run_node_with_element_type(root, element_type, nodes, option=None):
	if IRunNode.providedBy(root):
		if root.element_type == element_type:
			if element_type == 'Figure Image' and option:
				for child in root:
					if IImage.providedBy(child):
						child.inline_image = True
			nodes.append(root)
		elif hasattr(root, 'children'):
			for child in root:
				search_run_node_with_element_type(child, element_type, nodes, option)
	elif hasattr(root, 'children'):
		for child in root:
			search_run_node_with_element_type(child, element_type, nodes, option)
	return nodes


def search_label_node_in_list(nodes, label):
	for item in nodes:
		if IRunNode.providedBy(item):
			if item.element_type == 'Label':
				label = item
				nodes.remove(item)
	return label

def remove_node_from_parent(node):
	parent = node.__parent__
	for child in parent.children:
		if child == node:
			parent.children.remove(child)

				
def find_superscript_node(root, root_type, label_dict, label_ref_dict, sup_nodes):
	if IRunNode.providedBy(root):
		if root.element_type == 'Superscript':
			sup_type = u'%s_Superscript' %(root_type) 
			find_label_node(root, sup_type, label_dict)
			ref_label_node = []
			find_ref_node(root, ref_label_node)
			if label_dict and ref_label_node:
				if len(label_dict) == len(ref_label_node):
					for i, key in enumerate(label_dict):
						label_ref_dict[label_dict[key]] = ref_label_node[i]
						sup_nodes[label_dict[key]] = root
		elif hasattr(root, 'children'):
			for child in root:
				find_superscript_node(child, root_type, label_dict, label_ref_dict, sup_nodes)
	elif hasattr(root, 'children'):
		for child in root:
			find_superscript_node(child, root_type, label_dict, label_ref_dict, sup_nodes)
	return label_dict, label_ref_dict, sup_nodes

def find_label_node(node, parent_type, label_dict):
	if IRunNode.providedBy(node):
		if node.element_type == 'Label':
			label_dict[parent_type] = render_output(node)
		elif hasattr(node, 'children'):
			for child in node:
				find_label_node(child, parent_type, label_dict)
	elif hasattr(node, 'children'):
		for child in node:
			find_label_node(child, parent_type, label_dict)
	return label_dict

def find_label_node_to_cleanup(node, label_dict):
	if IRunNode.providedBy(node):
		if node.element_type == 'Label':
			label_dict[render_output(node)] = node
		elif hasattr(node, 'children'):
			for child in node:
				find_label_node_to_cleanup(child, label_dict)
	elif hasattr(node, 'children'):
		for child in node:
			find_label_node_to_cleanup(child, label_dict)
	return label_dict

def cleanup_label_node(node, epub):
	label_dict = {}
	find_label_node_to_cleanup(node, label_dict)
	temp = list(epub.label_refs.keys())
	for label in label_dict:
		if label not in temp:
			lnode = label_dict[label]
			parent = lnode.__parent__
			parent.remove(lnode)

def find_ref_node(node, ref_label_node):
	if IHyperlink.providedBy(node):
		target = node.target
		if '#' in target:
			label_ref_idx = target.find('#') + 1
			node.target = target[label_ref_idx:]
			ref_label_node.append(node.target)
	elif hasattr(node, 'children'):
		for child in node:
			find_ref_node(child, ref_label_node)
	return ref_label_node

def search_footnote_refs(root, epub):
	label_dict = {}
	label_ref_dict = {}
	sup_nodes = {}
	find_superscript_node(root, 'Refs', label_dict, label_ref_dict, sup_nodes)
	for item in sup_nodes.keys():
		id_ref = label_ref_dict[item]
		if id_ref in epub.footnote_ids.keys():
			node = sup_nodes[item]
			parent = node.__parent__
			footnote_node = epub.footnote_ids[id_ref]
			for i, child in enumerate(parent):
				if child == node:
					parent.children.remove(child)
					parent.children.insert(i, footnote_node)
	return label_dict, label_ref_dict, sup_nodes

def search_href_node(node, epub):
	if IHyperlink.providedBy(node):
		target = node.target
		if '#' in target:
			label_ref_idx = target.find('#') + 1
			node.target = target[label_ref_idx:]
			if node.target in epub.labels.keys():
				node.type = 'ntiidref'
		elif node.target in epub.labels.keys():
			node.type = 'ntiidref'

	elif hasattr(node, 'children'):
		for child in node:
			search_href_node(child, epub)

def find_href_node_index(node, targets):
	if IHyperlink.providedBy(node):
		if '#' in node.target:
			label_ref_idx = node.target.find('#') + 1
			target = node.target[label_ref_idx:]
			target = target.replace('page_', '')
			targets.append((target, node))
			parent = node.__parent__
			parent.children = ()
	elif hasattr(node, 'children'):
		for child in node:
			find_href_node_index(child, targets)
	return targets

def search_a_label_node(node, label):
	if IRunNode.providedBy(node):
		if node.element_type == 'Label':
			label = node
		elif hasattr(node, 'children'):
			for child in node:
				label = search_a_label_node(child, label)
				if label:
					return label
	elif hasattr(node, 'children'):
		for child in node:
			label = search_a_label_node(child, label)
			if label:
				return label
	return label

def search_sections_of_real_page_number(root, sections, page_numbers):
	if ISection.providedBy(root) or IChapter.providedBy(root):
		sections.append(root)
	elif IRealPageNumber.providedBy(root):
		if sections:
			last_section = sections[-1]
			if isinstance(last_section.label, text_type):
				page_numbers[render_children_output(root)] = last_section.label
			else:
				page_numbers[render_children_output(root)] = render_output(last_section.label)
	elif hasattr(root, 'children'):
		for child in root:
			search_sections_of_real_page_number(child, sections, page_numbers)
	return sections, page_numbers