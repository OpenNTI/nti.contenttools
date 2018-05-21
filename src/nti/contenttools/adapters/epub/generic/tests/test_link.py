#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from lxml import html

from nti.contenttools.adapters.epub.generic.run import Run

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.tests import ContentToolsTestCase

class TestLinkAdapter(ContentToolsTestCase):

    def test_a_element(self):
        script = u"""<div><a href="url">link text</a></div>"""
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\href{url}{link text}'))

    def test_a_element_2(self):
        script = u"""<div><a href="https://nextthought.com/">NTI</a></div>"""
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\href{https://nextthought.com/}{NTI}'))