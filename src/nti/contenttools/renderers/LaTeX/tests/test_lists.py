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

from nti.contenttools.types.text import TextNode

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
        # todo : check with TextNode
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

    def test_unordered_list_without_item(self):
        node = UnorderedList()
        output = render_output(node)
        assert_that(output, is_(u'\\begin{itemize}\n\n\\end{itemize}\n'))

    def test_unordered_list(self):
        node = UnorderedList()
        child = Item()
        node.add(child)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{itemize}\n\item  \n\n\end{itemize}\n'))

    def test_ordered_list_without_item(self):
        node = OrderedList()
        output = render_output(node)
        assert_that(output, is_(u''))

    def test_ordered_list(self):
        node = OrderedList()
        child = Item()
        node.add(child)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{enumerate}[start=0]\n\item  \n\n\\end{enumerate}\n'))

    def test_item_with_description(self):
        node = ItemWithDesc()
        output = render_output(node)
        assert_that(output, is_(u''))

    def test_description_list(self):
        node = DescriptionList()
        output = render_output(node)
        assert_that(output,
                    is_('\\begin{description}\n\n\\end{description}\n'))

    def test_description_list_with_item_desc(self):
        node = DescriptionList()
        child = ItemWithDesc()
        dt = DT()
        dd = DD()
        dt.desc = dd
        child.add(dt)
        node.add(child)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{description}\n\item []  \n\n\\end{description}\n'))

    def test_description_list_with_dt(self):
        node = DescriptionList()
        dt = DT()
        dd = DD()
        dt.desc = dd
        node.add(dt)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{description}\n\item []  \n\n\\end{description}\n'))

    def test_dd_with_text(self):
        node = DD()
        run = Run()
        run.add(TextNode(u'dd'))
        node.add(run)
        output = render_output(node)
        assert_that(output, is_(u'dd'))

    def test_dt_with_desc_with_text(self):
        node = DT()
        run = Run()
        run.add(TextNode(u'term'))
        node.add(run)
        node.desc = Run()
        node.desc.add(TextNode(u'description'))
        output = render_output(node)
        assert_that(output, is_(u'\\item [term] description \n'))
    
    def test_unordered_list_with_text(self):
        node = UnorderedList()
        
        child_1 = Item()
        run_child_1 = Run()
        run_child_1.add(TextNode(u'bullet 1'))
        child_1.add(run_child_1)
        node.add(child_1)
        
        child_2 = Item()
        run_child_2 = Run()
        run_child_2.add(TextNode(u'bullet 2'))
        child_2.add(run_child_2)
        node.add(child_2)
        
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{itemize}\n\\item bullet 1 \n\\item bullet 2 \n\n\end{itemize}\n'))
    
    def test_ordered_list_with_text(self):
        node = OrderedList()
        
        child_1 = Item()
        run_child_1 = Run()
        run_child_1.add(TextNode(u'number 1'))
        child_1.add(run_child_1)
        node.add(child_1)
        
        child_2 = Item()
        run_child_2 = Run()
        run_child_2.add(TextNode(u'number 2'))
        child_2.add(run_child_2)
        node.add(child_2)
        
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{enumerate}[start=0]\n\\item number 1 \n\\item number 2 \n\n\end{enumerate}\n'))
