#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from nti.contenttools.renderers.LaTeX.utils import search_node
from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value

from nti.contenttools.types.document import Document

from nti.contenttools.types.interfaces import IItem

from nti.contenttools.types.lists import Item
from nti.contenttools.types.lists import OrderedList

from nti.contenttools.types.media import Figure
from nti.contenttools.types.run import Run
from nti.contenttools.types.text import TextNode

from nti.contenttools.types.sectioning import Section

from nti.contenttools.tests import ContentToolsTestCase


class TestUtils(ContentToolsTestCase):

    def test_search_node_true(self):
        root = Document()
        section_1 = Section()
        section_2 = Section()
        list_1 = OrderedList()
        item_1 = Item()
        item_2 = Item()
        list_1.add(item_1)
        list_1.add(item_2)
        section_2.add(list_1)
        root.add(section_1)
        root.add(section_2)
        result = search_node(IItem, root)
        assert_that(result, is_(True))

    def test_search_node_false(self):
        root = Document()
        section_1 = Section()
        section_2 = Section()
        list_1 = OrderedList()
        section_2.add(list_1)
        root.add(section_1)
        root.add(section_2)
        result = search_node(IItem, root)
        assert_that(result, is_(False))

    def test_get_variant_field_string_value(self):
        node = Figure()

        node.caption = u'This is a figure caption'
        caption = get_variant_field_string_value(node.caption)
        assert_that(caption, is_(u'This is a figure caption'))

        node.title = TextNode(u'This is a figure title')
        title = get_variant_field_string_value(node.title)
        assert_that(title, is_(u'This is a figure title'))

        node.label = Run()
        child = TextNode(u'This is a figure label')
        node.label.add(child)
        label = get_variant_field_string_value(node.label)
        assert_that(label, is_(u'This is a figure label'))
