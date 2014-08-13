#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

from nti.contentfragments.latex import PlainTextToLatexFragmentConverter

from nti.contenttools.tests import ContentToolsTestCase

class TestExtendedEscapeList(ContentToolsTestCase):
    
    def test_extended_escape_chars(self):
        plain_text = u"hello from plain µ"
        latex_tex  = u"hello from plain $\\mu$"
        result_tex = PlainTextToLatexFragmentConverter(plain_text, text_scaper='extended')
        assert_that(latex_tex, is_(result_tex))

        plain_text = u"check arrow ↑"
        latex_tex  = u"check arrow $\\uparrow$"
        result_tex = PlainTextToLatexFragmentConverter(plain_text, text_scaper='extended')
        assert_that(latex_tex, is_(result_tex))

        plain_text = u"hello from plain δ Τ"
        latex_tex  = u"hello from plain $\\delta$ $\\Tau$"
        result_tex = PlainTextToLatexFragmentConverter(plain_text, text_scaper='extended')
        assert_that(latex_tex, is_(result_tex))

