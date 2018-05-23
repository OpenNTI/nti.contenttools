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
        assert_that(output, is_(u'\\begin{figure}\n\\begin{center}\n\\includegraphics[width=0px,height=0px]{Images/CourseAssets/PRMIATest/f0002-01.gif}\n\caption{\textbf{FIGURE 1-1} The Risk Management Process}\n\\label{ch01fig1}\n\\end{center}\n\\end{figure}\n'))
