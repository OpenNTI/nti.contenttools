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
from nti.contenttools.types.math import MMultiscripts
from nti.contenttools.types.math import MMprescripts

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
        multiscript_node = MMultiscripts()
        multiscript_node.base = MathRun()
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
        multiscript_node.base = MathRun()
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
        assert_that(output_inline, is_(u'\\(\\frac{\\frac{a}{b}}{\\frac{c}{d}}\\)'))
    
    
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
        