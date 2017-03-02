#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
from StdSuites.AppleScript_Suite import string
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re
from six import string_types
from nti.contenttools.renderers.LaTeX.base import render_output

FORBIDDEN_CHARACTERS = r'[<>:"/\\\|\?\*\s\-,\t\'\!]'


def create_label(name, value):
    """
    create label based on the given name and value
    for example :
        name = "chapter"
        value = "Chapter review and summary"
        return \label{chapter:Chapter_review_and_summary}
    """
    value = re.sub(FORBIDDEN_CHARACTERS, '_', value)
    return u'\\label{%s:%s}' % (name, value)


def search_node(provided, root):
    """
    traverse nodes under the root
    return true if there is node providing the given interface 'provided' 
    otherwise return false
    """
    found = False
    for node in root:
        if provided.providedBy(node):
            return True
        else:
            found = search_node(provided, node)
    return found

def get_variant_field_string_value(field):
    """
    return string a node field which type is Variant : String or Node
    """
    if isinstance(field, string_types):
        str_field = field
    else:
        str_field = render_output(field)
    return str_field
    
