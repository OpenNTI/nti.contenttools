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

from nti.contenttools.renderers.interfaces import IRenderContext

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.tests import ContentToolsTestCase


class TestModel(ContentToolsTestCase):

    def test_interface(self):
        context = DefaultRendererContext(name="LaTeX")
        assert_that(context, validly_provides(IRenderContext))
        assert_that(context, verifiably_provides(IRenderContext))

    def test_context(self):
        context = DefaultRendererContext(name="LaTeX")
        assert_that(context, has_property('name', is_("LaTeX")))
        context.write("ichigo")
        assert_that(context.read(), is_('ichigo'))
