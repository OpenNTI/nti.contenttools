#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904
from hamcrest import is_
from hamcrest import assert_that
from hamcrest import has_property

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import IDocxTable
from nti.contenttools.types.interfaces import IDocxTRow
from nti.contenttools.types.interfaces import IDocxTCell

from nti.contenttools.types.docx_table import DocxTable
from nti.contenttools.types.docx_table import DocxTRow
from nti.contenttools.types.docx_table import DocxTCell

from nti.contenttools.tests import ContentToolsTestCase


class TestDocxTable(ContentToolsTestCase):

    def test_docx_table(self):
        node = DocxTable()
        assert_that(node, validly_provides(IDocxTable))
        assert_that(node, verifiably_provides(IDocxTable))
        assert_that(node, has_property('borders', is_(None)))
        assert_that(node, has_property('grid', is_(None)))

    def test_docx_trow(self):
        node = DocxTRow()
        assert_that(node, validly_provides(IDocxTRow))
        assert_that(node, verifiably_provides(IDocxTRow))

    def test_docx_tcell(self):
        node = DocxTCell()
        assert_that(node, validly_provides(IDocxTCell))
        assert_that(node, verifiably_provides(IDocxTCell))
