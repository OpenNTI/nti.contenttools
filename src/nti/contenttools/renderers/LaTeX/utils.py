#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re

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