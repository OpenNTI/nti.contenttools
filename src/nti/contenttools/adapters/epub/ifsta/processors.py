#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.adapters.epub.ifsta.interfaces import IChildProcessor

from nti.contenttools.adapters.epub.ifsta.paragraph import Paragraph


@interface.implementer(IChildProcessor)
class _ParagraphChildProcessor(object):

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, [], epub=epub)
        node.add_child(result)
        return result
