#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools.adapters.epub.generic import EPUBBody
from nti.contenttools.adapters.epub.generic import check_child
from nti.contenttools.adapters.epub.generic import check_element_tail
from nti.contenttools.adapters.epub.generic import check_element_text

from nti.contenttools.adapters.epub.prmia.finder import search_footnote_refs

def adapt(fragment, epub=None):
    body = fragment.find('body')
    epub_body = EPUBBody.process(body, epub)
    search_footnote_refs(epub_body, epub)   	
    return epub_body
