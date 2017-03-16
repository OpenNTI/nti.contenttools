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

from nti.contenttools.types.interfaces import IHyperlink
from nti.contenttools.types.link import Hyperlink

from nti.contenttools.tests import ContentToolsTestCase


class TestLink(ContentToolsTestCase):

    def test_hyperlink(self):
        node = Hyperlink()
        assert_that(node, validly_provides(IHyperlink))
        assert_that(node, verifiably_provides(IHyperlink))
        assert_that(node, has_property('target', is_(None)))
        assert_that(node, has_property('type', is_(u'Normal')))
