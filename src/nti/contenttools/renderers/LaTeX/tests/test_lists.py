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

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.lists import DD
from nti.contenttools.types.lists import DT
from nti.contenttools.types.lists import Item
from nti.contenttools.types.lists import List
from nti.contenttools.types.lists import ItemWithDesc
from nti.contenttools.types.lists import OrderedList
from nti.contenttools.types.lists import UnorderedList
from nti.contenttools.types.lists import DescriptionList

from nti.contenttools.types.run import Run

from nti.contenttools.tests import ContentToolsTestCase

class TestLists(ContentToolsTestCase):

    def test_dd(self):
        node = DD()
        output = render_output(node)
        assert_that(output, is_(u''))

    def test_dt(self):
        node = DT()
        output = render_output(node)
        assert_that(output, is_(u'\\item []  \n'))
    
    def test_dt_with_desc(self):
        node = DT()
        node.desc = Run()
        output = render_output(node)
        assert_that(output, is_(u'\\item []  \n'))

    def test_item(self):
        node = Item()
        output = render_output(node)
        assert_that(output, is_(u'\\item  \n'))

    def test_list(self):
        node = List()
        output = render_output(node)
        assert_that(output, is_(u'\\begin{itemize}\n\n\\end{itemize}\n'))

    def test_unordered_list(self):
        node = UnorderedList()
        output = render_output(node)
        assert_that(output, is_(u'\\begin{itemize}\n\n\\end{itemize}\n'))

    def test_ordered_list_without_item(self):
        node = OrderedList()
        output = render_output(node)
        assert_that(output, is_(u''))

    def test_ordered_list(self):
        node = OrderedList()
        child = Item()
        node.add(child)
        output = render_output(node)
        assert_that(
            output,
            is_(u'\\begin{enumerate}[start=0]\n\item  \n\n\\end{enumerate}\n'))

    def test_item_with_description(self):
        node = ItemWithDesc()
        output = render_output(node)
        assert_that(output, is_(u''))

    def test_description_list(self):
        node = DescriptionList()
        output = render_output(node)
        assert_that(output, is_('\\begin{description}\n\n\\end{description}\n'))