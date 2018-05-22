#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.adapters.epub.interfaces import IChildProcessor

from nti.contenttools.adapters.epub.tcia.lists import OrderedList
from nti.contenttools.adapters.epub.tcia.lists import UnorderedList

from nti.contenttools.adapters.epub.tcia.media import Image
from nti.contenttools.adapters.epub.tcia.media import Figure

from nti.contenttools.adapters.epub.tcia.link import Hyperlink

from nti.contenttools.adapters.epub.tcia.paragraph import Paragraph

from nti.contenttools.adapters.epub.tcia.run import Run
from nti.contenttools.adapters.epub.tcia.run import process_span_elements


from nti.contenttools.types import TextNode


@interface.implementer(IChildProcessor)
class _ParagraphChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, [], epub=epub)
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
class _ImageChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Image.process(child, epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _FigureChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Figure.process(child, epub=epub)
        node.add_child(result)
        return result