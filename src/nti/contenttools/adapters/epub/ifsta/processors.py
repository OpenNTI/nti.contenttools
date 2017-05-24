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

from nti.contenttools.adapters.epub.ifsta.run import Run
from nti.contenttools.adapters.epub.ifsta.run import process_span_elements

from nti.contenttools.adapters.epub.ifsta.link import Hyperlink


@interface.implementer(IChildProcessor)
class _ParagraphChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, [], epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _BoldChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Run.process(child, (u'bold',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _SpanChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = process_span_elements(child, epub=epub)
        node.add_child(result)
        return result

@interface.implementer(IChildProcessor)
class _HyperlinkChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Hyperlink.process(child, epub=epub)
        node.add_child(result)
        return result
