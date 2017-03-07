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
from nti.contenttools.types.omath import OMathMr
from nti.contenttools.types.omath import OMathRun
from nti.contenttools.types.omath import OMathSub
from nti.contenttools.types.omath import OMathSup
from nti.contenttools.types.omath import OMathNary
from nti.contenttools.types.omath import OMathBase
from nti.contenttools.types.omath import OMathFrac
from nti.contenttools.types.omath import OMathPara
from nti.contenttools.types.omath import OMathEqArr
from nti.contenttools.types.omath import OMathNaryPr
from nti.contenttools.types.omath import OMathMatrix
from nti.contenttools.types.omath import OMathSubSup
from nti.contenttools.types.omath import OMathDegree
from nti.contenttools.types.omath import OMathRadical
from nti.contenttools.types.omath import OMathNumerator
from nti.contenttools.types.omath import OMathSubscript
from nti.contenttools.types.omath import OMathSuperscript
from nti.contenttools.types.omath import OMathDenominator

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

    def test_omath_numerator(self):
        node = OMathNumerator()
        text = TextNode(u'3', type_text='omath')
        node.add(text)
        output = render_output(node)
        assert_that(output, is_(u'3'))

    def test_omath_denominator(self):
        node = OMathDenominator()
        text = TextNode(u'4', type_text='omath')
        node.add(text)
        output = render_output(node)
        assert_that(output, is_(u'4'))

    def test_omath_fraction(self):
        numerator = OMathNumerator()
        num_child = TextNode(u'3', type_text='omath')
        numerator.add(num_child)

        denominator = OMathDenominator()
        den_child = TextNode(u'4', type_text='omath')
        denominator.add(den_child)

        frac = OMathFrac()
        frac.add(numerator)
        frac.add(denominator)

        output = render_output(frac)
        assert_that(output, is_(u'\\frac{3}{4}'))

    def test_omath_fraction_lin(self):
        numerator = OMathNumerator()
        num_child = TextNode(u'3', type_text='omath')
        numerator.add(num_child)

        denominator = OMathDenominator()
        den_child = TextNode(u'4', type_text='omath')
        denominator.add(den_child)

        frac = OMathFrac()
        frac.frac_type = u'lin'
        frac.add(numerator)
        frac.add(denominator)

        output = render_output(frac)
        assert_that(output, is_(u'{3}/{4}'))

    def test_omath_fraction_skw(self):
        numerator = OMathNumerator()
        num_child = TextNode(u'3', type_text='omath')
        numerator.add(num_child)

        denominator = OMathDenominator()
        den_child = TextNode(u'4', type_text='omath')
        denominator.add(den_child)

        frac = OMathFrac()
        frac.frac_type = u'skw'
        frac.add(numerator)
        frac.add(denominator)

        output = render_output(frac)
        assert_that(output, is_(u'{^{3}}/_{4}'))

    def test_omath_fraction_no_bar(self):
        numerator = OMathNumerator()
        num_child = TextNode(u'3', type_text='omath')
        numerator.add(num_child)

        denominator = OMathDenominator()
        den_child = TextNode(u'4', type_text='omath')
        denominator.add(den_child)

        frac = OMathFrac()
        frac.frac_type = u'noBar'
        frac.add(numerator)
        frac.add(denominator)

        output = render_output(frac)
        assert_that(output, is_(u'{3 \\choose 4}'))

    def test_omath_fraction_under_omath(self):
        omath = OMath()

        numerator = OMathNumerator()
        num_child = TextNode(u'3', type_text='omath')
        numerator.add(num_child)

        denominator = OMathDenominator()
        den_child = TextNode(u'4', type_text='omath')
        denominator.add(den_child)

        frac = OMathFrac()
        frac.add(numerator)
        frac.add(denominator)

        omath.add(frac)
        output = render_output(omath)
        assert_that(output, is_(u'$\\frac{3}{4}$'))

    def test_omath_fraction_under_omath_para(self):
        omath = OMath()
        omath_para = OMathPara()

        numerator = OMathNumerator()
        num_child = TextNode(u'3', type_text='omath')
        numerator.add(num_child)

        denominator = OMathDenominator()
        den_child = TextNode(u'4', type_text='omath')
        denominator.add(den_child)

        frac = OMathFrac()
        frac.add(numerator)
        frac.add(denominator)

        omath_para.add(frac)
        omath.add(omath_para)
        output = render_output(omath)
        assert_that(output, is_(u'$$\\frac{3}{4}$$'))

    def test_omath_base(self):
        node = OMathBase()
        text = TextNode(u'A', type_text='omath')
        node.add(text)
        output = render_output(node)
        assert_that(output, is_(u'A'))

    def test_omath_degree(self):
        node = OMathDegree()
        text = TextNode(u'b', type_text='omath')
        node.add(text)
        output = render_output(node)
        assert_that(output, is_(u'b'))

    def test_omath_radical_one_child(self):
        base = OMathBase()
        base_child = TextNode(u'A', type_text='omath')
        base.add(base_child)

        rad = OMathRadical()
        rad.add(base)

        output = render_output(rad)
        assert_that(output, is_(u'\\sqrt{A}'))

    def test_omath_radical_two_child(self):
        base = OMathBase()
        base_child = TextNode(u'A', type_text='omath')
        base.add(base_child)

        deg = OMathDegree()
        deg_child = TextNode(u'b', type_text='omath')
        deg.add(deg_child)

        rad = OMathRadical()
        rad.add(deg)
        rad.add(base)

        output = render_output(rad)
        assert_that(output, is_(u'\\sqrt[b]{A}'))

    def test_omath_radical_one_child_under_omath(self):
        omath = OMath()

        base = OMathBase()
        base_child = TextNode(u'A', type_text='omath')
        base.add(base_child)

        rad = OMathRadical()
        rad.add(base)

        omath.add(rad)
        output = render_output(omath)
        assert_that(output, is_(u'$\\sqrt{A}$'))

    def test_omath_radical_two_child_under_omath(self):
        omath = OMath()

        base = OMathBase()
        base_child = TextNode(u'A', type_text='omath')
        base.add(base_child)

        deg = OMathDegree()
        deg_child = TextNode(u'b', type_text='omath')
        deg.add(deg_child)

        rad = OMathRadical()
        rad.add(deg)
        rad.add(base)

        omath.add(rad)
        output = render_output(omath)
        assert_that(output, is_(u'$\\sqrt[b]{A}$'))

    def test_omath_radical_one_child_under_omath_para(self):
        omath = OMath()
        omath_para = OMathPara()

        base = OMathBase()
        base_child = TextNode(u'A', type_text='omath')
        base.add(base_child)

        rad = OMathRadical()
        rad.add(base)

        omath_para.add(rad)
        omath.add(omath_para)
        output = render_output(omath)
        assert_that(output, is_(u'$$\\sqrt{A}$$'))

    def test_omath_radical_two_child_under_omath_para(self):
        omath = OMath()
        omath_para = OMathPara()

        base = OMathBase()
        base_child = TextNode(u'A', type_text='omath')
        base.add(base_child)

        deg = OMathDegree()
        deg_child = TextNode(u'b', type_text='omath')
        deg.add(deg_child)

        rad = OMathRadical()
        rad.add(deg)
        rad.add(base)

        omath_para.add(rad)
        omath.add(omath_para)
        output = render_output(omath)
        assert_that(output, is_(u'$$\\sqrt[b]{A}$$'))

    def test_omath_sub(self):
        node = OMathSub()
        text = TextNode(u'1', type_text='omath')
        node.add(text)
        output = render_output(node)
        assert_that(output, is_(u'1'))

    def test_omath_sup(self):
        node = OMathSup()
        text = TextNode(u'2', type_text='omath')
        node.add(text)
        output = render_output(node)
        assert_that(output, is_(u'2'))

    def test_omath_superscript(self):
        base = OMathBase()
        base_child = TextNode(u'y', type_text='omath')
        base.add(base_child)

        sup = OMathSup()
        sup_child = TextNode(u'2', type_text='omath')
        sup.add(sup_child)

        superscript = OMathSuperscript()
        superscript.add(base)
        superscript.add(sup)

        output = render_output(superscript)
        assert_that(output, is_(u'{y}^{2}'))

    def test_omath_subscript(self):
        base = OMathBase()
        base_child = TextNode(u'x', type_text='omath')
        base.add(base_child)

        sub = OMathSub()
        sub_child = TextNode(u'2', type_text='omath')
        sub.add(sub_child)

        subscript = OMathSubscript()
        subscript.add(base)
        subscript.add(sub)

        output = render_output(subscript)
        assert_that(output, is_(u'{x}_{2}'))

    def test_omath_subsup(self):
        base = OMathBase()
        base_child = TextNode(u'x', type_text='omath')
        base.add(base_child)

        sup = OMathSup()
        sup_child = TextNode(u'2', type_text='omath')
        sup.add(sup_child)

        sub = OMathSub()
        sub_child = TextNode(u'1', type_text='omath')
        sub.add(sub_child)

        subsup = OMathSubSup()
        subsup.add(base)
        subsup.add(sub)
        subsup.add(sup)

        output = render_output(subsup)
        assert_that(output, is_(u'{x}_{1}^{2}'))

    def test_omath_superscript_under_omath(self):
        omath = OMath()

        base = OMathBase()
        base_child = TextNode(u'y', type_text='omath')
        base.add(base_child)

        sup = OMathSup()
        sup_child = TextNode(u'2', type_text='omath')
        sup.add(sup_child)

        superscript = OMathSuperscript()
        superscript.add(base)
        superscript.add(sup)

        omath.add(superscript)
        output = render_output(omath)
        assert_that(output, is_(u'${y}^{2}$'))

    def test_omath_subscript_under_omath(self):
        omath = OMath()

        base = OMathBase()
        base_child = TextNode(u'x', type_text='omath')
        base.add(base_child)

        sub = OMathSub()
        sub_child = TextNode(u'2', type_text='omath')
        sub.add(sub_child)

        subscript = OMathSubscript()
        subscript.add(base)
        subscript.add(sub)

        omath.add(subscript)
        output = render_output(omath)
        assert_that(output, is_(u'${x}_{2}$'))

    def test_omath_subsup_under_omath(self):
        omath = OMath()

        base = OMathBase()
        base_child = TextNode(u'x', type_text='omath')
        base.add(base_child)

        sup = OMathSup()
        sup_child = TextNode(u'2', type_text='omath')
        sup.add(sup_child)

        sub = OMathSub()
        sub_child = TextNode(u'1', type_text='omath')
        sub.add(sub_child)

        subsup = OMathSubSup()
        subsup.add(base)
        subsup.add(sub)
        subsup.add(sup)

        omath.add(subsup)
        output = render_output(omath)
        assert_that(output, is_(u'${x}_{1}^{2}$'))

    def test_omath_superscript_under_omath_para(self):
        omath = OMath()
        omath_para = OMathPara()

        base = OMathBase()
        base_child = TextNode(u'y', type_text='omath')
        base.add(base_child)

        sup = OMathSup()
        sup_child = TextNode(u'2', type_text='omath')
        sup.add(sup_child)

        superscript = OMathSuperscript()
        superscript.add(base)
        superscript.add(sup)

        omath_para.add(superscript)
        omath.add(omath_para)
        output = render_output(omath)
        assert_that(output, is_(u'$${y}^{2}$$'))

    def test_omath_subscript_under_omath_para(self):
        omath = OMath()
        omath_para = OMathPara()

        base = OMathBase()
        base_child = TextNode(u'x', type_text='omath')
        base.add(base_child)

        sub = OMathSub()
        sub_child = TextNode(u'2', type_text='omath')
        sub.add(sub_child)

        subscript = OMathSubscript()
        subscript.add(base)
        subscript.add(sub)

        omath_para.add(subscript)
        omath.add(omath_para)
        output = render_output(omath)
        assert_that(output, is_(u'$${x}_{2}$$'))

    def test_omath_subsup_under_omath_para(self):
        omath = OMath()
        omath_para = OMathPara()

        base = OMathBase()
        base_child = TextNode(u'x', type_text='omath')
        base.add(base_child)

        sup = OMathSup()
        sup_child = TextNode(u'2', type_text='omath')
        sup.add(sup_child)

        sub = OMathSub()
        sub_child = TextNode(u'1', type_text='omath')
        sub.add(sub_child)

        subsup = OMathSubSup()
        subsup.add(base)
        subsup.add(sub)
        subsup.add(sup)

        omath_para.add(subsup)
        omath.add(omath_para)
        output = render_output(omath)
        assert_that(output, is_(u'$${x}_{1}^{2}$$'))

    def test_omath_nary_pr(self):
        nary_pr = OMathNaryPr()
        text = TextNode(u'∑', type_text='omath')
        nary_pr.add(text)
        output = render_output(nary_pr)
        assert_that(output, is_(u'\\sum '))

    def test_omath_nary_three_children_sum(self):
        nary = OMathNary()

        nary_pr = OMathNaryPr()
        text = TextNode(u'∑', type_text='omath')
        nary_pr.add(text)
        nary.add(nary_pr)

        sub = OMathSub()
        sub_text = TextNode(u'i=1', type_text='omath')
        sub.add(sub_text)
        nary.add(sub)

        sup = OMathSup()
        sup_text = TextNode(u'20', type_text='omath')
        sup.add(sup_text)
        nary.add(sup)

        output = render_output(nary)
        assert_that(output, is_(u'\\sum_{i=1}^{20}'))

    def test_omath_nary_three_children_prod(self):
        nary = OMathNary()

        nary_pr = OMathNaryPr()
        text = TextNode(u'∏', type_text='omath')
        nary_pr.add(text)
        nary.add(nary_pr)

        sub = OMathSub()
        sub_text = TextNode(u'i=1', type_text='omath')
        sub.add(sub_text)
        nary.add(sub)

        sup = OMathSup()
        sup_text = TextNode(u'20', type_text='omath')
        sup.add(sup_text)
        nary.add(sup)

        output = render_output(nary)
        assert_that(output, is_(u'\\prod_{i=1}^{20}'))

    def test_omath_nary_three_children_int(self):
        nary = OMathNary()

        nary_pr = OMathNaryPr()
        text = TextNode(u'∫', type_text='omath')
        nary_pr.add(text)
        nary.add(nary_pr)

        sub = OMathSub()
        sub_text = TextNode(u'i=1', type_text='omath')
        sub.add(sub_text)
        nary.add(sub)

        sup = OMathSup()
        sup_text = TextNode(u'20', type_text='omath')
        sup.add(sup_text)
        nary.add(sup)

        output = render_output(nary)
        assert_that(output, is_(u'\\int_{i=1}^{20}'))

    def test_omath_nary_four_children_sum(self):
        nary = OMathNary()

        nary_pr = OMathNaryPr()
        text = TextNode(u'∑', type_text='omath')
        nary_pr.chrVal = u'∑'
        nary_pr.add(text)
        nary.add(nary_pr)

        sub = OMathSub()
        sub_text = TextNode(u'1', type_text='omath')
        sub.add(sub_text)
        nary.add(sub)

        sup = OMathSup()
        sup_text = TextNode(u'20', type_text='omath')
        sup.add(sup_text)
        nary.add(sup)

        base = OMathBase()
        base_text = TextNode(u'x', type_text='omath')
        base.add(base_text)
        nary.add(base)

        output = render_output(nary)
        assert_that(output, is_(u'\\sum_{1}^{20} x'))

    def test_omath_nary_four_children_int(self):
        nary = OMathNary()

        nary_pr = OMathNaryPr()
        text = TextNode(u'\8747', type_text='omath')
        nary_pr.limLocVal = u'\8747'
        nary_pr.add(text)
        nary.add(nary_pr)

        sub = OMathSub()
        sub_text = TextNode(u'1', type_text='omath')
        sub.add(sub_text)
        nary.add(sub)

        sup = OMathSup()
        sup_text = TextNode(u'20', type_text='omath')
        sup.add(sup_text)
        nary.add(sup)

        base = OMathBase()
        base_text = TextNode(u'x', type_text='omath')
        base.add(base_text)
        nary.add(base)

        output = render_output(nary)
        assert_that(output, is_(u'\\int_{1}^{20} x'))

    def test_omath_nary_four_children_token_int(self):
        nary = OMathNary()

        nary_pr = OMathNaryPr()
        text = TextNode(u'∫', type_text='omath')
        nary_pr.chrVal = u'∫'
        nary_pr.add(text)
        nary.add(nary_pr)

        sub = OMathSub()
        sub_text = TextNode(u'1', type_text='omath')
        sub.add(sub_text)
        nary.add(sub)

        sup = OMathSup()
        sup_text = TextNode(u'n', type_text='omath')
        sup.add(sup_text)
        nary.add(sup)

        base = OMathBase()
        base_text = TextNode(u'y', type_text='omath')
        base.add(base_text)
        nary.add(base)

        output = render_output(nary)
        assert_that(output, is_(u'\\int_{1}^{n} y'))

    def test_omath_basic_matrix(self):
        matrix = OMathMatrix()
        output = render_output(matrix)
        assert_that(output, is_(u'\\begin{matrix}\n\\end{matrix}\n'))

    def test_omath_basic_matrix_with_row_one_cell(self):
        matrix = OMathMatrix()

        mr_1 = OMathMr()
        base_1_1 = OMathBase()
        base_1_1.add(TextNode(u'A'))
        mr_1.add(base_1_1)

        mr_2 = OMathMr()
        base_2_1 = OMathBase()
        base_2_1.add(TextNode(u'C'))
        mr_2.add(base_2_1)

        matrix.add(mr_1)
        matrix.add(mr_2)

        output = render_output(matrix)
        assert_that(output, 
                    is_('\\begin{matrix}\nA \\\\\nC \\\\\n\\end{matrix}\n'))

    def test_omath_basic_matrix_with_row_cell(self):
        matrix = OMathMatrix()

        mr_1 = OMathMr()
        base_1_1 = OMathBase()
        base_1_1.add(TextNode(u'A'))
        base_1_2 = OMathBase()
        base_1_2.add(TextNode(u'B'))
        mr_1.add(base_1_1)
        mr_1.add(base_1_2)

        mr_2 = OMathMr()
        base_2_1 = OMathBase()
        base_2_1.add(TextNode(u'C'))
        base_2_2 = OMathBase()
        base_2_2.add(TextNode(u'D'))
        mr_2.add(base_2_1)
        mr_2.add(base_2_2)

        matrix.add(mr_1)
        matrix.add(mr_2)

        output = render_output(matrix)
        assert_that(output,
                    is_('\\begin{matrix}\nA & B \\\\\nC & D \\\\\n\\end{matrix}\n'))

    def test_omath_pmatrix(self):
        matrix = OMathMatrix()
        matrix.begChr = u'('
        output = render_output(matrix)
        assert_that(output, is_(u'\\begin{pmatrix}\n\\end{pmatrix}\n'))

    def test_omath_pmatrix_with_row_cell(self):
        matrix = OMathMatrix()
        matrix.begChr = u'('

        mr_1 = OMathMr()
        base_1_1 = OMathBase()
        base_1_1.add(TextNode(u'A'))
        base_1_2 = OMathBase()
        base_1_2.add(TextNode(u'B'))
        mr_1.add(base_1_1)
        mr_1.add(base_1_2)

        mr_2 = OMathMr()
        base_2_1 = OMathBase()
        base_2_1.add(TextNode(u'C'))
        base_2_2 = OMathBase()
        base_2_2.add(TextNode(u'D'))
        mr_2.add(base_2_1)
        mr_2.add(base_2_2)

        matrix.add(mr_1)
        matrix.add(mr_2)

        output = render_output(matrix)
        assert_that(output,
                    is_('\\begin{pmatrix}\nA & B \\\\\nC & D \\\\\n\\end{pmatrix}\n'))

    def test_omath_bmatrix(self):
        matrix = OMathMatrix()
        matrix.begChr = u'['
        output = render_output(matrix)
        assert_that(output, is_(u'\\begin{bmatrix}\n\\end{bmatrix}\n'))

    def test_omath_bmatrix_with_row_cell(self):
        matrix = OMathMatrix()
        matrix.begChr = u'['

        mr_1 = OMathMr()
        base_1_1 = OMathBase()
        base_1_1.add(TextNode(u'A'))
        base_1_2 = OMathBase()
        base_1_2.add(TextNode(u'B'))
        mr_1.add(base_1_1)
        mr_1.add(base_1_2)

        mr_2 = OMathMr()
        base_2_1 = OMathBase()
        base_2_1.add(TextNode(u'C'))
        base_2_2 = OMathBase()
        base_2_2.add(TextNode(u'D'))
        mr_2.add(base_2_1)
        mr_2.add(base_2_2)

        matrix.add(mr_1)
        matrix.add(mr_2)

        output = render_output(matrix)
        assert_that(output, 
                    is_('\\begin{bmatrix}\nA & B \\\\\nC & D \\\\\n\\end{bmatrix}\n'))

    def test_omath_basic_eq_array(self):
        eq_arr = OMathEqArr()
        output = render_output(eq_arr)
        assert_that(output, is_(u'\\begin{array}{lr}\n\n\\end{array}'))

    def test_omath_eq_array(self):
        eq_arr = OMathEqArr()
        base_1 = OMathBase()
        row_1 = OMathMr()
        row_1.add(TextNode(u'x_{1} + x_{2} = 4'))
        base_1.add(row_1)

        base_2 = OMathBase()
        row_2 = OMathMr()
        row_2.add(TextNode(u'x_{3} + x_{4} = 10'))
        base_2.add(row_2)
        
        eq_arr.add(base_1)
        eq_arr.add(base_2)
        output = render_output(eq_arr)

        assert_that(output, is_(u'\\begin{array}{lr}\nx_{1} + x_{2} = 4 \\\\\nx_{3} + x_{4} = 10 \\\\\n\n\\end{array}'))
    
    def test_omath_eq_array2(self):
        eq_arr = OMathEqArr()
        eq_arr.rowSpace = 2
        
        base_1 = OMathBase()
        row_1 = OMathMr()
        row_1.add(TextNode(u'x_{1} + x_{2} = 4'))
        row_1.add(TextNode(u'Y'))
        base_1.add(row_1)

        base_2 = OMathBase()
        row_2 = OMathMr()
        row_2.add(TextNode(u'x_{3} + x_{4} = 10'))
        row_2.add(TextNode(u'Z'))
        base_2.add(row_2)

        eq_arr.add(base_1)
        eq_arr.add(base_2)
        output = render_output(eq_arr)

        assert_that(output, is_(u'\\begin{array}{ l  l }\nx_{1} + x_{2} = 4 & Y \\\\\nx_{3} + x_{4} = 10 & Z \\\\\n\n\\end{array}'))
    