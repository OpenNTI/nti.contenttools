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

from nti.contenttools.adapters.epub.ifsta.paragraph import Paragraph

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

    def test_simple_paragraph_2(self):
        script = u'<p>This is the first paragraph</p><p>This is the second paragraph</p>'

        element = html.fromstring(script)
        node = Paragraph.process(element)
        output = render_output(node)

        assert_that(output,
                    is_(u'This is the first paragraph\n\nThis is the second paragraph\n\n\n\n'))

    def test_paragraph(self):
        script = u'<p class="Body-Text ParaOverride-1"><span id="_idTextSpan3557" class="CharOverride-14" style="position:absolute;top:3112.14px;left:240px;letter-spacing:6.58px;">Organizations </span><span id="_idTextSpan3558" class="CharOverride-14" style="position:absolute;top:3112.14px;left:1655.29px;letter-spacing:5.36px;">that </span><span id="_idTextSpan3559" class="CharOverride-14" style="position:absolute;top:3112.14px;left:2090.1px;letter-spacing:6.9px;">specialize </span><span id="_idTextSpan3560" class="CharOverride-14" style="position:absolute;top:3112.14px;left:3103.96px;letter-spacing:4.83px;">in </span><span id="_idTextSpan3561" class="CharOverride-14" style="position:absolute;top:3112.14px;left:3349.03px;letter-spacing:4.99px;">the </span><span id="_idTextSpan3562" class="CharOverride-14" style="position:absolute;top:3112.14px;left:3709.6px;letter-spacing:3.65px;">development </span><span id="_idTextSpan3563" class="CharOverride-14" style="position:absolute;top:3112.14px;left:5000.69px;letter-spacing:2.35px;">of </span><span id="_idTextSpan3564" class="CharOverride-14" style="position:absolute;top:3112.14px;left:5232.37px;letter-spacing:6.13px;">standards </span><span id="_idTextSpan3565" class="CharOverride-14" style="position:absolute;top:3112.14px;left:6236.09px;letter-spacing:4.53px;">and </span><span id="_idTextSpan3566" class="CharOverride-14" style="position:absolute;top:3112.14px;left:6652.47px;letter-spacing:3.66px;">codes </span><span id="_idTextSpan3567" class="CharOverride-14" style="position:absolute;top:3384.14px;left:0px;letter-spacing:4.24px;">often </span><span id="_idTextSpan3568" class="CharOverride-14" style="position:absolute;top:3384.14px;left:530.98px;letter-spacing:3.96px;">create </span><span id="_idTextSpan3569" class="CharOverride-14" style="position:absolute;top:3384.14px;left:1151.35px;letter-spacing:4.55px;">them. </span><span id="_idTextSpan3570" class="CharOverride-14" style="position:absolute;top:3384.14px;left:1744.19px;letter-spacing:3.94px;">In </span><span id="_idTextSpan3571" class="CharOverride-14" style="position:absolute;top:3384.14px;left:1986.59px;letter-spacing:2.55px;">order </span><span id="_idTextSpan3572" class="CharOverride-14" style="position:absolute;top:3384.14px;left:2534.12px;letter-spacing:2.59px;">to </span><span id="_idTextSpan3573" class="CharOverride-14" style="position:absolute;top:3384.14px;left:2759.12px;letter-spacing:2.83px;">be </span><span id="_idTextSpan3574" class="CharOverride-14" style="position:absolute;top:3384.14px;left:3026.82px;letter-spacing:3.9px;">enforceable </span><span id="_idTextSpan3575" class="CharOverride-14" style="position:absolute;top:3384.14px;left:4179.97px;letter-spacing:3.18px;">by </span><span id="_idTextSpan3576" class="CharOverride-14" style="position:absolute;top:3384.14px;left:4444.46px;letter-spacing:1.57px;">law, </span><span id="_idTextSpan3577" class="CharOverride-14" style="position:absolute;top:3384.14px;left:4857.38px;letter-spacing:4.45px;">the </span><span id="_idTextSpan3578" class="CharOverride-14" style="position:absolute;top:3384.14px;left:5203.49px;letter-spacing:5.51px;">AHJ </span><span id="_idTextSpan3579" class="CharOverride-14" style="position:absolute;top:3384.14px;left:5627px;letter-spacing:3.5px;">must </span><span id="_idTextSpan3580" class="CharOverride-14" style="position:absolute;top:3384.14px;left:6139.43px;letter-spacing:2.25px;">adopt </span><span id="_idTextSpan3581" class="CharOverride-14" style="position:absolute;top:3384.14px;left:6716.58px;letter-spacing:4.68px;">stan-</span><span id="_idTextSpan3582" class="CharOverride-14" style="position:absolute;top:3656.14px;left:0px;letter-spacing:5.55px;">dards </span><span id="_idTextSpan3583" class="CharOverride-14" style="position:absolute;top:3656.14px;left:586.57px;letter-spacing:4.53px;">and </span><span id="_idTextSpan3584" class="CharOverride-14" style="position:absolute;top:3656.14px;left:995.77px;letter-spacing:3.91px;">codes. </span></p>'
        element = html.fromstring(script)
        node = Paragraph.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'Organizations that specialize in the development of standards and codes often create them. In order to be enforceable by law, the AHJ must adopt stan-dards and codes. \\\\ \n\n'))
