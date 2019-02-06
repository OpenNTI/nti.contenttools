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

from nti.contenttools.adapters.epub.ifsta.lists import OrderedList
from nti.contenttools.adapters.epub.ifsta.lists import UnorderedList

from nti.contenttools.adapters.epub.ifsta.media import Image
from nti.contenttools.adapters.epub.ifsta.media import Figure

from nti.contenttools.adapters.epub.ifsta.link import Hyperlink

from nti.contenttools.adapters.epub.ifsta.paragraph import Paragraph

from nti.contenttools.adapters.epub.ifsta.run import Run
from nti.contenttools.adapters.epub.ifsta.run import process_div_elements
from nti.contenttools.adapters.epub.ifsta.run import process_span_elements

from nti.contenttools.adapters.epub.ifsta.table import Table

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
class _HyperlinkChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Hyperlink.process(child, epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _DivChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = process_div_elements(child, node, epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _OrderedListChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = OrderedList.process(child, epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _UnorderedListChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = UnorderedList.process(child, epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _TableChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Table.process(child, epub=epub)
        node.add_child(result)
        node.add_child(TextNode(u'\\\\'))
        node.add_child(TextNode(u'\n'))
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


@interface.implementer(IChildProcessor)
class _BrChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Run()
        node.add_child(result)
        return result
