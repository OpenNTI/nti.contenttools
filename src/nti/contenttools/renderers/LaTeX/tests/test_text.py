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

from nti.contenttools.types.text import TextNode

from nti.contenttools.tests import ContentToolsTestCase

class TestTextNode(ContentToolsTestCase):
    
    def test_simple_text_node(self):
        node = TextNode('Hello There')
        output = render_output(node)
        assert_that(output, is_('Hello There'))
    
    def test_text_node_special_char(self):
        node = TextNode(u'hello from plain µ δ Τ')
        output = render_output(node)
        #TODO : check why δ Τ are rendered as \u03b4 \u03a4
        assert_that(output, is_(u'hello from plain $\mu$ \u03b4 \u03a4'))
        
    def test_text_node_special_char_omath(self):
        node = TextNode(u'µ δ Τ', type_text='omath')
        output = render_output(node)
        assert_that(output, is_(u'\mu  \delta  \Tau '))
    
    def test_text_node_special_char_math(self):
        node = TextNode(u'µ δ Τ', type_text='math')
        output = render_output(node)
        assert_that(output, is_(u'\mu  \delta  \Tau '))
        