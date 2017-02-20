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

from nti.contenttools.types.interfaces import IFootnote
from nti.contenttools.types.interfaces import IFootnoteText
from nti.contenttools.types.interfaces import IFootnoteMark

from nti.contenttools.types.footnote import Footnote
from nti.contenttools.types.footnote import FootnoteText
from nti.contenttools.types.footnote import FootnoteMark

from nti.contenttools.tests import ContentToolsTestCase


class TestFootnote(ContentToolsTestCase):

    def test_footnote(self):
        node = Footnote()
        assert_that(node, validly_provides(IFootnote))
        assert_that(node, verifiably_provides(IFootnote))
        assert_that(node, has_property('text', is_(None)))
        assert_that(node, has_property('label', is_(None)))

    def test_footnote_text(self):
        node = FootnoteText()
        assert_that(node, validly_provides(IFootnoteText))
        assert_that(node, verifiably_provides(IFootnoteText))
        assert_that(node, has_property('text', is_(None)))
        assert_that(node, has_property('label', is_(None)))
        assert_that(node, has_property('num', is_(None)))

    def test_footnote_mark(self):
        node = FootnoteMark()
        assert_that(node, validly_provides(IFootnoteMark))
        assert_that(node, verifiably_provides(IFootnoteMark))
        assert_that(node, has_property('text', is_(None)))
        assert_that(node, has_property('num', is_(None)))
