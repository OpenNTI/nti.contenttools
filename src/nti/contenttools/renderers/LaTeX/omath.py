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

from nti.contenttools.renderers.LaTeX.base import render_node, render_output
from nti.contenttools.renderers.LaTeX.base import render_children

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.omath import IOMath
from nti.contenttools.types.omath import IOMathRun
from nti.contenttools.types.omath import IOMathSub
from nti.contenttools.types.omath import IOMathSup
from nti.contenttools.types.omath import IOMathBase
from nti.contenttools.types.omath import IOMathFrac
from nti.contenttools.types.omath import IOMathPara
from nti.contenttools.types.omath import IOMathDegree
from nti.contenttools.types.omath import IOMathSubSup
from nti.contenttools.types.omath import IOMathRadical
from nti.contenttools.types.omath import IOMathNumerator
from nti.contenttools.types.omath import IOMathSubscript
from nti.contenttools.types.omath import IOMathSuperscript
from nti.contenttools.types.omath import IOMathDenominator
from nti.contenttools.types.omath import IOMathNary
from nti.contenttools.types.omath import IOMathNaryPr


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
    #example : equation_sample-6.docx, equation_sample-7.docx, 
    """
    if node.children:
        token = render_output(node.children[0])
        if len(node.children) == 3:
            if u'\\sum' in token or u'\u2211' in unicode(token):
                node = render_omath_nary_three_children(context, node, u'sum')
            elif u'\\prod' in token or u'\u220F' in unicode(token):
                node = render_omath_nary_three_children(context, node, u'prod')
            elif u'\\int' in token or u'\u222B' in unicode(token):
                node = render_omath_nary_three_children(context, node, u'int')
            else:
                logger.warn('Unhandled <m:nary> node with 3 children')
        elif len(node.children) == 4:
            if IOMathNaryPr.providedBy(node.children[0]):
                if node.children[0].chrVal:
                    node = render_omath_nary_four_children(context, node, has_chrVal=True)
                else:
                    node = render_omath_nary_four_children(context, node)
            else:
                logger.warn('<m:nary> node has 4 children yet the first child does not provide IOMathNaryPr')
        else:
            logger.warn(u'The total number of <m:nary> node children is not 3 nor 4')
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
        render_node(context, node.children[0])
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
