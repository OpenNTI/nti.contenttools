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

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.paragraph import Paragraph
from nti.contenttools.types.text import TextNode

from nti.contenttools.tests import ContentToolsTestCase


class TestParagraph(ContentToolsTestCase):

    def test_simple_par(self):
        par = Paragraph(element_type='manga')
        output = render_output(par)
        assert_that(output, is_(u'\n\n'))
    
    def test_par_with_text(self):
        par = Paragraph(element_type='manga')
        text = TextNode('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
        par.add(text)
        output = render_output(par)
        assert_that(output, is_(u'\n\n'))
