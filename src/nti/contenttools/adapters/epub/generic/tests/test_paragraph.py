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

from nti.contenttools.adapters.epub.generic.paragraph import Paragraph

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

	def test_heading_one(self):
		script = u'<div><h1>Heading 1</h1></div>'
		element = html.fromstring(script)
		node = Run.process(element)
		output = render_output(node)
		assert_that(output,
		            is_(u'\chapter{Heading 1}\n\n'))

	def test_heading_two(self):
		script = u'<div><h2>Heading 2</h2></div>'
		element = html.fromstring(script)
		node = Run.process(element)
		output = render_output(node)
		assert_that(output,
		            is_(u'\section{Heading 2}\n\n'))

	def test_heading_three(self):
		script = u'<div><h3>Heading 3</h3></div>'
		element = html.fromstring(script)
		node = Run.process(element)
		output = render_output(node)
		assert_that(output,
		            is_(u'\subsection{Heading 3}\n\n'))

	def test_heading_four(self):
		script = u'<div><h4>Heading 4</h4></div>'
		element = html.fromstring(script)
		node = Run.process(element)
		output = render_output(node)
		assert_that(output,
		            is_(u'\subsubsection{Heading 4}\n\n'))

	def test_heading_five(self):
		script = u'<div><h5>Heading 5</h5></div>'
		element = html.fromstring(script)
		node = Run.process(element)
		output = render_output(node)
		assert_that(output,
		            is_(u'\paragraph{Heading 5}\n\n'))

	def test_heading_six(self):
		script = u'<div><h6>Heading 6</h6></div>'
		element = html.fromstring(script)
		node = Run.process(element)
		output = render_output(node)
		assert_that(output,
		            is_(u'\subparagraph{Heading 6}\n\n'))

	def test_heading_seven(self):
		script = u'<div><h7>Heading 7</h7></div>'
		element = html.fromstring(script)
		node = Run.process(element)
		output = render_output(node)
		assert_that(output,
		            is_(u'\subsubparagraph{Heading 6}\n\n'))