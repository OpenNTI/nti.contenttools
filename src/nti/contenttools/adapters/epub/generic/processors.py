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

from nti.contenttools.adapters.epub.generic.lists import OrderedList
from nti.contenttools.adapters.epub.generic.lists import UnorderedList

from nti.contenttools.adapters.epub.generic.link import Hyperlink

from nti.contenttools.adapters.epub.generic.run import Run
from nti.contenttools.adapters.epub.generic.run import process_div_elements
from nti.contenttools.adapters.epub.generic.run import process_span_elements

from nti.contenttools.adapters.epub.generic.paragraph import Paragraph

from nti.contenttools.types import TextNode

@interface.implementer(IChildProcessor)
class _BoldChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Run.process(child, (u'bold',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _ItalicChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Run.process(child, (u'italic',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _UnderlineChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Run.process(child, (u'underline',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _StrongChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Run.process(child, (u'bold',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _StrikeChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Run.process(child, (u'strike',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _EmphasisChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Run.process(child, (u'italic',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _SubscriptChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Run.process(child, (u'sub',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _SuperscriptChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Run.process(child, (u'sup',), epub=epub)
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
class _HeadingOneChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, (u'Heading1',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _HeadingTwoChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, (u'Heading2',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _HeadingThreeChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, (u'Heading3',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _HeadingFourChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, (u'Heading4',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _HeadingFiveChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, (u'Heading5',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _HeadingSixChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, (u'Heading6',), epub=epub)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _HeadingSevenChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, (u'Heading7',), epub=epub)
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
class _NewlineChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = TextNode(u'\\newline\n')
        node.add_child(result)
        node.add_child(TextNode(child.tail))
        return result
