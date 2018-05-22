#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml.html import HtmlComment

from zope import component

from nti.contenttools import types

from nti.contenttools._compat import text_

from nti.contenttools.adapters.epub.generic import EPUBBody
from nti.contenttools.adapters.epub.generic import check_child
from nti.contenttools.adapters.epub.generic import check_element_tail
from nti.contenttools.adapters.epub.generic import check_element_text

from nti.contenttools.adapters.epub.interfaces import IChildProcessor

from nti.contenttools.types import TextNode

from nti.contenttools.adapters.epub.tcia.finder import search_image_thubms_up_down

def adapt(fragment, epub=None):
    body = fragment.find('body')
    epub_body = EPUBBody.process(body, epub)
    search_image_thubms_up_down(epub_body)
    return epub_body
