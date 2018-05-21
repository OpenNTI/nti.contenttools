#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools import types

from nti.contenttools.adapters.epub.prmia import check_child
from nti.contenttools.adapters.epub.prmia import check_element_text
from nti.contenttools.adapters.epub.prmia import check_element_tail
from nti.contenttools.adapters.epub.generic.run import Run

from nti.contenttools.types import TextNode

def process_div_elements(element, parent, epub=None):
    el = Run.process(element, epub=epub)
    return el

def process_span_elements(element, epub=None):
    el = Run.process(element, epub=epub)
    return el