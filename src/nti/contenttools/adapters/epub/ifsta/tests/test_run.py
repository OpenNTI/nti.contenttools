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

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.adapters.epub.ifsta.tests import IFSTATestCase

from nti.contenttools.adapters.epub.ifsta.tests import create_epub_object

class TestRunAdapter(IFSTATestCase):

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

    def test_span_oblique(self):
        script = u'<div id="_idContainer043" class="Basic-Text-Frame"><span class="CharOverride-12">Figure 13.10 </span>Steel with enough ductility will deform instead of breaching, as shown in this drum that contained a polymerization reaction. <span class="CharOverride-13">Courtesy of Barry Lindley.</span></div>'
        element = html.fromstring(script)
        epub = create_epub_object()
        epub.epub_type = 'ifsta_rf'
        node = Run.process(element, epub=epub) 
        output = render_output(node)
        assert_that(output,
                    is_(u'\\textit{Figure 13.10 }Steel with enough ductility will deform instead of breaching, as shown in this drum that contained a polymerization reaction. \\textbf{Courtesy of Barry Lindley.}'))

    def test_span_oblique_2(self):
        script = u'<div><span class="CharOverride-10">Figure 12.38</span> Technical decon is impractical at incidents where a large number of people must be decontaminated. <span class="CharOverride-12">Courtesy of David Lewis.</span></div>'
        element = html.fromstring(script)
        epub = create_epub_object()
        epub.epub_type = 'ifsta_rf'
        node = Run.process(element, epub=epub) 
        output = render_output(node)
        assert_that(output,
                    is_(u'\\textbf{Figure 12.38} Technical decon is impractical at incidents where a large number of people must be decontaminated. \\textit{Courtesy of David Lewis.}'))

    def test_span_bullet(self):
        script = u'<div>Test <span class="bullet CharOverride-3">Fire and Emergency Services Company Officer, 5th Edition</span></div>'
        element = html.fromstring(script)
        epub = create_epub_object()
        epub.epub_type = 'ifsta_rf'
        node = Run.process(element, epub=epub) 
        output = render_output(node)
        assert_that(output,
                    is_(u'Test \\textbf{Fire and Emergency Services Company Officer, 5th Edition}'))

    def test_span_italic(self):
        script = """<div><p class="Main ParaOverride-2"><span class="CharOverride-4">AAR. </span><span class="italic _idGenCharOverride-1">See</span><span class="CharOverride-4"> After Action Report (AAR); American Association of Railroads (AAR)</span></p></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        epub.epub_type = 'ifsta_rf'
        node = Run.process(element, epub=epub) 
        output = render_output(node)
        assert_that(output,
                    is_(u'AAR. \\textit{See} After Action Report (AAR); American Association of Railroads (AAR)\n\n'))

    def test_span_note(self):
        script = """<div><p class="Body-Text"><span class="NOTE _idGenCharOverride-2">NOTE:</span><span class="CharOverride-20"> </span>While fuel injectors do not have external moving parts, they are still a source of collected dirt and oil. This area should be checked and cleaned. </p></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        epub.epub_type = 'ifsta_rf'
        node = Run.process(element, epub=epub) 
        output = render_output(node)
        assert_that(output,
                    is_(u'\n\\begin{sidebar}[css-class=note]{NOTE:}\nNOTE: While fuel injectors do not have external moving parts, they are still a source of collected dirt and oil. This area should be checked and cleaned. \n\\end{sidebar}\n\\\\\n'))