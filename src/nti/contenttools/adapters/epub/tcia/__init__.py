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

from nti.contenttools.adapters.epub.tcia.finder import search_image_thubms_up_down

def adapt(fragment, epub=None):
    body = fragment.find('body')
    epub_body = EPUBBody.process(body, epub)
    search_image_thubms_up_down(epub_body)
    return epub_body
