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

from nti.contenttools.renderers.LaTeX.base import render_node
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
