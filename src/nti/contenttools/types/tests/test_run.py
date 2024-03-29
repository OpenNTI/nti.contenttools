#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import IRunNode

from nti.contenttools.types.run import Run

from nti.contenttools.tests import ContentToolsTestCase


class TestNode(ContentToolsTestCase):

    def test_node(self):
        node = Run()
        assert_that(node, validly_provides(IRunNode))
        assert_that(node, verifiably_provides(IRunNode))
