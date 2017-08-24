#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
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
                    is_('This is the first paragraph\n\n'))

    def test_paragraph(self):
        script = u'<div><p>This is the second paragraph</p></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)

        assert_that(output,
                    is_('This is the second paragraph\n\n'))

    def test_paragraph_2(self):
        script = u'<div><p class="Normal ParaOverride-4"><span class="CharOverride-5">1.  </span><span class="CharOverride-6">In a standard deck of 52 playing cards, the red number cards greater than 6 are the 7, 8, 9 and 10 in the suits of diamonds and hearts. That’s a total of 8 cards. The percent probability that Perta randomly selects one of these 8 cards, then, is 8/52 </span><span class="CharOverride-7">≈</span><span class="CharOverride-6"> </span><span class="CharOverride-5">15.38</span><span class="CharOverride-6">%.</span></p></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)

        assert_that(output,
                    is_("1. In a standard deck of 52 playing cards, the red number cards greater than 6 are the 7, 8, 9 and 10 in the suits of diamonds and hearts. That's a total of 8 cards. The percent probability that Perta randomly selects one of these 8 cards, then, is 8/52 $\\approx$ 15.38\\%.\n\n"))