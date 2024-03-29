#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re

from six import string_types

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.interfaces import IRunNode

FORBIDDEN_CHARACTERS = r'[<>:"/\\\|\?\*\s\-,\t\'\!{}()]'


def create_label(name, value, label_tag_ignored=False):
    """
    create label based on the given name and value
    for example :
        name = "chapter"
        value = "Chapter review and summary"
        return \label{chapter:Chapter_review_and_summary}
    """
    if isinstance(value, string_types):
        value = re.sub(FORBIDDEN_CHARACTERS, '_', value)
    else:
        value = render_output(value)
        value = re.sub(FORBIDDEN_CHARACTERS, '_', value)
    value = value.replace(u'_textbf_', u'').replace(u'_textit_', u'')
    if label_tag_ignored:
        return u'%s:%s' % (name, value)
    return u'\\label{%s:%s}' % (name, value)


def search_run_node_and_remove_styles(root):
    if IRunNode.providedBy(root):
        root.styles = []
    if hasattr(root, u'children'):
        for node in root:
            search_run_node_and_remove_styles(node)


def search_node(provided, root):
    """
    traverse tree of nodes to look for a particular interface (provided)
    return true if there is node providing the given interface 'provided' 
    otherwise return false
    """
    if provided.providedBy(root):
        return True
    elif hasattr(root, u'children'):
        for node in root:
            found = search_node(provided, node)
            if found:
                return found
    return False


def search_and_update_node_property(provided, root, field):
    """
    traverse tree of nodes to look for a particular node given the interface (provided)
    if the node is found, update the value of the node's attribute 
    """
    if provided.providedBy(root):
        for name, value in field.items():
            if hasattr(root, name):
                setattr(root, name, value)
        return True
    elif hasattr(root, u'children'):
        for node in root:
            found = search_and_update_node_property(provided, node, field)
            if found:
                return found
    return False


def get_variant_field_string_value(field):
    """
    return string of a node field which type is Variant : String or Node
    """
    if isinstance(field, string_types):
        str_field = field
    else:
        str_field = render_output(field)
    return str_field
