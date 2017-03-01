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

from nti.contenttools.types.run import Run
from nti.contenttools.types.text import TextNode

from nti.contenttools.tests import ContentToolsTestCase


class TestRunNode(ContentToolsTestCase):

    def test_run(self):
        node = Run()
        output = render_output(node)
        assert_that(output, is_(u''))
    
    def test_run_with_text_node(self):
        node = Run()
        child = TextNode('This is Sparta')
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'This is Sparta'))

    def test_run_bold(self):
        node = Run()
        node.styles = ['bold']
        output = render_output(node)
        assert_that(output, is_(u'\\textbf{}'))
    
    def test_run_bold_with_text(self):
        node = Run()
        child = TextNode(u'doraemon')
        node.add(child)
        node.styles = ['bold']
        output = render_output(node)
        assert_that(output, is_(u'\\textbf{doraemon}'))

    def test_run_modified(self):
        node = Run()
        node.styles = ['inserted']
        output = render_output(node)
        assert_that(output, is_(u'\\modified{}'))
    
    def test_run_modified_with_text(self):
        node = Run()
        child = TextNode(u'doraemon')
        node.add(child)
        node.styles = ['inserted']
        output = render_output(node)
        assert_that(output, is_(u'\\modified{doraemon}'))

    def test_run_italic(self):
        node = Run()
        node.styles = ['italic']
        output = render_output(node)
        assert_that(output, is_(u'\\textit{}'))
    
    def test_run_italic_with_text(self):
        node = Run()
        node.styles = ['italic']
        child = TextNode(u'doraemon')
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\textit{doraemon}'))

    def test_run_strike(self):
        node = Run()
        node.styles = ['strike']
        output = render_output(node)
        assert_that(output, is_(u'\\strikeout{}'))
    
    def test_run_strike_with_text(self):
        node = Run()
        node.styles = ['strike']
        child = TextNode(u'doraemon')
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\strikeout{doraemon}'))

    def test_run_sub(self):
        node = Run()
        node.styles = ['sub']
        output = render_output(node)
        assert_that(output, is_(u'\\textsubscript{}'))
    
    def test_run_sub_with_text(self):
        node = Run()
        node.styles = ['sub']
        child = TextNode(u'doraemon')
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\textsubscript{doraemon}'))

    def test_run_underline(self):
        node = Run()
        node.styles = ['underline']
        output = render_output(node)
        assert_that(output, is_(u'\\uline{}'))
    
    def test_run_underline_with_text(self):
        node = Run()
        node.styles = ['underline']
        child = TextNode(u'doraemon')
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\uline{doraemon}'))

    def test_run_superscript(self):
        node = Run()
        node.styles = ['superscript']
        output = render_output(node)
        assert_that(output, is_(u'\\textsuperscript{}'))
    
    def test_run_superscript_with_text(self):
        node = Run()
        node.styles = ['superscript']
        child = TextNode(u'doraemon')
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\textsuperscript{doraemon}'))

    def test_run_bold_underline(self):
        node = Run()
        node.styles = ['bold', 'underline']
        output = render_output(node)
        assert_that(output, is_(u'\\uline{\\textbf{}}'))
    
    def test_run_bold_underline_with_text(self):
        node = Run()
        node.styles = ['bold', 'underline']
        child = TextNode(u'doraemon')
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\uline{\\textbf{doraemon}}'))

    def test_run_bold_underline_italic(self):
        node = Run()
        node.styles = ['bold', 'underline', 'italic']
        output = render_output(node)
        assert_that(output, is_(u'\\textit{\\uline{\\textbf{}}}'))
    
    def test_run_bold_underline_italic_with_text(self):
        node = Run()
        node.styles = ['bold', 'underline', 'italic']
        child = TextNode(u'doraemon')
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\textit{\\uline{\\textbf{doraemon}}}'))
