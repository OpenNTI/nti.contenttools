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

from nti.contenttools.types.omath import OMath
from nti.contenttools.types.omath import OMathRun
from nti.contenttools.types.omath import OMathPara

from nti.contenttools.types.text import TextNode

from nti.contenttools.tests import ContentToolsTestCase

class OMathTest(ContentToolsTestCase):
    def test_omath(self):
        node = OMath()
        text = TextNode(u'µ δ Τ', type_text='omath')
        node.add(text)
        output = render_output(node)
        assert_that(output, is_(u'$\\mu  \\delta  \\Tau $'))
    
    def test_omath_para(self):
        node = OMathPara()
        text = TextNode(u'µ δ Τ', type_text='omath')
        node.add(text)
        output = render_output(node)
        assert_that(output, is_(u'$\\mu  \\delta  \\Tau $'))
    
    def test_omath_para_under_omath(self):
        omath = OMath()
        node = OMathPara()
        text = TextNode(u'µ δ Τ', type_text='omath')
        node.add(text)
        omath.add(node)
        output = render_output(omath)
        assert_that(output, is_(u'$$\\mu  \\delta  \\Tau $$'))
    
    def test_omath_run(self):
        node = OMathRun()
        text = TextNode(u'test: Τ', type_text='omath')
        node.add(text)
        output = render_output(node)
        assert_that(output, is_(u'test: \\Tau '))
    
    def test_omath_run_under_omath(self):
        omath = OMath()
        node = OMathRun()
        text = TextNode(u'test: Τ', type_text='omath')
        node.add(text)
        omath.add(node)
        output = render_output(omath)
        assert_that(output, is_(u'$test: \\Tau $'))
    
    def test_omath_run_under_omath_para(self):
        omath_para = OMathPara()
        node = OMathRun()
        text = TextNode(u'test: Τ', type_text='omath')
        node.add(text)
        omath_para.add(node)
        output = render_output(omath_para)
        assert_that(output, is_(u'$test: \\Tau $'))
    
    def test_omath_run_under_omath_and_para(self):
        omath = OMath()
        omath_para = OMathPara()
        node = OMathRun()
        text = TextNode(u'test: Τ', type_text='omath')
        node.add(text)
        omath_para.add(node)
        omath.add(omath_para)
        output = render_output(omath)
        assert_that(output, is_(u'$$test: \\Tau $$'))
        