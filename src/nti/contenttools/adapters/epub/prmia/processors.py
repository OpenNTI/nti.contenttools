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

from nti.contenttools.adapters.epub.prmia.media import Image

from nti.contenttools.adapters.epub.prmia.paragraph import Paragraph

from nti.contenttools.adapters.epub.prmia.run import process_div_elements
from nti.contenttools.adapters.epub.prmia.run import process_span_elements

from nti.contenttools.adapters.epub.prmia.link import Hyperlink

from nti.contenttools import types

from nti.contenttools.types import TextNode

from nti.contenttools.renderers.LaTeX.utils import create_label

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
class _DivChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = process_div_elements(child, node, epub=epub)
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
        result.label = generate_section_label(result, 'chapter')
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _HeadingTwoChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, (u'Heading2',), epub=epub)
        result.label = generate_section_label(result, 'section')
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _HeadingThreeChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, (u'Heading3',), epub=epub)
        result.label = generate_section_label(result, 'subsection')
        node.add_child(result)
        return result


@interface.implementer(IChildProcessor)
class _HeadingFourChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = Paragraph.process(child, (u'Heading4',), epub=epub)
        result.label = generate_section_label(result, 'subsubsection')
        node.add_child(result)
        return result


def generate_section_label(section_node, section_type):
    label = types.Run()
    label.children = section_node.children
    label = TextNode(create_label(section_type, label))
    return label

