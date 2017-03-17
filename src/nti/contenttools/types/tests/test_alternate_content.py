#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import IAlternateContent
from nti.contenttools.types.interfaces import ITextBoxContent

from nti.contenttools.types.alternate_content import AlternateContent
from nti.contenttools.types.alternate_content import TextBoxContent

from nti.contenttools.tests import ContentToolsTestCase


class TestAlternateContent(ContentToolsTestCase):

    def test_alternate_content(self):
        node = AlternateContent()
        assert_that(node, validly_provides(IAlternateContent))
        assert_that(node, verifiably_provides(IAlternateContent))

    def test_text_box_content(self):
        node = TextBoxContent()
        assert_that(node, validly_provides(ITextBoxContent))
        assert_that(node, verifiably_provides(ITextBoxContent))
