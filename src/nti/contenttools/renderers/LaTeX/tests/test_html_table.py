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

from nti.contenttools.types.table import Row
from nti.contenttools.types.table import Cell
from nti.contenttools.types.table import TBody
from nti.contenttools.types.table import THead
from nti.contenttools.types.table import TFoot
from nti.contenttools.types.table import Table

from nti.contenttools.tests import ContentToolsTestCase


class TestHTMLTable(ContentToolsTestCase):

    def test_html_table(self):
        node = Table()
        output = render_output(node)
        assert_that(output,
                    is_(u'\n\\begin{table}\n\\begin{tabular}{}\n\n\\end{tabular}\n\\end{table}\n'))
    
    def test_html_table_with_caption(self):
        node = Table()
        node.caption = "Caption for table"
        output = render_output(node)
        assert_that(output,
                    is_(u'\n\\begin{table}\n\\caption{Caption for table}\n\\label{table:Caption_for_table}\n\\begin{tabular}{}\n\n\\end{tabular}\n\\end{table}\n'))
    
    def test_html_table_with_caption_and_label(self):
        node = Table()
        node.caption = "Caption for table"
        node.label = "label_table"
        output = render_output(node)
        assert_that(output,
                    is_(u'\n\\begin{table}\n\\caption{Caption for table}\n\\label{label_table}\n\\begin{tabular}{}\n\n\\end{tabular}\n\\end{table}\n'))

    def test_html_table_row(self):
        node = Row()
        output = render_output(node)
        assert_that(output, is_(u'\\\\\n'))

    def test_html_table_cell(self):
        node = Cell()
        output = render_output(node)
        assert_that(output, is_(u' ~ '))

    def test_html_tbody(self):
        node = TBody()
        output = render_output(node)
        assert_that(output, is_(u'\hline\n'))

    def test_html_tfooter(self):
        node = TFoot()
        output = render_output(node)
        assert_that(output, is_(u''))

    def test_html_theader(self):
        node = THead()
        output = render_output(node)
        assert_that(output, is_(u''))
