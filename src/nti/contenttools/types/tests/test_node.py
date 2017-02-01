#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property
does_not = is_not

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import INode

from nti.contenttools.types.node import Node

from nti.contenttools.tests import ContentToolsTestCase


class TestNode(ContentToolsTestCase):

    def test_interface(self):
        node = Node()
        assert_that(node, validly_provides(INode))
        assert_that(node, verifiably_provides(INode))

    def test_children(self):
        parent = Node()
        child = Node()
        parent.add(child)
        assert_that(parent, has_property('children', has_length(1)))
        assert_that(list(parent), has_length(1))
        assert_that(child, has_property('__parent__', is_(parent)))
        parent.remove(child)
        assert_that(list(parent), has_length(0))
        assert_that(child, has_property('__parent__', is_(none())))
        with self.assertRaises(ValueError):
            parent.remove(child)
