#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)


from nti.contenttools.types.interfaces import IRunNode
from nti.contenttools.types.interfaces import IHyperlink

from nti.contenttools.renderers.LaTeX.base import render_output


def search_run_node_with_element_type(root, element_type, nodes):
	if IRunNode.providedBy(root):
		if root.element_type == element_type:
			nodes.append(root)
		elif hasattr(root, 'children'):
			for child in root:
				search_run_node_with_element_type(child, element_type, nodes)
	elif hasattr(root, 'children'):
		for child in root:
			search_run_node_with_element_type(child, element_type, nodes)
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
					sup_nodes.append(root)
		elif hasattr(root, 'children'):
			for child in root:
				find_superscript_node(child, root_type, label_dict, label_ref_dict, sup_nodes)
	elif hasattr(root, 'children'):
		for child in root:
			find_superscript_node(child, root_type, label_dict, label_ref_dict, sup_nodes)
	return label_dict, label_ref_dict

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
