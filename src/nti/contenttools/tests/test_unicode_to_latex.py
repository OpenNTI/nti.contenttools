#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_entries

from nti.contenttools.unicode_to_latex import unicode_to_latex

from nti.contenttools.tests import ContentToolsTestCase


class TestUnicodeToLatex(ContentToolsTestCase):

    def test_mapping(self):
        mapping = unicode_to_latex()
        assert_that(mapping, has_length(2362))
        assert_that(mapping, 
                    has_entries("\u277b", "\\ding{187}",
                                "\u2926", "\\ElsevierGlyph{E20A}",
                                "\ud7c5", "\\mathsfbfsl{\\vartheta}",
                                "\u223a", "\\mathbin{{:}\\!\\!{-}\\!\\!{:}}",
                                "\u0337", "{\\fontencoding{LECO}\\selectfont\\char215}",
                                "\u0140", "{\\fontencoding{LELA}\\selectfont\\char202}"))
