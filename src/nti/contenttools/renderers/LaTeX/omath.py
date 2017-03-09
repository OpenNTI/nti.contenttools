#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools._compat import unicode_

from nti.contenttools.renderers.LaTeX.base import render_node
from nti.contenttools.renderers.LaTeX.base import render_output
from nti.contenttools.renderers.LaTeX.base import render_children
from nti.contenttools.renderers.LaTeX.base import render_iterable
from nti.contenttools.renderers.LaTeX.base import render_command

from nti.contenttools.renderers.LaTeX.utils import search_and_update_node_property
from nti.contenttools.renderers.LaTeX.utils import search_node

from nti.contenttools.unicode_to_latex import replace_unicode_with_latex_tag

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.omath import IOMath
from nti.contenttools.types.omath import IOMathMr
from nti.contenttools.types.omath import IOMathDPr
from nti.contenttools.types.omath import IOMathRun
from nti.contenttools.types.omath import IOMathSub
from nti.contenttools.types.omath import IOMathSup
from nti.contenttools.types.omath import IOMathBase
from nti.contenttools.types.omath import IOMathFrac
from nti.contenttools.types.omath import IOMathNary
from nti.contenttools.types.omath import IOMathPara
from nti.contenttools.types.omath import IOMathEqArr
from nti.contenttools.types.omath import IOMathDegree
from nti.contenttools.types.omath import IOMathNaryPr
from nti.contenttools.types.omath import IOMathMatrix
from nti.contenttools.types.omath import IOMathSubSup
from nti.contenttools.types.omath import IOMathRadical
from nti.contenttools.types.omath import IOMathDelimiter
from nti.contenttools.types.omath import IOMathNumerator
from nti.contenttools.types.omath import IOMathSubscript
from nti.contenttools.types.omath import IOMathSuperscript
from nti.contenttools.types.omath import IOMathDenominator
from nti.contenttools.types.omath import IOMathFunc
from nti.contenttools.types.omath import IOMathFName
from nti.contenttools.types.omath import IOMathLim
from nti.contenttools.types.omath import IOMathBar
from nti.contenttools.types.omath import IOMathLimLow
from nti.contenttools.types.omath import IOMathAcc


def render_omath(context, node):
    """
    render <m:OMath> element
    """
    context.write(u'$')
    render_children(context, node)
    context.write(u'$')
    return node


def render_omath_para(context, node):
    """
    render <m:OMathPara> element
    """
    context.write(u'$')
    render_children(context, node)
    context.write(u'$')
    return node


def render_omath_run(context, node):
    """
    to render <m:r> element
    """
    return render_children(context, node)


def render_omath_fraction(context, node):
    """
    render <m:f> element
    """
    if node.frac_type == u'lin':
        context.write(u'{')
        render_node(context, node.children[0])
        context.write(u'}/{')
        render_node(context, node.children[1])
        context.write(u'}')
    elif node.frac_type == u'skw':
        context.write(u'{^{')
        render_node(context, node.children[0])
        context.write(u'}}/_{')
        render_node(context, node.children[1])
        context.write(u'}')
    elif node.frac_type == u'noBar':
        context.write(u'{')
        render_node(context, node.children[0])
        context.write(u' \\choose ')
        render_node(context, node.children[1])
        context.write(u'}')
    else:
        context.write(u'\\frac{')
        render_node(context, node.children[0])
        context.write(u'}{')
        render_node(context, node.children[1])
        context.write(u'}')
    return node


def render_omath_numerator(context, node):
    """
    render <m:num>
    """
    return render_children(context, node)


def render_omath_denominator(context, node):
    """
    render <m:den>
    """
    return render_children(context, node)


def render_omath_radical(context, node):
    """
    render <m:rad> element
    """
    if len(node.children) == 1:
        context.write(u'\\sqrt{')
        render_node(context, node.children[0])
        context.write(u'}')
    elif len(node.children) == 2:
        context.write(u'\\sqrt[')
        render_node(context, node.children[0])
        context.write(u']{')
        render_node(context, node.children[1])
        context.write(u'}')
    return node


def render_omath_base(context, node):
    """
    render <m:e>
    """
    return render_children(context, node)


def render_omath_degree(context, node):
    """
    render <m:deg>
    """
    return render_children(context, node)


def render_omath_superscript(context, node):
    """
    render <m:sSup>
    """
    if len(node.children) == 2:
        context.write(u'{')
        render_node(context, node.children[0])
        context.write(u'}^{')
        render_node(context, node.children[1])
        context.write(u'}')
    else:
        logger.warn("<m:sSup> is not 2")
    return node


def render_omath_sup(context, node):
    """
    render <m:sup>
    """
    return render_children(context, node)


def render_omath_subscript(context, node):
    """
    render <m:sSub>
    """
    if len(node.children) == 2:
        context.write(u'{')
        render_node(context, node.children[0])
        context.write(u'}_{')
        render_node(context, node.children[1])
        context.write(u'}')
    else:
        logger.warn("<m:sSub> is not 2")
    return node


def render_omath_sub(context, node):
    """
    render <m:sub>
    """
    return render_children(context, node)


def render_omath_subsup(context, node):
    """
    render <m:sSubSup>
    """
    if len(node.children) == 3:
        context.write(u'{')
        render_node(context, node.children[0])
        context.write(u'}_{')
        render_node(context, node.children[1])
        context.write(u'}^{')
        render_node(context, node.children[2])
        context.write(u'}')
    else:
        logger.warn("<m:sSub> is not 3")
    return node


def render_omath_nary(context, node):
    """
    render <m:nary>
    """
    if node.children:
        token = render_output(node.children[0])
        if len(node.children) == 3:
            if u'\\sum' in token or u'\u2211' in unicode_(token):
                node = render_omath_nary_three_children(context, node, u'sum')
            elif u'\\prod' in token or u'\u220F' in unicode_(token):
                node = render_omath_nary_three_children(context, node, u'prod')
            elif u'\\int' in token or u'\u222B' in unicode_(token):
                node = render_omath_nary_three_children(context, node, u'int')
            else:
                logger.warn('Unhandled <m:nary> node with 3 children')
        elif len(node.children) == 4:
            if IOMathNaryPr.providedBy(node.children[0]):
                if node.children[0].chrVal:
                    node = render_omath_nary_four_children(
                        context, node, has_chrVal=True)
                else:
                    node = render_omath_nary_four_children(context, node)
            else:
                logger.warn(
                    '<m:nary> node has 4 children yet the first child does not provide IOMathNaryPr')
        else:
            logger.warn(
                u'The total number of <m:nary> node children is not 3 nor 4')
    else:
        logger.warn(u'<m:nary> node does not have children')

    return node


def render_omath_nary_three_children(context, node, nary_type):
    if nary_type == u'sum':
        context.write(u'\\sum')
    elif nary_type == u'prod':
        context.write(u'\\prod')
    elif nary_type == u'int':
        context.write(u'\\int')
    context.write(u'_{')
    render_node(context, node.children[1])
    context.write(u'}^{')
    render_node(context, node.children[2])
    context.write(u'}')
    return node


def render_omath_nary_four_children(context, node, has_chrVal=False):
    if has_chrVal:
        token = render_output(node.children[0]).rstrip()
        context.write(token)
    else:
        context.write(u'\\int')
    context.write(u'_{')
    render_node(context, node.children[1])
    context.write(u'}^{')
    render_node(context, node.children[2])
    context.write(u'} ')
    render_node(context, node.children[3])
    return node


def render_omath_nary_pr(context, node):
    """
    render <m:naryPr>
    """
    return render_children(context, node)


def render_omath_delimiter(context, node):
    """
    render <m:d>
    """
    if node.children:
        num_of_children = len(node.children)
        if IOMathDPr.providedBy(node.children[0]):
            if not node.children[0].begChr:
                found_frac_no_bar = search_node(IOMathFrac, node)
                if found_frac_no_bar:
                    render_iterable(context, node.children[1:num_of_children])
                else:
                    context.write(u'(')
                    render_iterable(context, node.children[1:num_of_children])
                    context.write(u')')
            elif node.children[0].begChr:
                field = {'begChr': node.children[0].begChr,
                         'endChr': node.children[0].endChr}
                found_matrix = search_and_update_node_property(IOMathMatrix, node, field)
                if found_matrix:
                    render_iterable(context, node.children[1:num_of_children])
                else:
                    field = {'begBorder': node.children[0].begChr,
                             'endBorder': node.children[0].endChr}
                    found_eq_arr = search_and_update_node_property(
                        IOMathEqArr,
                        node,
                        field)
                    if found_eq_arr:
                        render_iterable(context, node.children[1:num_of_children])
                    else:
                        begChr = replace_unicode_with_latex_tag(
                            node.children[0].begChr)
                        endChr = replace_unicode_with_latex_tag(
                            node.children[0].endChr)
                        context.write(begChr)
                        render_iterable(context, node.children[1:num_of_children])
                        context.write(endChr)
        else:
            render_children(context, node)
    return node


def render_omath_dpr(context, node):
    """
    render <m:dPr>
    """
    return render_children(context, node)


def render_omath_matrix(context, node):
    """
    render <m:m>
    """
    if node.begChr == '(':
        return render_matrix(context, node, u'pmatrix')
    elif node.begChr == '[':
        return render_matrix(context, node, u'bmatrix')
    else:
        return render_matrix(context, node, u'matrix')


def render_matrix(context, node, matrix_type):
    context.write(u'\\begin{')
    context.write(matrix_type)
    context.write(u'}\n')
    render_children(context, node)
    context.write(u'\\end{')
    context.write(matrix_type)
    context.write(u'}\n')
    return node


def render_omath_mr(context, node):
    """
    render <m:mr>
    """
    context.write(render_node_with_newline(node))
    return node


def render_node_with_newline(node):
    result = []
    for child in node.children:
        result.append(render_output(child))
    return u' & '.join(result) + u' \\\\\n'


def render_omath_eqarr(context, node):
    """
    render <m:eqArr>
    """
    if node.rowSpace == 1:
        if node.begBorder == u'{' and node.endBorder == u'':
            context.write(u'\\left \\{ ')
            render_array(context, node, u'lr')
            context.write(u' \\right.')
        elif node.begBorder == u'' and node.endBorder == u'}':
            context.write(u'\\left. ')
            render_array(context, node, u'lr')
            context.write(u' \\right \\}')
        elif not node.begBorder and not node.endBorder:
            render_array(context, node, u'lr')
        else:
            logger.warn('Unhandled equation array element render')
    else:
        number_of_space = int(node.rowSpace)
        string_col = u''
        for unused in range(number_of_space):
            string_col = string_col + u' l '
        render_array(context, node, string_col)
    return node


def render_array(context, node, string_col):
    context.write(u'\\begin{array}')
    context.write(u'{')
    context.write(string_col)
    context.write(u'}\n')
    render_children(context, node)
    context.write(u'\n\\end{array}')
    return node


def render_omath_func(context, node):
    """
    render <m:func>
    """
    return render_children(context, node)


def render_omath_fname(context, node):
    """
    render <m:fName>
    """
    return render_children(context, node)


def render_omath_lim(context, node):
    """
    render <m:lim>
    """
    return render_children(context, node)


def render_omath_lim_low(context, node):
    """
    render <m:limlow>
    """
    if node.__parent__:
        if IOMathFName.providedBy(node.__parent__):
            context.write(u'\\')
            render_node(context, node.children[0])
            context.write(u'_{')
            children_num = len(node.children)
            render_iterable(context, node.children[1:children_num])
            context.write(u'}')
        else:
            render_underset(context, node)
    else:
        render_underset(context, node)
    return node


def render_underset(context, node):
    children_num = len(node.children)
    context.write(u'\\underset{')
    render_iterable(context, node.children[1:children_num])
    context.write(u'}{')
    render_node(context, node.children[0])
    context.write(u'}')
    return node


def render_omath_bar(context, node):
    """
    render <m:bar>
    """
    if node.pos == u'top':
        return render_command(context, u'overline', node)
    else:
        return render_command(context, u'underline', node)


def render_omath_acc(context, node):
    """
    render <m:acc>
    """
    if node.accChr:
        accChr = node.accChr
        if accChr == u'\u0300':
            render_command(context, u'grave', node)
        elif accChr == u'\u0301':
            render_command(context, u'acute', node)
        elif accChr == u'\u0302':
            render_command(context, u'hat', node)
        elif accChr == u'\u0303':
            render_command(context, u'tilde', node)
        elif accChr == u'\u0304':
            render_command(context, u'bar', node)
        elif accChr == u'\u0306':
            render_command(context, u'breve', node)
        elif accChr == u'\u0307':
            render_command(context, u'dot', node)
        elif accChr == u'\u0308':
            render_command(context, u'ddot', node)
        elif accChr == u'\u030C':
            render_command(context, u'check', node)
        elif accChr == u'\u2190' or accChr == u'\u20d6':
            render_command(context, u'overleftarrow', node)
        elif accChr == u'\u2192' or accChr == u'\u20d7':
            render_command(context, u'overrightarrow', node)
        elif accChr == u'\u20e1':
            render_command(context, u'overleftrightarrow', node)
        elif accChr == u'\u20d0':
            context.write(u'\\overset{\\leftharpoonup}{')
            render_children(context, node)
            context.write(u'}')
        elif accChr == u'\u20d1':
            context.write(u'\\overset{\\rightharpoonup}{')
            render_children(context, node)
            context.write(u'}')
        elif accChr == u'\u0305':
            render_command(context, u'overline', node)
        else:
            logger.warn('Unhandled accent unicode render')

    else:
        render_command(context, u'hat', node)
    return node


@interface.implementer(IRenderer)
class RendererMixin(object):

    func = None

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None):
        node = self.node if node is None else node
        return self.func(context, node)
    __call__ = render


@component.adapter(IOMath)
class OMathRenderer(RendererMixin):
    func = staticmethod(render_omath)


@component.adapter(IOMathPara)
class OMathParaRenderer(RendererMixin):
    func = staticmethod(render_omath_para)


@component.adapter(IOMathRun)
class OMathRunRenderer(RendererMixin):
    func = staticmethod(render_omath_run)


@component.adapter(IOMathFrac)
class OMathFracRenderer(RendererMixin):
    func = staticmethod(render_omath_fraction)


@component.adapter(IOMathDenominator)
class OMathDenominatorRenderer(RendererMixin):
    func = staticmethod(render_omath_denominator)


@component.adapter(IOMathNumerator)
class OMathNumeratorRenderer(RendererMixin):
    func = staticmethod(render_omath_numerator)


@component.adapter(IOMathRadical)
class OMathRadicalRenderer(RendererMixin):
    func = staticmethod(render_omath_radical)


@component.adapter(IOMathBase)
class OMathBaseRenderer(RendererMixin):
    func = staticmethod(render_omath_base)


@component.adapter(IOMathDegree)
class OMathDegreeRenderer(RendererMixin):
    func = staticmethod(render_omath_degree)


@component.adapter(IOMathSubscript)
class OMathSubscriptRenderer(RendererMixin):
    func = staticmethod(render_omath_subscript)


@component.adapter(IOMathSuperscript)
class OMathSuperscriptRenderer(RendererMixin):
    func = staticmethod(render_omath_superscript)


@component.adapter(IOMathSub)
class OMathSubRenderer(RendererMixin):
    func = staticmethod(render_omath_sub)


@component.adapter(IOMathSup)
class OMathSupRenderer(RendererMixin):
    func = staticmethod(render_omath_sup)


@component.adapter(IOMathSubSup)
class OMathSubSupRenderer(RendererMixin):
    func = staticmethod(render_omath_subsup)


@component.adapter(IOMathNary)
class OMathNaryRenderer(RendererMixin):
    func = staticmethod(render_omath_nary)


@component.adapter(IOMathNaryPr)
class OMathNaryPrRenderer(RendererMixin):
    func = staticmethod(render_omath_nary_pr)


@component.adapter(IOMathDelimiter)
class OMathDelimiterRenderer(RendererMixin):
    func = staticmethod(render_omath_delimiter)


@component.adapter(IOMathDPr)
class OMathDPrRenderer(RendererMixin):
    func = staticmethod(render_omath_dpr)


@component.adapter(IOMathMatrix)
class OMathMatrixRenderer(RendererMixin):
    func = staticmethod(render_omath_matrix)


@component.adapter(IOMathMr)
class OMathMrRenderer(RendererMixin):
    func = staticmethod(render_omath_mr)


@component.adapter(IOMathEqArr)
class OMathEqArrRenderer(RendererMixin):
    func = staticmethod(render_omath_eqarr)


@component.adapter(IOMathFunc)
class OMathFuncRenderer(RendererMixin):
    func = staticmethod(render_omath_func)


@component.adapter(IOMathFName)
class OMathFNameRenderer(RendererMixin):
    func = staticmethod(render_omath_fname)


@component.adapter(IOMathLimLow)
class OMathLimLowRenderer(RendererMixin):
    func = staticmethod(render_omath_lim_low)


@component.adapter(IOMathLim)
class OMathLimRenderer(RendererMixin):
    func = staticmethod(render_omath_lim)


@component.adapter(IOMathBar)
class OMathBarRenderer(RendererMixin):
    func = staticmethod(render_omath_bar)


@component.adapter(IOMathAcc)
class OMathAccRenderer(RendererMixin):
    func = staticmethod(render_omath_acc)
