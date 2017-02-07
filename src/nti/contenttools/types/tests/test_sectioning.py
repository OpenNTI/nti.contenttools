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

from nti.contenttools.types.interfaces import IChapter
from nti.contenttools.types.interfaces import ISection

from nti.contenttools.types.sectioning import Chapter
from nti.contenttools.types.sectioning import Section

from nti.contenttools.tests import ContentToolsTestCase


class TestSectioning(ContentToolsTestCase):

    def test_interface(self):
        node = Chapter()
        assert_that(node, validly_provides(IChapter))
        assert_that(node, verifiably_provides(IChapter))
        
        node = Section()
        assert_that(node, validly_provides(ISection))
        assert_that(node, verifiably_provides(ISection))

    def test_title_label(self):
        node = Chapter()
        node.set_label("mylabel")
        node.set_title("mytitle")
        assert_that(node, has_property('label', is_('mylabel')))
        assert_that(node, has_property('title', is_('mytitle')))
