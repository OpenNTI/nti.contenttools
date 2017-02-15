#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_property
does_not = is_not

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import IDD
from nti.contenttools.types.interfaces import IDT
from nti.contenttools.types.interfaces import IItem
from nti.contenttools.types.interfaces import IList
from nti.contenttools.types.interfaces import IOrderedList
from nti.contenttools.types.interfaces import IItemWithDesc
from nti.contenttools.types.interfaces import IUnorderedList
from nti.contenttools.types.interfaces import IDescriptionList

from nti.contenttools.types.lists import DD
from nti.contenttools.types.lists import DT
from nti.contenttools.types.lists import Item
from nti.contenttools.types.lists import List
from nti.contenttools.types.lists import ItemWithDesc
from nti.contenttools.types.lists import OrderedList
from nti.contenttools.types.lists import UnorderedList
from nti.contenttools.types.lists import DescriptionList

from nti.contenttools.tests import ContentToolsTestCase


class TestLists(ContentToolsTestCase):

    def test_list(self):
        node = List()
        assert_that(node, validly_provides(IList))
        assert_that(node, verifiably_provides(IList))
        assert_that(node, has_property('group', is_(u'')))
        assert_that(node, has_property('format', is_(u'')))
        assert_that(node, has_property('level', is_(u'')))
        assert_that(node, has_property('start', is_(0)))

    def test_unordered_list(self):
        node = UnorderedList()
        assert_that(node, validly_provides(IUnorderedList))
        assert_that(node, verifiably_provides(IUnorderedList))
        assert_that(node, has_property('group', is_(u'')))
        assert_that(node, has_property('format', is_(u'')))
        assert_that(node, has_property('level', is_(u'')))
        assert_that(node, has_property('start', is_(0)))

    def test_ordered_list(self):
        node = OrderedList()
        assert_that(node, validly_provides(IOrderedList))
        assert_that(node, verifiably_provides(IOrderedList))
        assert_that(node, has_property('group', is_(u'')))
        assert_that(node, has_property('format', is_(u'')))
        assert_that(node, has_property('level', is_(u'')))
        assert_that(node, has_property('start', is_(0)))

    def test_item(self):
        node = Item()
        assert_that(node, validly_provides(IItem))
        assert_that(node, verifiably_provides(IItem))

    def test_description_list(self):
        node = DescriptionList()
        assert_that(node, validly_provides(IDescriptionList))
        assert_that(node, verifiably_provides(IDescriptionList))

    def test_item_with_desc(self):
        node = ItemWithDesc()
        assert_that(node, validly_provides(IItemWithDesc))
        assert_that(node, verifiably_provides(IItemWithDesc))

    def test_dt(self):
        node = DT()
        assert_that(node, validly_provides(IDT))
        assert_that(node, verifiably_provides(IDT))
        assert_that(node, has_property('desc', is_(None)))
        assert_that(node, has_property('type', is_(None)))

    def test_dd(self):
        node = DD()
        assert_that(node, validly_provides(IDD))
        assert_that(node, verifiably_provides(IDD))
