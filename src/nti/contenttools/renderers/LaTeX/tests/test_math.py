#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
from pty import CHILD

__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.math import Math
from nti.contenttools.types.math import MRow
from nti.contenttools.types.math import MathRun
from nti.contenttools.types.math import MFenced
from nti.contenttools.types.math import Mtable
from nti.contenttools.types.math import Mtr
from nti.contenttools.types.math import Mtd

from nti.contenttools.tests import ContentToolsTestCase


class TestMath(ContentToolsTestCase):

    def test_math(self):
        node = Math()
        output = render_output(node)
        assert_that(output, is_(u''))

    def test_mrow(self):
        node = MRow()
        output = render_output(node)
        assert_that(output, is_(u''))

    def test_mfenced(self):
        node = MFenced()
        output = render_output(node)
        assert_that(output, is_(u''))
    
    def test_mfenced_with_mtable(self):
        node = MFenced()
        child = Mtable()
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\begin{matrix}\n\\end{matrix}\n'))
    
    def test_mfenced_bmatrix(self):
        node = MFenced()
        node.opener = u'['
        child = Mtable()
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\begin{bmatrix}\n\\end{bmatrix}\n'))
    
    def test_mfenced_pmatrix(self):
        node = MFenced()
        node.opener = u'('
        child = Mtable()
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\begin{pmatrix}\n\\end{pmatrix}\n'))
    
    def test_mfenced_with_mrow_mtable(self):
        node = MFenced()
        child = MRow()
        grandchild = Mtable()
        child.add(grandchild)
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\begin{matrix}\n\\end{matrix}\n'))

    def test_math_run(self):
        node = MathRun()
        output = render_output(node)
        assert_that(output, is_(u''))
    
    def test_mtable(self):
        node = Mtable()
        output = render_output(node)
        assert_that(output, is_('\\begin{array}{}\n\\end{array}'))
    
    def test_mtr(self):
        node = Mtr()
        output = render_output(node)
        assert_that(output, is_('\\\\\n'))
    
    def test_mtd(self):
        node = Mtd()
        output = render_output(node)
        assert_that(output, is_(u''))
    
    def test_mtable_with_mtr_mtd(self):
        node = Mtable()
        node.number_of_col = 1
        child = Mtr()
        grandchild = Mtd()
        child.add(grandchild)
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\begin{array}{ l }\n\\\\\n\\end{array}'))
        
