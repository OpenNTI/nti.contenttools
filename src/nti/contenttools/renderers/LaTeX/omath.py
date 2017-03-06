#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: omath.py 107717 2017-03-01 10:26:58Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_node
from nti.contenttools.renderers.LaTeX.base import render_command
from nti.contenttools.renderers.LaTeX.base import render_output
from nti.contenttools.renderers.LaTeX.base import render_children
from nti.contenttools.renderers.LaTeX.base import render_children_output

from nti.contenttools.types.omath import IOMath
from nti.contenttools.types.omath import IOMathRun
from nti.contenttools.types.omath import IOMathPara
from nti.contenttools.types.omath import IOMathFrac
from nti.contenttools.types.omath import IOMathDenominator
from nti.contenttools.types.omath import IOMathNumerator
from nti.contenttools.types.omath import IOMathRadical
from nti.contenttools.types.omath import IOMathBase
from nti.contenttools.types.omath import IOMathDegree

from nti.contenttools.renderers.interfaces import IRenderer

def render_omath(context, node):
    """
    render <m:OMath> element
    """
    global begMatrixBorder 
    global endMatrixBorder
    begMatrixBorder = None
    endMatrixBorder = None

    global begEqArrBorder
    global endEqArrBorder
    begEqArrBorder = None
    endEqArrBorder = None
    
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
    to render <m:e>
    """
    return render_children(context, node)

def render_omath_degree(context, node):
    """
    to render <m:deg>
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
