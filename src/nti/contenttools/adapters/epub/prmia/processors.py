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
from nti.contenttools.adapters.epub.prmia.run import process_sup_elements
from nti.contenttools.adapters.epub.prmia.run import process_span_elements

from nti.contenttools.adapters.epub.prmia.link import Hyperlink

from nti.contenttools import types

from nti.contenttools.types import TextNode

from nti.contenttools.renderers.LaTeX.utils import create_label

from nti.contenttools.adapters.epub.generic.run import Run

from nti.contenttools.adapters.epub.prmia.finder import search_real_page_number_in_title

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
class _SuperscriptChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = process_sup_elements(child, node, epub=epub)
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
        result = types.Chapter()
        el = Run.process(child, epub=epub)
        result.title = el
        set_heading_label(child, result, 'chapter', epub)
        node.add_child(result)
        if epub:
            search_real_page_number_in_title(el, result.label, epub.page_numbers)
        return result


@interface.implementer(IChildProcessor)
class _HeadingTwoChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = types.Section()
        el = Run.process(child, epub=epub)
        result.title = el
        set_heading_label(child, result, 'section', epub)
        node.add_child(result)
        if epub:
            search_real_page_number_in_title(el, result.label, epub.page_numbers)
        return result


@interface.implementer(IChildProcessor)
class _HeadingThreeChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = types.SubSection()
        el = Run.process(child, epub=epub)
        result.title = el
        set_heading_label(child, result, 'subsection',epub)
        node.add_child(result)
        if epub:
            search_real_page_number_in_title(el, result.label, epub.page_numbers)
        return result


@interface.implementer(IChildProcessor)
class _HeadingFourChildProcessor(object):

    __slots__ = ()

    def process(self, child, node, element, epub=None):
        result = types.SubSubSection()
        el = Run.process(child, epub=epub)
        result.title = el
        set_heading_label(child, result, 'subsubsection', epub)
        node.add_child(result)
        if epub:
            search_real_page_number_in_title(el, result.label, epub.page_numbers)
        return result

def set_heading_label(element, header_node, section_type, epub):
    attrib = element.attrib
    if 'id' in attrib:
        header_node.label = TextNode(attrib['id'])
        epub.labels[attrib['id']] = section_type
    else:
        header_node.label = generate_section_label(header_node.title, section_type)

def generate_section_label(section_node, section_type):
    label = types.Run()
    label.children = section_node.children
    label = TextNode(create_label(section_type, label, label_tag_ignored=True))
    return label

