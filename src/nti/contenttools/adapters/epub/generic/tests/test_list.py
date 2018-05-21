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

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.tests import ContentToolsTestCase

class TestListAdapter(ContentToolsTestCase):

    def test_ul_element(self):
        script = u"""<div><ul>
        <li>Coffee</li>
        <li>Tea</li>
        <li>Milk</li>
        </ul></div>"""
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{itemize}\n\\item Coffee \n\\item Tea \n\\item Milk \n\n\\end{itemize}\n'))

    def test_ol_element(self):
        script = u"""<div><ol>
        <li>Coffee</li>
        <li>Tea</li>
        <li>Milk</li>
        </ol></div>"""
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{enumerate}\n\\item Coffee \n\\item Tea \n\\item Milk \n\n\\end{enumerate}\n'))