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

from nti.contenttools.types.document import Document

from nti.contenttools.types.interfaces import IItem

from nti.contenttools.types.lists import Item
from nti.contenttools.types.lists import OrderedList

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
