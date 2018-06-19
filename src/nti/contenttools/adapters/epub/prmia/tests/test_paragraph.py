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

from nti.contenttools.adapters.epub.prmia.paragraph import Paragraph

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.adapters.epub.prmia.tests import PRMIATestCase

from nti.contenttools.adapters.epub.prmia.tests import create_epub_object

from nti.contenttools.adapters.epub.prmia.finder import search_sections_of_real_page_number

class TestParagraphAdapter(PRMIATestCase):

    def test_simple_paragraph(self):
        script = u'<p>This is the first paragraph</p>'
        element = html.fromstring(script)
        node = Paragraph.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'This is the first paragraph\n\n'))

    def test_center_node(self):
        script = u'<div><p class="center">***</p></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{center}\n***\n\\end{center}\n'))

    def test_bulleted_paragraph(self):
    	script = u"""<div><p class="list-bulleted-first">&#8226; 
    	<em>The role of the board must be strengthened.</em> 
    	Strengthening board oversight of risk does not diminish the fundamental responsibility of management for the risk management process.</p></div>"""
    	element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{itemize}\n\\item * \\textit{The role of the board must be strengthened.} Strengthening board oversight of risk does not diminish the fundamental responsibility of management for the risk management process. \n\n\\end{itemize}\n'))


    def test_heading_2(self):
        script = u'<div><h2 class="h2a"><strong>CORPORATE RISK MANAGEMENT: A PRIMER</strong></h2></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\chapter{\\textbf{CORPORATE RISK MANAGEMENT: A PRIMER}}\n\\label{chapter:CORPORATE_RISK_MANAGEMENT__A_PRIMER_}\n'))

    def test_heading_3(self):
        script = u'<div><h3 class="h3a"><strong>CORPORATE RISK MANAGEMENT: A PRIMER</strong></h3></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\section{\\textbf{CORPORATE RISK MANAGEMENT: A PRIMER}}\n\\label{section:CORPORATE_RISK_MANAGEMENT__A_PRIMER_}\n'))

    def test_heading_4(self):
        script = u'<div><h4 class="h4a"><strong>CORPORATE RISK MANAGEMENT: A PRIMER</strong></h4></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\subsection{\\textbf{CORPORATE RISK MANAGEMENT: A PRIMER}}\n\\label{subsection:CORPORATE_RISK_MANAGEMENT__A_PRIMER_}\n'))

    def test_footnote_node(self):
        script = u'<div><p class="footnote">This is footnote</p></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\footnote{This is footnote}'))

    def test_footnote_node2(self):
        script = u'<div><p class="footnote"><sup><a id="ch03fn29"></a><a href="ch03.html#ch03fn_29">29</a></sup>The stock of high-quality liquid assets is composed of Level 1 assets and Level 2 assets.</p></div>'
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        for item in epub.footnote_ids:
            footnote_node = epub.footnote_ids[item]
            output = render_output(footnote_node)
            assert_that(output,
                    is_(u'\\footnote{\\label{ch03fn29}The stock of high-quality liquid assets is composed of Level 1 assets and Level 2 assets.}'))

    def test_para_index(self):
        script_1 = u'<div><h2>Chapter 1</h2><h3>Section 1</h3><p><a id="page_39"></a></p></div>'
        element = html.fromstring(script_1)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        search_sections_of_real_page_number(node, [], epub.page_numbers)
        
        script_2 = u'<div><p class="indexmain">Apple, <a href="ch01a.html#page_39">39</a></p></div>'
        element_2 = html.fromstring(script_2)
        node_2 = Run.process(element_2, epub=epub)
        
        output = render_output(node_2)
        assert_that(output, is_(u'\\ntiidref{section:Section_1}<Apple>\n\n'))
        

    def test_para_index2(self):
        script_1 = u'<div><h2>Chapter 1</h2><h3>Section 1</h3><p><a id="page_48"></a></p><h3>Section 2</h3><p><a id="page_156"></a></p></div>'
        element = html.fromstring(script_1)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        search_sections_of_real_page_number(node, [], epub.page_numbers)

        script_2 = u'<div><p class="indexmain">Agency risk, <a href="ch02.html#page_48">48</a>, <a href="ch04.html#page_156">156</a></p></div>'
        element_2 = html.fromstring(script_2)
        node_2 = Run.process(element_2, epub=epub)
        
        output = render_output(node_2)
        assert_that(output, is_(u'\\ntiidref{section:Section_1}<Agency risk>, \\ntiidref{section:Section_2}<Agency risk>\n\n'))

