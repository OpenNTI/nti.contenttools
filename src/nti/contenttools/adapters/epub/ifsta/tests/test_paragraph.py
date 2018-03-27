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

from nti.contenttools.adapters.epub.ifsta.run import Run

from nti.contenttools.adapters.epub.ifsta.paragraph import Paragraph

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.tests import ContentToolsTestCase

from nti.contenttools.adapters.epub.ifsta.tests import create_epub_object


class TestParagraphAdapter(ContentToolsTestCase):

    def test_simple_paragraph(self):
        script = u'<p>This is the first paragraph</p>'
        element = html.fromstring(script)
        node = Paragraph.process(element)
        output = render_output(node)

        assert_that(output,
                    is_(u'This is the first paragraph\n\n'))

    def test_table_title(self):
        script = u'<div><p class="Table-Title">Cryogenic <br />Containers</p></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\textbf{Cryogenic \\newline Containers}'))

    def test_second_paragraph_2(self):
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
                    is_(u'Organizations that specialize in the development of standards and codes often create them. In order to be enforceable by law, the AHJ must adopt stan-dards and codes. \n\n'))

    def test_h1(self):
        script = u'<div><h1>This is heading 1</h1></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\chapter{This is heading 1}\n\n'))

    def test_h2(self):
        script = u'<div><h2>This is heading 2</h2></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\section{This is heading 2}\n\n'))

    def test_h3(self):
        script = u'<div><h3>This is heading 3</h3></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\subsection{This is heading 3}\n\n'))

    def test_h4(self):
        script = u'<div><h4>This is heading 4</h4></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\subsubsection{This is heading 4}\n\n'))

    def test_h5(self):
        script = u'<div><h5>This is heading 5</h5></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\paragraph{This is heading 5}\n\n'))

    def test_h6(self):
        script = u'<div><h6>This is heading 6</h6></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\subparagraph{This is heading 6}\n\n'))

    def test_h7(self):
        script = u'<div><h7>This is heading 7</h7></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\subsubparagraph{This is heading 7}\n\n'))

    def test_sidebar_info(self):
        """
        This case is found in IFSTA Book 5 : Fire and Emergency Services Company Officer Fifth Edition
        """
        script = """<div><p class="sidebars-body-text ParaOverride-11"><span class="CharOverride-12"><img class="_idGenObjectAttribute-2" src="image/Info_Icon.png" alt="" />Other Possible Duties</span></p></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        epub.book_title = 'epub_test'
        epub.epub_type = 'ifsta_rf'
        epub.input_file = False
        node = Run.process(element, epub=epub) 
        output = render_output(node)
        assert_that(output,
                    is_(u'\n\\begin{sidebar}{\\textit{\\begin{figure}[h]\n\\includegraphics{Images/CourseAssets/epub_test/Info_Icon.png}\n\\end{figure}\nOther Possible Duties}}\n\n\\end{sidebar}\n\\\\\n'))

    def test_sidebar_info_marked_as_body_text(self):
        """
        This case is found in IFSTA Book 5 : Fire and Emergency Services Company Officer Fifth Edition
        """
        script = """<div><p class="Body-Text"><span class="CharOverride-34"><img class="_idGenObjectAttribute-2" src="image/Info_Icon.png" alt="" />Elements of Flashover</span></p></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        epub.book_title = 'epub_test'
        epub.epub_type = 'ifsta_rf'
        epub.input_file = False
        node = Run.process(element, epub=epub) 
        output = render_output(node)
        assert_that(output,
                    is_(u'\n\\begin{sidebar}{\\begin{figure}[h]\n\\includegraphics{Images/CourseAssets/epub_test/Info_Icon.png}\n\\end{figure}\nElements of Flashover}\n\n\\end{sidebar}\n\\\\\n'))
