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

from nti.contenttools.adapters.html.mathcounts.run import Run

from nti.contenttools.adapters.html.mathcounts.paragraph import Paragraph

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.tests import ContentToolsTestCase

class TestParagraphAdapter(ContentToolsTestCase):

    def test_simple_paragraph(self):
        script = u'<p>This is the first paragraph</p>'
        element = html.fromstring(script)
        node = Paragraph.process(element)
        output = render_output(node)

        assert_that(output,
                    is_(u'This is the first paragraph\n\n'))

    def test_paragraph(self):
        script = u'<div><p>This is the second paragraph</p></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)

        assert_that(output,
                    is_(u'This is the second paragraph\n\n'))