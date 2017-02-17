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

from nti.contenttools.types.interfaces import IGlossary
from nti.contenttools.types.interfaces import IGlossaryList
from nti.contenttools.types.interfaces import IGlossaryItem
from nti.contenttools.types.interfaces import IGlossaryDT
from nti.contenttools.types.interfaces import IGlossaryDD
from nti.contenttools.types.interfaces import IGlossaryTerm

from nti.contenttools.types.glossary import Glossary
from nti.contenttools.types.glossary import GlossaryList
from nti.contenttools.types.glossary import GlossaryItem
from nti.contenttools.types.glossary import GlossaryDT
from nti.contenttools.types.glossary import GlossaryDD
from nti.contenttools.types.glossary import GlossaryTerm

from nti.contenttools.tests import ContentToolsTestCase


class TestGlossary(ContentToolsTestCase):

    def test_glossary(self):
        node = Glossary()
        assert_that(node, validly_provides(IGlossary))
        assert_that(node, verifiably_provides(IGlossary))

    def test_glossary_list(self):
        node = GlossaryList()
        assert_that(node, validly_provides(IGlossaryList))
        assert_that(node, verifiably_provides(IGlossaryList))

    def test_glossary_item(self):
        node = GlossaryItem()
        assert_that(node, validly_provides(IGlossaryItem))
        assert_that(node, verifiably_provides(IGlossaryItem))

    def test_glossary_dd(self):
        node = GlossaryDD()
        assert_that(node, validly_provides(IGlossaryDD))
        assert_that(node, verifiably_provides(IGlossaryDD))

    def test_glossary_dt(self):
        node = GlossaryDT()
        assert_that(node, validly_provides(IGlossaryDT))
        assert_that(node, verifiably_provides(IGlossaryDT))

    def test_glossary_term(self):
        node = GlossaryTerm()
        assert_that(node, validly_provides(IGlossaryTerm))
        assert_that(node, verifiably_provides(IGlossaryTerm))
