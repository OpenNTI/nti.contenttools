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

from nti.contenttools.types.footnote import Footnote
from nti.contenttools.types.footnote import FootnoteText
from nti.contenttools.types.footnote import FootnoteMark

from nti.contenttools.types.run import Run

from nti.contenttools.tests import ContentToolsTestCase

class TestFootnote(ContentToolsTestCase):
    def test_footnote(self):
        node = Footnote()
        output = render_output(node)
        assert_that(output, is_(u''))
    
    def test_footnote_with_some_text(self):
        node = Footnote()
        #todo : replace Run() with TextNode() 
        child_1 = Run()
        node.add(child_1)
        output = render_output(node)
        assert_that(output, is_(u''))
    
    def test_footnote_text(self):
        node = FootnoteText()
        node.text = 'this is footnote text'
        node.num = 1
        output = render_output(node)
        assert_that(output, is_(u'\\footnotetext[1]{this is footnote text}'))
    
    def test_footnote_mark_without_num(self):
        node = FootnoteMark()
        output = render_output(node)
        assert_that(output, is_(u''))
    
    def test_footnote_mark(self):
        node = FootnoteMark()
        node.num = 1
        output = render_output(node)
        assert_that(output, is_(u'\\footnotemark[1]'))