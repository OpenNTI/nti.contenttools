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