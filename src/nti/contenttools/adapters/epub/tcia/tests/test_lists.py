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


class TestList(TCIATestCase):
    def test_ordered_list(self):
        script = u'<div><ol><li>item 1</li><li>item 2</li></ol><div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{enumerate}\n\\item item 1 \n\\item item 2 \n\n\\end{enumerate}\n'))

    def test_unordered_list(self):
        script = u'<div><ul><li>item 1</li><li>item 2</li></ul><div>'
        element = html.fromstring(script)
        node = Run.process(element)
        output = render_output(node)
        assert_that(output,
                    is_(u'\\begin{itemize}\n\\item item 1 \n\\item item 2 \n\n\\end{itemize}\n'))
