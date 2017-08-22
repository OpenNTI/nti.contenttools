#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: processors.py 116254 2017-06-29 13:38:07Z carlos.sanchez $
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.adapters.html.mathcounts.interfaces import IChildProcessor

from nti.contenttools.adapters.html.mathcounts.paragraph import Paragraph

from nti.contenttools.adapters.html.mathcounts.run import Run

from nti.contenttools.types import TextNode


@interface.implementer(IChildProcessor)
class _ParagraphChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, html=None):
        result = Paragraph.process(child, [], html=html)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _BoldChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, html=None):
        result = Run.process(child, (u'bold',), html=html)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _ItalicChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, html=None):
        result = Run.process(child, (u'italic',), html=html)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _UnderlineChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, html=None):
        result = Run.process(child, (u'underline',), html=html)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _StrongChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, html=None):
        result = Run.process(child, (u'bold',), html=html)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _StrikeChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, html=None):
        result = Run.process(child, (u'strike',), html=html)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _EmphasisChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, html=None):
        result = Run.process(child, (u'italic',), html=html)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _SubscriptChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, html=None):
        result = Run.process(child, (u'sub',), html=html)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _SuperscriptChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, html=None):
        result = Run.process(child, (u'sup',), html=html)
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _DivChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, html=None):
        result = Run.process(child, html=html)
        node.add_child(result)
        return result

@interface.implementer(IChildProcessor)
class _SpanChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, hmtl=None):
        result = Run.process(child, html=html)
        node.add_child(result)
        return result

@interface.implementer(IChildProcessor)
class _NewlineChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, hmtl=None):
        result = TextNode(u'\\newline\n')
        node.add_child(result)
        node.add_child(TextNode(child.tail))
        return result