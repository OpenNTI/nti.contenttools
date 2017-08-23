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

from nti.contenttools.adapters.html.mathcounts.parser import MathcountsHTMLParser

from nti.contenttools.tests import ContentToolsTestCase


class TestMathcountsHTMLParser(ContentToolsTestCase):

    def test_symmath(self):
        script = u'<html><body><div><p class="Normal ParaOverride-4"><span class="CharOverride-5">1.  </span><span class="CharOverride-6">In a standard deck of 52 playing cards, the red number cards greater than 6 are the 7, 8, 9 and 10 in the suits of diamonds and hearts. That’s a total of 8 cards. The percent probability that Perta randomly selects one of these 8 cards, then, is 8/52 </span><span class="CharOverride-7">≈</span><span class="CharOverride-6"> </span><span class="CharOverride-5">15.38</span><span class="CharOverride-6">%.</span></p></div></body></html>'
        _ = html.fromstring(script)
        parser = MathcountsHTMLParser(script, 'output_dir', 'test.tex')
        parser.process()
        assert_that(parser.context.read(),
                    is_("\\begin{document}\n\\begin{naquestion}[individual=true]\n\\label{naqsymmath:test_1}\\begin{naqsymmathpart}\n1. In a standard deck of 52 playing cards, the red number cards greater than 6 are the 7, 8, 9 and 10 in the suits of diamonds and hearts. That's a total of 8 cards. The percent probability that Perta randomly selects one of these 8 cards, then, is 8/52 $\\approx$ 15.38\\%.\n\n\n\\begin{naqsolutions}\n\n\\end{naqsolutions}\n\n\\begin{naqsolexplanation}\n\n\\end{naqsolexplanation}\n\n\n\\end{naqsymmathpart}\n\n\\end{naquestion}\n\n\\end{document}\n"))
