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

from nti.contenttools.adapters.epub.prmia.run import Run

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.adapters.epub.prmia.tests import PRMIATestCase

from nti.contenttools.adapters.epub.prmia.tests import create_epub_object

class TestRunAdapter(PRMIATestCase):
    def test_div_group(self):
        script = u"""<div><div class="group">
        <p class="image"><a id="ch01fig1"></a><img src="f0002-01.gif" alt="Image"/></p>
        <p class="figcap"><strong>FIGURE 1-1</strong> The Risk Management Process</p>
        </div></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        assert_that(epub.ids, is_(["ch01fig1"]))
        output = render_output(node)
        assert_that(output, is_(u'\\begin{figure}\n\\begin{center}\n\\includegraphics[width=0px,height=0px]{Images/CourseAssets/PRMIATest/f0002-01.gif}\n\\caption{\\textbf{FIGURE 1-1} The Risk Management Process}\n\\label{ch01fig1}\n\\end{center}\n\\end{figure}\n'))

    def test_div_sidebar(self):
        script = u"""<div><div class="sidebar"><p class="side-title"><a id="ch03sb1"></a><strong>BOX 3-1 BANK REGULATION AND RISK MANAGEMENT</strong></p><p class="noindentt">Para 1</p><p class="indent">Para 2</p></div></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        output = render_output(node)
        assert_that(output, is_(u'\n\\begin{sidebar}{\\textbf{BOX 3-1 BANK REGULATION AND RISK MANAGEMENT}}\n\\label{ch03sb1}Para 1\n\nPara 2\n\n\n\\end{sidebar}\n\\\\\n'))


    def test_h2_element(self):
        script = u"""<div><h2 class="h2" id="ch07">Chapter 7</h2></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        output = render_output(node)
        assert_that(output, is_(u'\\chapter{Chapter 7}\n\\label{ch07}\n'))
        for item in epub.labels:
            assert_that(item, is_(u'ch07'))

    def test_div_group_table(self):
        script = u"""<div><div class="group">
        <p class="tabcap"><a id="ch07tab2"></a><strong>TABLE 7-2</strong> Example of a Selection of Risk Factors</p>
        <p class="image"><img src="f0247-01.gif" alt="Image"/></p>
        </div></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        output = render_output(node)
        assert_that(output, is_(u'\n\\begin{table}\n\\caption{\\textbf{TABLE 7-2} Example of a Selection of Risk Factors}\n\\label{ch07tab2}\n\\begin{tabular}{ l }\n\\includegraphics{Images/CourseAssets/PRMIATest/f0247-01.gif}\n\\end{tabular}\n\\end{table}\n'))