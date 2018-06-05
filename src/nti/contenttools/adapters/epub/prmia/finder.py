#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)


from nti.contenttools.types.interfaces import IRunNode

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
	children = []
	for child in parent.children:
		if child == node:
			parent.children.remove(child)