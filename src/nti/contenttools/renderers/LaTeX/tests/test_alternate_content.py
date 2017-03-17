#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.alternate_content import TextBoxContent
from nti.contenttools.types.alternate_content import AlternateContent

from nti.contenttools.types.run import Run
from nti.contenttools.types.text import TextNode

from nti.contenttools.tests import ContentToolsTestCase


class TestAlternateContent(ContentToolsTestCase):

    def test_alternate_content(self):
        node = AlternateContent()
        run = Run()
        run.add(TextNode(u'This is an alternate content'))
        node.add(run)
        output = render_output(node)
        assert_that(output, is_(u'This is an alternate content'))

    def test_text_box_content(self):
        node = TextBoxContent()
        run = Run()
        run.add(TextNode(u'This is a text box'))
        node.add(run)
        output = render_output(node)
        assert_that(output, u'\\parbox[c]{\\textwidth}{This is a text box}')
