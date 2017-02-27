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

from nti.contenttools.types.math import Mtr
from nti.contenttools.types.math import Mtd
from nti.contenttools.types.math import Math
from nti.contenttools.types.math import MRow
from nti.contenttools.types.math import MSub
from nti.contenttools.types.math import MSup
from nti.contenttools.types.math import MFrac
from nti.contenttools.types.math import Msqrt
from nti.contenttools.types.math import MRoot
from nti.contenttools.types.math import Mtable
from nti.contenttools.types.math import MUnder
from nti.contenttools.types.math import MFenced
from nti.contenttools.types.math import MathRun
from nti.contenttools.types.math import MSubSup
from nti.contenttools.types.math import MUnderover
from nti.contenttools.types.math import MOver
from nti.contenttools.types.math import MMultiscripts
from nti.contenttools.types.math import MMprescripts

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

    def test_mfrac(self):
        node = MFrac()
        child_1 = MathRun()
        child_2 = MathRun()
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_('\\frac{}{}'))

    def test_double_frac(self):
        node = MFrac()
        child_1 = MathRun()
        g_child_1 = MFrac()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_(u'\\frac{\\frac{}{}}{}'))

    def test_msub(self):
        node = MSub()
        child_1 = MathRun()
        child_2 = MathRun()
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_(u'{}_{}'))

    def test_double_msub_1(self):
        node = MSub()
        child_1 = MathRun()
        g_child_1 = MSub()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_(u'{{}_{}}_{}'))

    def test_double_msub_2(self):
        node = MSub()
        child_1 = MathRun()
        g_child_1 = MSub()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        node.add(child_2)
        node.add(child_1)
        output = render_output(node)
        assert_that(output, is_(u'{}_{{}_{}}'))

    def test_double_msup_1(self):
        node = MSup()
        child_1 = MathRun()
        g_child_1 = MSup()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_(u'{{}^{}}^{}'))

    def test_double_msup_2(self):
        node = MSup()
        child_1 = MathRun()
        g_child_1 = MSup()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        node.add(child_2)
        node.add(child_1)
        output = render_output(node)
        assert_that(output, is_(u'{}^{{}^{}}'))

    def test_msup(self):
        node = MSup()
        child_1 = MathRun()
        child_2 = MathRun()
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_(u'{}^{}'))

    def test_msubsup(self):
        node = MSubSup()
        child_1 = MathRun()
        child_2 = MathRun()
        child_3 = MathRun()
        node.add(child_1)
        node.add(child_2)
        node.add(child_3)
        output = render_output(node)
        assert_that(output, is_(u'{}_{}^{}'))

    def test_double_msubsup_1(self):
        node = MSubSup()
        child_1 = MathRun()
        g_child_1 = MSup()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        child_3 = MathRun()
        node.add(child_1)
        node.add(child_2)
        node.add(child_3)
        output = render_output(node)
        assert_that(output, is_(u'{{}^{}}_{}^{}'))

    def test_double_msubsup_2(self):
        node = MSubSup()
        child_1 = MathRun()
        g_child_1 = MSub()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        child_3 = MathRun()
        node.add(child_1)
        node.add(child_2)
        node.add(child_3)
        output = render_output(node)
        assert_that(output, is_(u'{{}_{}}_{}^{}'))

    def test_double_msubsup_3(self):
        node = MSubSup()
        child_1 = MathRun()
        g_child_1 = MSub()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        child_3 = MathRun()
        node.add(child_2)
        node.add(child_1)
        node.add(child_3)
        output = render_output(node)
        assert_that(output, is_(u'{}_{{}_{}}^{}'))

    def test_msqrt(self):
        node = Msqrt()
        output = render_output(node)
        assert_that(output, is_(u'\\sqrt{}'))

    def test_mroot(self):
        node = MRoot()
        child_1 = MathRun()
        child_2 = MathRun()
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_(u'\\sqrt[]{}'))

    def test_double_mroot_1(self):
        node = MRoot()
        child_1 = MathRun()
        g_child_1 = MRoot()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_(u'\\sqrt[\\sqrt[]{}]{}'))

    def test_double_mroot_2(self):
        node = MRoot()
        child_1 = MathRun()
        g_child_1 = MRoot()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        node.add(child_2)
        node.add(child_1)
        output = render_output(node)
        assert_that(output, is_(u'\\sqrt[]{\\sqrt[]{}}'))

    def test_munder(self):
        node = MUnder()
        child_1 = MathRun()
        child_2 = MathRun()
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_(u'\\underset{}{}'))

    def test_munder_with_other_element_1(self):
        node = MUnder()
        child_1 = MathRun()
        g_child_1 = MRoot()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_(u'\\underset{}{\\sqrt[]{}}'))

    def test_munder_with_other_element_2(self):
        node = MUnder()
        child_1 = MathRun()
        g_child_1 = MRoot()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        g_child_2 = MSub()
        gg_child_21 = MathRun()
        gg_child_22 = MathRun()
        g_child_2.add(gg_child_21)
        g_child_2.add(gg_child_22)
        child_2.add(g_child_2)
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_(u'\\underset{{}_{}}{\\sqrt[]{}}'))

    def test_munderover(self):
        node = MUnderover()
        child_1 = MathRun()
        child_2 = MathRun()
        child_3 = MathRun()
        node.add(child_1)
        node.add(child_2)
        node.add(child_3)
        output = render_output(node)
        assert_that(output, is_(u'\\overset{}{\\underset{}{}}'))
        
    def test_mover(self):
        node = MOver()
        child_1 = MathRun()
        child_2 = MathRun()
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_(u'\\overset{}{}'))
        
    def test_mover_with_other_element_1(self):
        node = MOver()
        child_1 = MathRun()
        g_child_1 = MRoot()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        node.add(child_1)
        node.add(child_2)
        output = render_output(node)
        assert_that(output, is_(u'\\overset{}{\\sqrt[]{}}'))

    def test_mover_with_other_element_2(self):
        node = MOver()
        child_1 = MathRun()
        g_child_1 = MRoot()
        gg_child_11 = MathRun()
        gg_child_12 = MathRun()
        g_child_1.add(gg_child_11)
        g_child_1.add(gg_child_12)
        child_1.add(g_child_1)
        child_2 = MathRun()
        node.add(child_2)
        node.add(child_1)
        output = render_output(node)
        assert_that(output, is_(u'\\overset{\\sqrt[]{}}{}'))
        
    def test_mprescripts(self):
        node = MMprescripts()
        node_sup = MSup()
        sup_child_1 = MathRun()
        sup_child_2 = MathRun()
        node_sup.add(sup_child_1)
        node_sup.add(sup_child_2)
        node_sub = MSub()
        sub_child_1 = MathRun()
        sub_child_2 = MathRun()
        node_sup.add(sub_child_1)
        node_sup.add(sub_child_2)
        node.sub = node_sub
        node.sup = node_sup
        output = render_output(node)
        assert_that(output, is_(u'{_{}^{}}'))
    
    def test_mmultiscript(self):
        node = MMprescripts()
        node_sup = MSup()
        sup_child_1 = MathRun()
        sup_child_2 = MathRun()
        node_sup.add(sup_child_1)
        node_sup.add(sup_child_2)
        node_sub = MSub()
        sub_child_1 = MathRun()
        sub_child_2 = MathRun()
        node_sup.add(sub_child_1)
        node_sup.add(sub_child_2)
        node.sub = node_sub
        node.sup = node_sup
        multiscript_node = MMprescripts()
        multiscript_node.base = MathRun()
        multiscript_node.prescript = node
        output = render_output(node)
        assert_that(output, is_(u'{_{}^{}}'))
        