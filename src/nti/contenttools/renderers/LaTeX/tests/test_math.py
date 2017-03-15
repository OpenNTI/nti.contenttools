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
from nti.contenttools.types.math import MNone
from nti.contenttools.types.math import MOver
from nti.contenttools.types.math import MRoot
from nti.contenttools.types.math import Msqrt
from nti.contenttools.types.math import MText
from nti.contenttools.types.math import Mtable
from nti.contenttools.types.math import MUnder
from nti.contenttools.types.math import MFenced
from nti.contenttools.types.math import MathRun
from nti.contenttools.types.math import MSubSup
from nti.contenttools.types.math import MMenclose
from nti.contenttools.types.math import MUnderover
from nti.contenttools.types.math import MMprescripts
from nti.contenttools.types.math import MMultiscripts

from nti.contenttools.types.text import TextNode

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
        assert_that(output, is_(' \\\\\n'))

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
        assert_that(output, is_(u'\\begin{array}{ l }\n \\\\\n\\end{array}'))

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
        assert_that(output, is_(u'\\sqrt[]{\\sqrt[]{}}'))

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
        assert_that(output, is_(u'\\sqrt[\\sqrt[]{}]{}'))

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
        multiscript_node = MMultiscripts()
        multiscript_node.base = []
        multiscript_node.prescripts = node
        output = render_output(multiscript_node)
        assert_that(output, is_(u'{_{}^{}}'))

    def test_mmultiscript_with_mnone(self):
        node = MMprescripts()
        node_sup = MSup()
        sup_child_1 = MathRun()
        sup_child_2 = MNone()
        node_sup.add(sup_child_1)
        node_sup.add(sup_child_2)
        node_sub = MSub()
        sub_child_1 = MathRun()
        sub_child_2 = MNone()
        node_sup.add(sub_child_1)
        node_sup.add(sub_child_2)
        node.sub = node_sub
        node.sup = node_sup
        multiscript_node = MMultiscripts()
        multiscript_node.base = []
        multiscript_node.prescripts = node
        output = render_output(multiscript_node)
        assert_that(output, is_(u'{_{}^{}}'))

    def test_mnone(self):
        node = MNone()
        output = render_output(node)
        assert_that(output, is_(u''))

    def test_mtext(self):
        node = MText()
        output = render_output(node)
        assert_that(output, is_(u''))

    def test_menclose_updiagonalstrike(self):
        node = MMenclose()
        node.notation = u'updiagonalstrike'
        output = render_output(node)
        assert_that(output, is_(u'\\cancel{}'))

    def test_menclose_downdiagonalstrike(self):
        node = MMenclose()
        node.notation = u'downdiagonalstrike'
        output = render_output(node)
        assert_that(output, is_(u'\\bcancel{}'))

    def test_menclose_radical(self):
        node = MMenclose()
        node.notation = u'radical'
        output = render_output(node)
        assert_that(output, is_(u'\\sqrt{}'))

    def test_menclose_left(self):
        node = MMenclose()
        node.notation = u'left'
        output = render_output(node)
        assert_that(output, is_(u'\\Big|'))

    def test_menclose_right(self):
        node = MMenclose()
        node.notation = u'right'
        output = render_output(node)
        assert_that(output, is_(u'\\Big|'))

    def test_menclose_top(self):
        node = MMenclose()
        node.notation = u'top'
        output = render_output(node)
        assert_that(output, is_(u'\\overline{}'))

    def test_menclose_bottom(self):
        node = MMenclose()
        node.notation = u'bottom'
        output = render_output(node)
        assert_that(output, is_(u'\\underline{}'))

    def test_menclose_horizontalstrike(self):
        node = MMenclose()
        node.notation = u'horizontalstrike'
        output = render_output(node)
        assert_that(output, is_(u'\\hcancel{}'))

    def test_menclose_box(self):
        node = MMenclose()
        node.notation = u'box'
        output = render_output(node)
        assert_that(output, is_(u'\\boxed{}'))

    def test_menclose_longdiv(self):
        node = MMenclose()
        node.notation = u'longdiv'
        output = render_output(node)
        assert_that(output, is_(u'\\overline{}'))

    def test_complete_math_msup(self):
        """
        example from : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/math
#===============================================================================
#  <math>
#     <mrow>
#       <mrow>
#         <msup>
#           <mi>a</mi>
#           <mn>2</mn>
#         </msup>
#         <mo>+</mo>
#         <msup>
#           <mi>b</mi>
#           <mn>2</mn>
#         </msup>
#       </mrow>
#       <mo>=</mo>
#       <msup>
#         <mi>c</mi>
#         <mn>2</mn>
#       </msup>
#     </mrow>
#   </math>
#===============================================================================
        """
        math = Math()
        mrow_main = MRow()

        mrow = MRow()

        msup_1 = MSup()
        mi_1 = MathRun()
        mi_1.add(TextNode(u'a', type_text=u'math'))
        mn_1 = MathRun()
        mn_1.add(TextNode(u'2', type_text=u'math'))
        msup_1.add(mi_1)
        msup_1.add(mn_1)
        mrow.add(msup_1)

        mo_1 = MathRun()
        mo_1.add(TextNode(u'+', type_text=u'math'))
        mrow.add(mo_1)

        msup_2 = MSup()
        mi_2 = MathRun()
        mi_2.add(TextNode(u'b', type_text=u'math'))
        mn_2 = MathRun()
        mn_2.add(TextNode(u'2', type_text=u'math'))
        msup_2.add(mi_2)
        msup_2.add(mn_2)
        mrow.add(msup_2)

        mrow_main.add(mrow)

        mo_2 = MathRun()
        mo_2.add(TextNode(u'=', type_text=u'math'))
        mrow_main.add(mo_2)

        msup_3 = MSup()
        mi_3 = MathRun()
        mi_3.add(TextNode(u'c', type_text=u'math'))
        mn_3 = MathRun()
        mn_3.add(TextNode(u'2', type_text=u'math'))
        msup_3.add(mi_3)
        msup_3.add(mn_3)
        mrow_main.add(msup_3)

        math.add(mrow_main)

        output = render_output(math)
        assert_that(output, is_(u'\\[{a}^{2}+{b}^{2}={c}^{2}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\({a}^{2}+{b}^{2}={c}^{2}\\)'))

    def test_complete_math_mfrac(self):
        """
        example from  : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mfrac
#===============================================================================
# <math>  
#   <mfrac bevelled="true">
#      <mfrac>
#         <mi> a </mi>
#         <mi> b </mi>
#      </mfrac>
#      <mfrac>
#         <mi> c </mi>
#         <mi> d </mi>
#      </mfrac>
#   </mfrac>
# </math>
#===============================================================================
        """
        math = Math()
        mfrac = MFrac()

        mfrac_1 = MFrac()
        mi_1 = MathRun()
        mi_1.add(TextNode(u'a', type_text=u'math'))
        mi_2 = MathRun()
        mi_2.add(TextNode(u'b', type_text=u'math'))
        mfrac_1.add(mi_1)
        mfrac_1.add(mi_2)
        mfrac.add(mfrac_1)

        mfrac_2 = MFrac()
        mi_3 = MathRun()
        mi_3.add(TextNode(u'c', type_text=u'math'))
        mi_4 = MathRun()
        mi_4.add(TextNode(u'd', type_text=u'math'))
        mfrac_2.add(mi_3)
        mfrac_2.add(mi_4)
        mfrac.add(mfrac_2)

        math.add(mfrac)

        output = render_output(math)
        assert_that(output, is_(u'\\[\\frac{\\frac{a}{b}}{\\frac{c}{d}}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(
            output_inline, is_(u'\\(\\frac{\\frac{a}{b}}{\\frac{c}{d}}\\)'))

    def test_complete_math_msub(self):
        """
        example from : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/msub
#===============================================================================
# <math>
# 
#   <msub>
#     <mi>X</mi>
#     <mn>1</mn>
#   </msub> 
# 
# </math>
#===============================================================================
        """
        math = Math()

        msub = MSub()
        mi = MathRun()
        mi.add(TextNode(u'X', type_text=u'math'))
        msub.add(mi)
        mn = MathRun()
        mn.add(TextNode(u'1', type_text=u'math'))
        msub.add(mn)

        math.add(msub)
        output = render_output(math)
        assert_that(output, is_(u'\\[{X}_{1}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\({X}_{1}\\)'))

    def test_complete_math_msqrt(self):
        """
        example : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/msqrt
#===============================================================================
# <math>
# 
#  <msqrt>
#     <mi>x</mi>
#   </msqrt> 
# 
# </math>
#===============================================================================
        """
        math = Math()

        msqrt = Msqrt()
        mi = MathRun()
        mi.add(TextNode(u'X', type_text=u'math'))
        msqrt.add(mi)

        math.add(msqrt)
        output = render_output(math)
        assert_that(output, is_(u'\\[\\sqrt{X}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(\\sqrt{X}\\)'))

    def test_complete_math_mtable(self):
        """
        example : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mtable
#===============================================================================
# <math>
#     
#     <mi>X</mi>
#     <mo>=</mo>
#     <mtable frame="solid" rowlines="solid" align="axis 3">
#         <mtr>
#              <mtd><mi>A</mi></mtd>
#              <mtd><mi>B</mi></mtd>
#         </mtr>
#         <mtr>
#              <mtd><mi>C</mi></mtd>
#              <mtd><mi>D</mi></mtd>
#         </mtr>
#         <mtr>
#              <mtd><mi>E</mi></mtd>
#              <mtd><mi>F</mi></mtd>
#         </mtr>
#     </mtable>
# 
# </math>
#===============================================================================
        """
        math = Math()

        mi = MathRun()
        mi.add(TextNode(u'X', type_text=u'math'))
        math.add(mi)

        mo = MathRun()
        mo.add(TextNode(u'=', type_text=u'math'))
        math.add(mo)

        mtable = Mtable()
        mtable.number_of_col = 2

        mtr_1 = Mtr()

        mtd_1 = Mtd()
        mi_1 = MathRun()
        mi_1.add(TextNode(u'A', type_text=u'math'))
        mtd_1.add(mi_1)
        mtr_1.add(mtd_1)

        mtd_2 = Mtd()
        mi_2 = MathRun()
        mi_2.add(TextNode(u'B', type_text=u'math'))
        mtd_2.add(mi_2)
        mtr_1.add(mtd_2)

        mtable.add(mtr_1)

        mtr_2 = Mtr()

        mtd_3 = Mtd()
        mi_3 = MathRun()
        mi_3.add(TextNode(u'C', type_text=u'math'))
        mtd_3.add(mi_3)
        mtr_2.add(mtd_3)

        mtd_4 = Mtd()
        mi_4 = MathRun()
        mi_4.add(TextNode(u'D', type_text=u'math'))
        mtd_4.add(mi_4)
        mtr_2.add(mtd_4)

        mtable.add(mtr_2)

        mtr_3 = Mtr()

        mtd_5 = Mtd()
        mi_5 = MathRun()
        mi_5.add(TextNode(u'E', type_text=u'math'))
        mtd_5.add(mi_5)
        mtr_3.add(mtd_5)

        mtd_6 = Mtd()
        mi_6 = MathRun()
        mi_6.add(TextNode(u'F', type_text=u'math'))
        mtd_6.add(mi_6)
        mtr_3.add(mtd_6)

        mtable.add(mtr_3)

        math.add(mtable)
        output = render_output(math)
        assert_that(output, is_(
            u'\\[X=\\begin{array}{ l  l }\nA & B \\\\\nC & D \\\\\nE & F \\\\\n\\end{array}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(
            u'\\(X=\\begin{array}{ l  l }\nA & B \\\\\nC & D \\\\\nE & F \\\\\n\\end{array}\\)'))

    def test_complete_math_msubsup_integral(self):
        """
        example from : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/msubsup
#===============================================================================
# <math displaystyle="true">   
# 
#   <msubsup>
#     <mo> &#x222B;<!--Integral --> </mo>
#     <mn> 0 </mn>
#     <mn> 1 </mn>
#   </msubsup>
# 
# </math>
#===============================================================================
        """
        math = Math()

        msubsup = MSubSup()

        mo = MathRun()
        mo.add(TextNode(u'∫', type_text=u'math'))
        msubsup.add(mo)

        mn_1 = MathRun()
        mn_1.add(TextNode(u'0', type_text=u'math'))
        msubsup.add(mn_1)

        mn_2 = MathRun()
        mn_2.add(TextNode(u'1', type_text=u'math'))
        msubsup.add(mn_2)

        math.add(msubsup)

        output = render_output(math)
        assert_that(output, is_(u'\\[\\int_{0}^{1}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(\\int_{0}^{1}\\)'))

    def test_math_munder(self):
        """
        example from : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/munder
#===============================================================================
# <math>
# 
# <munder accentunder="true">
#   <mrow>
#     <mi> x </mi>
#     <mo> + </mo>
#     <mi> y </mi>
#     <mo> + </mo>
#     <mi> z </mi>
#   </mrow>
#   <mo> &#x23DF; <!--BOTTOM CURLY BRACKET--> </mo>
# </munder> 
# 
# </math>
#===============================================================================
        """
        math = Math()
        munder = MUnder()

        mrow = MRow()

        mi_1 = MathRun()
        mi_1.add(TextNode(u'x', type_text=u'math'))
        mrow.add(mi_1)

        mo_1 = MathRun()
        mo_1.add(TextNode(u'+', type_text=u'math'))
        mrow.add(mo_1)

        mi_2 = MathRun()
        mi_2.add(TextNode(u'y', type_text=u'math'))
        mrow.add(mi_2)

        mo_2 = MathRun()
        mo_2.add(TextNode(u'+', type_text=u'math'))
        mrow.add(mo_2)

        mi_3 = MathRun()
        mi_3.add(TextNode(u'z', type_text=u'math'))
        mrow.add(mi_3)

        munder.add(mrow)

        mo_4 = MathRun()
        mo_4.add(TextNode(u'⏟', type_text=u'math'))
        munder.add(mo_4)

        math.add(munder)

        output = render_output(math)
        assert_that(output, is_(u'\\[\\underbrace{x+y+z}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(\\underbrace{x+y+z}\\)'))

    def test_math_munderover(self):
        """
        example from : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/munderover
#===============================================================================
# <math displaystyle="true"> 
# 
#   <munderover >
#     <mo> &#x222B; <!--INTEGRAL--> </mo>
#     <mn> 0 </mn>
#     <mi> &#x221E; <!--INFINITY--> </mi>
#   </munderover>
# 
# </math>
#===============================================================================
        """
        math = Math()
        munderover = MUnderover()

        mo_1 = MathRun()
        mo_1.add(TextNode(u'∫', type_text=u'math'))
        munderover.add(mo_1)

        mi = MathRun()
        mi.add(TextNode(u'0', type_text=u'math'))
        munderover.add(mi)

        mo_2 = MathRun()
        mo_2.add(TextNode(u'∞', type_text=u'math'))
        munderover.add(mo_2)

        math.add(munderover)
        output = render_output(math)
        assert_that(output, is_(u'\\[\\int_{0}^{\\infty }\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(\\int_{0}^{\\infty }\\)'))

    def test_math_mover(self):
        """
        https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mover
#===============================================================================
# <math>
# 
# <mover accent="true">
#   <mrow>
#     <mi> x </mi>
#     <mo> + </mo>
#     <mi> y </mi>
#     <mo> + </mo>
#     <mi> z </mi>
#   </mrow>
#   <mo> &#x23DE; <!--TOP CURLY BRACKET--> </mo>
# </mover> 
# 
# </math>
#===============================================================================
        """
        math = Math()
        mover = MOver()

        mrow = MRow()

        mi_1 = MathRun()
        mi_1.add(TextNode(u'x', type_text=u'math'))
        mrow.add(mi_1)

        mo_1 = MathRun()
        mo_1.add(TextNode(u'+', type_text=u'math'))
        mrow.add(mo_1)

        mi_2 = MathRun()
        mi_2.add(TextNode(u'y', type_text=u'math'))
        mrow.add(mi_2)

        mo_2 = MathRun()
        mo_2.add(TextNode(u'+', type_text=u'math'))
        mrow.add(mo_2)

        mi_3 = MathRun()
        mi_3.add(TextNode(u'z', type_text=u'math'))
        mrow.add(mi_3)

        mover.add(mrow)

        mo_4 = MathRun()
        mo_4.add(TextNode(u'⏞', type_text=u'math'))
        mover.add(mo_4)

        math.add(mover)

        output = render_output(math)
        assert_that(output, is_(u'\\[\\overbrace{x+y+z}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(\\overbrace{x+y+z}\\)'))

    def test_math_mroot(self):
        """
        example : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mroot
#===============================================================================
# <math>
# 
#  <mroot>
#     <mi>x</mi>
#     <mn>3</mn>
#  </mroot> 
#  
# </math>
#===============================================================================
        """
        math = Math()

        mroot = MRoot()

        mi = MathRun()
        mi.add(TextNode(u'x', type_text=u'math'))
        mroot.add(mi)

        mn = MathRun()
        mn.add(TextNode(u'3', type_text=u'math'))
        mroot.add(mn)

        math.add(mroot)
        output = render_output(math)
        assert_that(output, is_(u'\\[\\sqrt[3]{x}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(\\sqrt[3]{x}\\)'))

    def test_math_mtext(self):
        """
        example: https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mtext 
#===============================================================================
# <math> 
# 
#   <mtext> Theorem of Pythagoras </mtext>  
#
# </math>
#===============================================================================
        """
        math = Math()
        mtext = MText()
        mtext.add(TextNode(u'Theorem of Pythagoras', type_text='math'))
        math.add(mtext)

        output = render_output(math)
        assert_that(output, is_(u'\\[\\text{Theorem of Pythagoras}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(\\text{Theorem of Pythagoras}\\)'))

        # TODO : mtext shoud be able to handle string /* and */ correctly:
        #mtext.add(TextNode(u' /* comment here */ ', type_text='math'))

    def test_math_mfenced_1(self):
        """
        example : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mfenced
#===============================================================================
# <math>
#   <mfenced open="{" close="}" separators=";;,"> 
#     <mi>a</mi> 
#     <mi>b</mi> 
#     <mi>c</mi> 
#     <mi>d</mi> 
#     <mi>e</mi> 
#   </mfenced> 
# </math>
#===============================================================================
        """
        math = Math()

        mfenced = MFenced()
        mfenced.opener = u'{'
        mfenced.close = u'}'
        mi_1 = MathRun()
        mi_1.add(TextNode(u'a', type_text='math'))
        mfenced.add(mi_1)
        mi_2 = MathRun()
        mi_2.add(TextNode(u'b', type_text='math'))
        mfenced.add(mi_2)
        mi_3 = MathRun()
        mi_3.add(TextNode(u'c', type_text='math'))
        mfenced.add(mi_3)
        mi_4 = MathRun()
        mi_4.add(TextNode(u'd', type_text='math'))
        mfenced.add(mi_4)
        mi_5 = MathRun()
        mi_5.add(TextNode(u'e', type_text='math'))
        mfenced.add(mi_5)

        math.add(mfenced)
        output = render_output(math)
        assert_that(output, is_(u'\\[\\{a,b,c,d,e\\}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(\\{a,b,c,d,e\\}\\)'))

    def test_math_mfenced_2(self):
        """
        example : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mfenced
        The last separator is repeated (,)
        Sample rendering: {a;b;c,d,e}
#===============================================================================
# <math>
#   <mfenced open="{" close="}" separators=";;,"> 
#     <mi>a</mi> 
#     <mi>b</mi> 
#     <mi>c</mi> 
#     <mi>d</mi> 
#     <mi>e</mi> 
#   </mfenced> 
# </math>
#===============================================================================
        """
        math = Math()

        mfenced = MFenced()
        mfenced.opener = u'{'
        mfenced.close = u'}'
        mfenced.separators = u';;,'
        mi_1 = MathRun()
        mi_1.add(TextNode(u'a', type_text='math'))
        mfenced.add(mi_1)
        mi_2 = MathRun()
        mi_2.add(TextNode(u'b', type_text='math'))
        mfenced.add(mi_2)
        mi_3 = MathRun()
        mi_3.add(TextNode(u'c', type_text='math'))
        mfenced.add(mi_3)
        mi_4 = MathRun()
        mi_4.add(TextNode(u'd', type_text='math'))
        mfenced.add(mi_4)
        mi_5 = MathRun()
        mi_5.add(TextNode(u'e', type_text='math'))
        mfenced.add(mi_5)

        math.add(mfenced)
        output = render_output(math)
        assert_that(output, is_(u'\\[\\{a;b;c,d,e\\}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(\\{a;b;c,d,e\\}\\)'))

    def test_math_mfenced_3(self):
        """
        example : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mfenced
        All excess is ignored (,)
        Sample rendering: [a|b|c|d|e]
#===============================================================================
# <math>
#   <mfenced open="[" close="]" separators="||||,"> 
#     <mi>a</mi> 
#     <mi>b</mi> 
#     <mi>c</mi> 
#     <mi>d</mi> 
#     <mi>e</mi> 
#   </mfenced> 
# </math>
#===============================================================================
        """
        math = Math()

        mfenced = MFenced()
        mfenced.opener = u'['
        mfenced.close = u']'
        mfenced.separators = "||||,"
        mi_1 = MathRun()
        mi_1.add(TextNode(u'a', type_text='math'))
        mfenced.add(mi_1)
        mi_2 = MathRun()
        mi_2.add(TextNode(u'b', type_text='math'))
        mfenced.add(mi_2)
        mi_3 = MathRun()
        mi_3.add(TextNode(u'c', type_text='math'))
        mfenced.add(mi_3)
        mi_4 = MathRun()
        mi_4.add(TextNode(u'd', type_text='math'))
        mfenced.add(mi_4)
        mi_5 = MathRun()
        mi_5.add(TextNode(u'e', type_text='math'))
        mfenced.add(mi_5)

        math.add(mfenced)
        output = render_output(math)
        assert_that(output, is_(u'\\[[a|b|c|d|e]\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\([a|b|c|d|e]\\)'))

    def test_math_mfenced_4(self):
        """
        example from : https://www.w3.org/TR/MathML3/chapter3.html
        when there is no open and close
#===============================================================================
# <mfenced>
#   <mrow>
#     <mi> a </mi>
#     <mo> + </mo>
#     <mi> b </mi>
#   </mrow>
# </mfenced>
#===============================================================================
        """
        math = Math()

        mfenced = MFenced()

        mrow = MRow()
        mi_1 = MathRun()
        mi_1.add(TextNode(u'a', type_text='math'))
        mrow.add(mi_1)

        mo = MathRun()
        mo.add(TextNode(u'+', type_text='math'))
        mrow.add(mo)

        mi_2 = MathRun()
        mi_2.add(TextNode(u'b', type_text='math'))
        mrow.add(mi_2)

        mfenced.add(mrow)
        math.add(mfenced)
        output = render_output(math)
        assert_that(output, is_(u'\\[(a+b)\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\((a+b)\\)'))

    def test_math_mfenced_5(self):
        """
        example from : https://www.w3.org/TR/MathML3/chapter3.html
        when there is no close
#===============================================================================
# <mfenced open="[">
#   <mn> 0 </mn>
#   <mn> 1 </mn>
# </mfenced>
#===============================================================================
        """
        math = Math()

        mfenced = MFenced()
        mfenced.opener = u'['

        mn_1 = MathRun()
        mn_1.add(TextNode(u'0', type_text='math'))
        mfenced.add(mn_1)

        mn_2 = MathRun()
        mn_2.add(TextNode(u'1', type_text='math'))
        mfenced.add(mn_2)

        math.add(mfenced)
        output = render_output(math)
        assert_that(output, is_(u'\\[[0,1)\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\([0,1)\\)'))

    def test_math_mfenced_6(self):
        """
        example from : https://www.w3.org/TR/MathML3/chapter3.html
        should be rendered as f(x,y)
#===============================================================================
# <mrow>
#   <mi> f </mi>
#   <mo> &#x2061;<!--FUNCTION APPLICATION--> </mo>
#   <mfenced>
#     <mi> x </mi>
#     <mi> y </mi>
#   </mfenced>
# </mrow>
#===============================================================================
        """
        math = Math()
        mrow = MRow()

        mi = MathRun()
        mi.add(TextNode(u'f', type_text='math'))
        mrow.add(mi)

        mo = MathRun()
        mo.element_type = u'operator'
        mo.add(TextNode(u'\u2061', type_text='math'))
        mrow.add(mo)

        mfenced = MFenced()
        mi_1 = MathRun()
        mi_1.add(TextNode(u'x', type_text='math'))
        mfenced.add(mi_1)
        mi_2 = MathRun()
        mi_2.add(TextNode(u'y', type_text='math'))
        mfenced.add(mi_2)
        mrow.add(mfenced)

        math.add(mrow)
        output = render_output(math)
        assert_that(output, is_(u'\\[f\\,(x,y)\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(f\\,(x,y)\\)'))

    def test_math_mmultiscripts_mprescripts(self):
        """
        example from : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mmultiscripts
#===============================================================================
# <math>  
# 
#     <mmultiscripts>
# 
#         <mi>X</mi>      <!-- base expression -->  
# 
#         <mi>d</mi>      <!-- postsubscript -->
#         <mi>c</mi>      <!-- postsuperscript -->
# 
#         <mprescripts />
#         <mi>b</mi>      <!-- presubscript -->
#         <mi>a</mi>      <!-- presuperscript -->
# 
#     </mmultiscripts>
# 
# </math>
#===============================================================================
        """
        math = Math()

        mmultiscripts = MMultiscripts()

        mi_1 = MathRun()
        mi_1.add(TextNode(u'X', type_text=u'math'))

        mi_2 = MathRun()
        mi_2.add(TextNode(u'd', type_text=u'math'))

        mi_3 = MathRun()
        mi_3.add(TextNode(u'c', type_text=u'math'))

        mmultiscripts.base = [mi_1, mi_2, mi_3]

        mmultiscripts.prescripts = MMprescripts()
        mi_4 = MathRun()
        mi_4.add(TextNode(u'b', type_text=u'math'))
        mmultiscripts.prescripts.sub = mi_4

        mi_5 = MathRun()
        mi_5.add(TextNode(u'a', type_text=u'math'))
        mmultiscripts.prescripts.sup = mi_5

        math.add(mmultiscripts)
        output = render_output(math)
        assert_that(output, is_(u'\\[{_{b}^{a}}X_{d}^{c}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\({_{b}^{a}}X_{d}^{c}\\)'))

    def test_math_mmultiscripts_mprescripts_2(self):
        """
        example from : https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mmultiscripts
#===============================================================================
# <math>  
# 
#     <mmultiscripts>
# 
#         <mi>X</mi>      <!-- base expression -->
# 
#         <none />        <!-- postsubscript -->
#         <mi>c</mi>      <!-- postsuperscript -->
# 
#         <mprescripts />
#         <mi>b</mi>      <!-- presubscript -->
#         <none />        <!-- presuperscript -->
# 
#     </mmultiscripts>
# 
# </math>
#===============================================================================
        """
        math = Math()

        mmultiscripts = MMultiscripts()

        mi_1 = MathRun()
        mi_1.add(TextNode(u'X', type_text=u'math'))

        mi_2 = MNone()

        mi_3 = MathRun()
        mi_3.add(TextNode(u'c', type_text=u'math'))

        mmultiscripts.base = [mi_1, mi_2, mi_3]

        mmultiscripts.prescripts = MMprescripts()
        mi_4 = MathRun()
        mi_4.add(TextNode(u'b', type_text=u'math'))
        mmultiscripts.prescripts.sub = mi_4

        mi_5 = MNone()
        mmultiscripts.prescripts.sup = mi_5

        math.add(mmultiscripts)
        output = render_output(math)
        assert_that(output, is_(u'\\[{_{b}^{}}X_{}^{c}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\({_{b}^{}}X_{}^{c}\\)'))

    def test_invisible_operator_1(self):
        """
        example from : https://www.w3.org/TR/MathML3/chapter3.html
#===============================================================================
# <mrow>
#   <mi> sin </mi>
#   <mo> &#x2061;<!--FUNCTION APPLICATION--> </mo>
#   <mi> x </mi>
# </mrow>
#===============================================================================
        """
        math = Math()
        mrow = MRow()

        mi_1 = MathRun()
        mi_1.add(TextNode(u'sin', type_text='math'))
        mrow.add(mi_1)

        mo = MathRun()
        mo.element_type = u'operator'
        mo.add(TextNode(u'\u2061', type_text='math'))
        mrow.add(mo)

        mi_2 = MathRun()
        mi_2.add(TextNode(u'x', type_text='math'))
        mrow.add(mi_2)

        math.add(mrow)
        output = render_output(math)
        assert_that(output, is_(u'\\[sin\\,x\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(sin\\,x\\)'))

    def test_invisible_operator_2(self):
        """
        example from : https://www.w3.org/TR/MathML3/chapter3.html
#===============================================================================
# <mrow>
#   <mi> x </mi>
#   <mo> &#x2062;<!--INVISIBLE TIMES--> </mo>
#   <mi> y </mi>
# </mrow>
#===============================================================================
        """
        math = Math()
        mrow = MRow()

        mi_1 = MathRun()
        mi_1.add(TextNode(u'x', type_text='math'))
        mrow.add(mi_1)

        mo = MathRun()
        mo.element_type = u'operator'
        mo.add(TextNode(u'\u2062', type_text='math'))
        mrow.add(mo)

        mi_2 = MathRun()
        mi_2.add(TextNode(u'y', type_text='math'))
        mrow.add(mi_2)

        math.add(mrow)
        output = render_output(math)
        assert_that(output, is_(u'\\[x\\,y\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(x\\,y\\)'))

    def test_invisible_operator_3(self):
        """
        example from : https://www.w3.org/TR/MathML3/chapter3.html
#===============================================================================
# <msub>
#   <mi> m </mi>
#   <mrow>
#     <mn> 1 </mn>
#     <mo> &#x2063;<!--INVISIBLE SEPARATOR--> </mo>
#     <mn> 2 </mn>
#   </mrow>
# </msub>
#===============================================================================
        """
        math = Math()
        msub = MSub()

        mi = MathRun()
        mi.add(TextNode(u'm', type_text='math'))
        msub.add(mi)

        mrow = MRow()

        mi_1 = MathRun()
        mi_1.add(TextNode(u'1', type_text='math'))
        mrow.add(mi_1)

        mo = MathRun()
        mo.element_type = u'operator'
        mo.add(TextNode(u'\u2063', type_text='math'))
        mrow.add(mo)

        mi_2 = MathRun()
        mi_2.add(TextNode(u'2', type_text='math'))
        mrow.add(mi_2)

        msub.add(mrow)
        math.add(msub)
        output = render_output(math)
        assert_that(output, is_(u'\\[{m}_{1\,2}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\({m}_{1\,2}\\)'))

    def test_invisible_operator_4(self):
        """
        example from : https://www.w3.org/TR/MathML3/chapter3.html
#===============================================================================
# <mrow>
#   <mn> 2 </mn>
#   <mo> &#x2064;<!--INVISIBLE PLUS--> </mo>
#   <mfrac>
#     <mn> 3 </mn>
#     <mn> 4 </mn>
#   </mfrac>
# </mrow>
#===============================================================================
        """
        math = Math()
        mrow = MRow()

        mn = MathRun()
        mn.add(TextNode(u'2', type_text='math'))
        mrow.add(mn)

        mo = MathRun()
        mo.element_type = u'operator'
        mo.add(TextNode(u'\u2064', type_text='math'))
        mrow.add(mo)

        mfrac = MFrac()

        mn_1 = MathRun()
        mn_1.add(TextNode(u'3', type_text='math'))
        mfrac.add(mn_1)

        mn_2 = MathRun()
        mn_2.add(TextNode(u'4', type_text='math'))
        mfrac.add(mn_2)

        mrow.add(mfrac)

        math.add(mrow)
        output = render_output(math)
        assert_that(output, is_(u'\\[2\\,\\frac{3}{4}\\]'))

        inline_math = math
        inline_math.equation_type = u'inline'
        output_inline = render_output(inline_math)
        assert_that(output_inline, is_(u'\\(2\\,\\frac{3}{4}\\)'))
    
    def test_text_embeeded_under_mo(self):
        """
        example : https://www.w3.org/TR/MathML3/chapter3.html#presm.mtext
#===============================================================================
# <mrow>
#   <mo> there exists </mo>
#   <mrow>
#     <mrow>
#       <mi> &#x3B4;<!--GREEK SMALL LETTER DELTA--> </mi>
#       <mo> &gt; </mo>
#       <mn> 0 </mn>
#     </mrow>
#     <mo> such that </mo>
#     <mrow>
#       <mrow>
#         <mi> f </mi>
#         <mo> &#x2061;<!--FUNCTION APPLICATION--> </mo>
#         <mrow>
#           <mo> ( </mo>
#           <mi> x </mi>
#           <mo> ) </mo>
#         </mrow>
#       </mrow>
#       <mo> &lt; </mo>
#       <mn> 1 </mn>
#     </mrow>
#   </mrow>
# </mrow>
#===============================================================================
        """
        math = Math()
        mrow = MRow()
        
        mo = MathRun()
        mo.element_type = u'operator'
        mo.add(TextNode(u'there exists', type_text=u'math'))
        mrow.add(mo)
        
        sub_mrow = MRow()
        mrow_1 = MRow()
        
        mi_1 = MathRun()
        mi_1.element_type = u'identifier'
        mi_1.add(TextNode(u"\u03B4", type_text=u'math'))
        mrow_1.add(mi_1)
        
        mo_1 = MathRun()
        mo_1.element_type = u'operator'
        mo_1.add(TextNode(u'>', type_text=u'math'))
        mrow_1.add(mo_1)
        
        mn_1 = MathRun()
        mn_1.element_type = u'numeric'
        mn_1.add(TextNode(u'0', type_text=u'math'))
        mrow_1.add(mn_1)
        sub_mrow.add(mrow_1)
        
        sub_mo = MathRun()
        sub_mo.element_type = u'operator'
        sub_mo.add(TextNode(u'such that', type_text=u'math'))
        sub_mrow.add(sub_mo)
        
        mrow_2 = MRow()
        
        sub_mrow_2 = MRow()
        sub_mi_2 = MathRun()
        sub_mi_2.element_type = u'identifier'
        sub_mi_2.add(TextNode(u"f", type_text=u'math'))
        sub_mrow_2.add(sub_mi_2)
        
        sub_mo_2 = MathRun()
        sub_mo_2.element_type = u'operator'
        sub_mo_2.add(TextNode(u"\u2061", type_text=u'math'))
        sub_mrow_2.add(sub_mo_2)
        
        sub_sub_mrow_2 = MRow()
        sub_sub_mo_2 = MathRun()
        sub_sub_mo_2.element_type = u'operator'
        sub_sub_mo_2.add(TextNode(u"(", type_text=u'math'))
        sub_sub_mrow_2.add(sub_sub_mo_2)
        
        sub_sub_mi_2 = MathRun()
        sub_sub_mi_2.element_type = u'identifier'
        sub_sub_mi_2.add(TextNode(u"x", type_text=u'math'))
        sub_sub_mrow_2.add(sub_sub_mi_2)
        
        sub_sub_mo_3 = MathRun()
        sub_sub_mo_3.element_type = u'operator'
        sub_sub_mo_3.add(TextNode(u")", type_text=u'math'))
        sub_sub_mrow_2.add(sub_sub_mo_3)
        
        sub_mrow_2.add(sub_sub_mrow_2)
        mrow_2.add(sub_mrow_2)
        
        mo_2 = MathRun()
        mo_2.element_type = u'operator'
        mo_2.add(TextNode(u'<', type_text=u'math'))
        mrow_2.add(mo_2)
        
        mn_2 = MathRun()
        mn_2.element_type = u'numeric'
        mn_2.add(TextNode(u'1', type_text=u'math'))
        mrow_2.add(mn_2)
        
        sub_mrow.add(mrow_2)
        mrow.add(sub_mrow)

        math.add(mrow)
        output = render_output(math)
        #assert_that(output, is_(u''))
        #TODO : something missed on the output
        #assert_that(output, is_(u'\\[\\exists \\delta 0\\ni f\\,x1\\]'))
    
    def test_mrow_mo(self):
        mrow_1 = MRow()
        mo_1 = MathRun()
        mo_1.element_type = u'operator'
        mo_1.add(TextNode(u'>', type_text=u'math'))
        mrow_1.add(mo_1)
        
        #TODO ega: why this test fail
        output = render_output(mrow_1)
        assert_that(output, is_(u'>'))