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

from nti.contenttools.adapters.epub.tcia.paragraph import Paragraph

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.adapters.epub.tcia.tests import TCIATestCase


class TestParagraphAdapter(TCIATestCase):

    def test_simple_paragraph(self):
        script = u'<p>This is the first paragraph</p>'
        element = html.fromstring(script)
        node = Paragraph.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'This is the first paragraph\n\n'))

    def test_chapter_paragraph(self):
        script = u'<div><p class="CL-CHPTR-HEADS ParaOverride-11"><span class="CharOverride-15">QUALITY CONTROL AND PROFESSIONALISM</span></p></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\chapter{QUALITY CONTROL AND PROFESSIONALISM}\n\\label{chapter:QUALITY_CONTROL_AND_PROFESSIONALISM}\n\n'))

    def test_section_paragraph(self):
        script = u'<div><p class="CL-SUBHEADS ParaOverride-5">Learning objectives</p></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\section{Learning objectives}\n\\label{section:Learning_objectives}\n\n'))

    def test_paragraph_list(self):
        script = u'<div><p class="CL-BODY-TEXT ParaOverride-16">• Sets high expectations.</p></div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{itemize}\n\\item Sets high expectations. \n\n\\end{itemize}\n'))