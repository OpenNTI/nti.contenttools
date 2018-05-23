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

