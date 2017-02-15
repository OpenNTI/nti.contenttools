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

from nti.contenttools.types.interfaces import IRow
from nti.contenttools.types.interfaces import ICell
from nti.contenttools.types.interfaces import ITBody
from nti.contenttools.types.interfaces import ITHead
from nti.contenttools.types.interfaces import ITFoot
from nti.contenttools.types.interfaces import ITable

from nti.contenttools.types.table import Row
from nti.contenttools.types.table import Cell
from nti.contenttools.types.table import TBody
from nti.contenttools.types.table import THead
from nti.contenttools.types.table import TFoot
from nti.contenttools.types.table import Table

from nti.contenttools.tests import ContentToolsTestCase


class TestTable(ContentToolsTestCase):

    def test_table(self):
        node = Table()
        assert_that(node, validly_provides(ITable))
        assert_that(node, verifiably_provides(ITable))
        assert_that(node, has_property('number_of_col_header', is_(0)))
        assert_that(node, has_property('number_of_col_body', is_(0)))
        assert_that(node, has_property('caption', is_(None)))
        assert_that(node, has_property('label', is_(None)))
        assert_that(node, has_property('border', is_(None)))
        assert_that(node, has_property('type', is_(None)))
        assert_that(node, has_property('alignment', is_(u'left')))

    def test_row(self):
        node = Row()
        assert_that(node, validly_provides(IRow))
        assert_that(node, verifiably_provides(IRow))
        assert_that(node, has_property('number_of_col', is_(0)))
        assert_that(node, has_property('border', is_(False)))
        assert_that(node, has_property('type', is_(None)))

    def test_cell(self):
        node = Cell()
        assert_that(node, validly_provides(ICell))
        assert_that(node, verifiably_provides(ICell))
        assert_that(node, has_property('border', is_(False)))
        assert_that(node, has_property('is_first_cell_in_the_row', is_(False)))
        assert_that(node, has_property('colspan', is_(1)))

    def test_table_body(self):
        node = TBody()
        assert_that(node, validly_provides(ITBody))
        assert_that(node, verifiably_provides(ITBody))
        assert_that(node, has_property('number_of_col', is_(0)))
        assert_that(node, has_property('border', is_(False)))

    def test_table_header(self):
        node = THead()
        assert_that(node, validly_provides(ITHead))
        assert_that(node, verifiably_provides(ITHead))
        assert_that(node, has_property('number_of_col', is_(0)))
        assert_that(node, has_property('border', is_(False)))

    def test_table_footer(self):
        node = TFoot()
        assert_that(node, validly_provides(ITFoot))
        assert_that(node, verifiably_provides(ITFoot))
        assert_that(node, has_property('number_of_col', is_(0)))
