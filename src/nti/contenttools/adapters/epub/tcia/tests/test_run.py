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

from nti.contenttools.adapters.epub.tcia.run import Run

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.adapters.epub.tcia.tests import TCIATestCase

from nti.contenttools.adapters.epub.tcia.tests import create_epub_object

class TestRunAdapter(TCIATestCase):

    def test_b_element(self):
        script = u'<div><b>This is a bold text</b></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\textbf{This is a bold text}'))

    def test_i_element(self):
        script = u'<div><i>This is an italic text</i></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\textit{This is an italic text}'))

    def test_u_element(self):
        script = u'<div><u>This is an underline text</u></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\uline{This is an underline text}'))

    def test_strong_element(self):
        script = u'<div><strong>This is a bold text</strong></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\textbf{This is a bold text}'))

    def test_s_element(self):
        script = u'<div><s>This is a strikeout text</s></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\strikeout{This is a strikeout text}'))

    def test_em_element(self):
        script = u'<div><em>This is an italic text</em></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\textit{This is an italic text}'))
    
    def test_sub_element(self):
        script = u'<div><sub>This is a sub text</sub></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\textsubscript{This is a sub text}'))
    
    def test_sup_element(self):
        script = u'<div><sup>This is a sup text</sup></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\textsuperscript{This is a sup text}'))

    def test_div_element(self):
        script = u'<div><div><p>test paragraph under div element</p></div></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'test paragraph under div element\n\n'))

    def test_span_bold_italic(self):
        script = """<div><p class="CL-BODY-TEXT"><span class="CharOverride-34">Crew leaders only:</span></p></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        epub.epub_type = 'tcia'
        node = Run.process(element, epub=epub) 
        output = render_output(node)
        assert_that(output,
                    is_(u'\\textbf{\\textit{Crew leaders only:}}\n\n'))
