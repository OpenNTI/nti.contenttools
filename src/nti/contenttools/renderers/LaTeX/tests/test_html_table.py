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

from nti.contenttools.types.text import TextNode

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
                    is_(u'\n\\begin{table}\n\\caption{Caption for table}\n\\label{table:label_table}\n\\begin{tabular}{}\n\n\\end{tabular}\n\\end{table}\n'))

    def test_html_table_row(self):
        node = Row()
        output = render_output(node)
        assert_that(output, is_(u'\\\\\n'))

    def test_html_table_row_with_one_cell(self):
        node = Row()
        cell = Cell()
        cell.add(TextNode(u'cell'))
        node.add(cell)
        output = render_output(node)
        assert_that(output, is_(u'cell\\\\\n'))

    def test_html_table_row_with_two_cell(self):
        node = Row()
        cell_1 = Cell()
        cell_2 = Cell()
        cell_1.add(TextNode(u'cell 1'))
        cell_2.add(TextNode(u'cell 2'))
        node.add(cell_1)
        node.add(cell_2)
        output = render_output(node)
        assert_that(output, is_(u'cell 1 & cell 2\\\\\n'))

    def test_html_table_empty_cell(self):
        node = Cell()
        output = render_output(node)
        assert_that(output, is_(u' ~ '))

    def test_html_table_cell(self):
        node = Cell()
        node.add(TextNode(u'cell'))
        output = render_output(node)
        assert_that(output, is_(u'cell'))

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

    def test_table_with_row_cell(self):
        table = Table()

        row_1 = Row()
        cell_1_1 = Cell()
        cell_1_1.add(TextNode(u'A'))
        cell_1_2 = Cell()
        cell_1_2.add(TextNode(u'B'))
        row_1.add(cell_1_1)
        row_1.add(cell_1_2)

        row_2 = Row()
        cell_2_1 = Cell()
        cell_2_1.add(TextNode(u'C'))
        cell_2_2 = Cell()
        cell_2_2.add(TextNode(u'D'))
        row_2.add(cell_2_1)
        row_2.add(cell_2_2)

        table.add(row_1)
        table.add(row_2)

        output = render_output(table)
        assert_that(output,
                    is_(u'\n\\begin{table}\n\\begin{tabular}{}\nA & B\\\\\nC & D\\\\\n\n\\end{tabular}\n\\end{table}\n'))

    def test_table_with_caption_row_cell(self):
        table = Table()
        table.caption = "Title"
        table.number_of_col_body = 2

        row_1 = Row()
        cell_1_1 = Cell()
        cell_1_1.add(TextNode(u'A'))
        cell_1_2 = Cell()
        cell_1_2.add(TextNode(u'B'))
        row_1.add(cell_1_1)
        row_1.add(cell_1_2)

        row_2 = Row()
        cell_2_1 = Cell()
        cell_2_1.add(TextNode(u'C'))
        cell_2_2 = Cell()
        cell_2_2.add(TextNode(u'D'))
        row_2.add(cell_2_1)
        row_2.add(cell_2_2)

        table.add(row_1)
        table.add(row_2)

        output = render_output(table)
        assert_that(output,
                    is_(u'\n\\begin{table}\n\\caption{Title}\n\\label{table:Title}\n\\begin{tabular}{ l  l }\nA & B\\\\\nC & D\\\\\n\n\\end{tabular}\n\\end{table}\n'))

    def test_table_with_caption_row_cell_border(self):
        table = Table()
        table.caption = "Title"
        table.number_of_col_body = 2
        table.border = True

        row_1 = Row()
        cell_1_1 = Cell()
        cell_1_1.add(TextNode(u'A'))
        cell_1_2 = Cell()
        cell_1_2.add(TextNode(u'B'))
        row_1.add(cell_1_1)
        row_1.add(cell_1_2)

        row_2 = Row()
        cell_2_1 = Cell()
        cell_2_1.add(TextNode(u'C'))
        cell_2_2 = Cell()
        cell_2_2.add(TextNode(u'D'))
        row_2.add(cell_2_1)
        row_2.add(cell_2_2)

        table.add(row_1)
        table.add(row_2)

        output = render_output(table)
        assert_that(output,
                    is_(u'\n\\begin{table}\n\\caption{Title}\n\\label{table:Title}\n\\begin{tabular}{|l|l|}\nA & B\\\\\nC & D\\\\\n\n\\end{tabular}\n\\end{table}\n'))
