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

from nti.contenttools.renderers.LaTeX.base import render_children

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import IMath
from nti.contenttools.types.interfaces import IMRow
from nti.contenttools.types.interfaces import IMTable
from nti.contenttools.types.interfaces import IMathRun
from nti.contenttools.types.interfaces import IMFenced


"""
rendering MathML element
"""


def render_math_html(context, node):
    """
    render element <math>
    """
    if len(node.children) == 0:
        context.write(u'')
    elif node.equation_type == u'inline':
        context.write(u'\\(')
        render_children(context, node)
        context.write(u'\\)')
    else:
        context.write(u'\\[')
        render_children(context, node)
        context.write(u'\\]')
    return node


def render_mrow(context, node):
    return render_children(context, node)


def render_mfenced(context, node):
    """
    render element <mfenced>
    """
    if len(node.children) > 0:
        if IMTable.providedBy(node.children[0]):
            return set_matrix_border(context, node)
        elif IMRow.providedBy(node.children[0]):
            if node.children[0].children:
                if IMTable.providedBy(node.children[0].children[0]):
                    return set_matrix_border(context, node)
                else:
                    return set_mfenced_without_border(context, node)
            else:
                return set_mfenced_without_border(context, node)
        else:
            return set_mfenced_without_border(context, node)
    else:
        context.write(u'')
    return node


def set_matrix_border(context, node):
    if node.opener == u'[':
        context.write(u'\\begin{bmatrix}\n')
        render_children(context, node)
        context.write(u'\\end{bmatrix}\n')
    elif node.opener == u'(':
        context.write(u'\\begin{pmatrix}\n')
        render_children(context, node)
        context.write(u'\\end{pmatrix}\n')
    else:
        context.write(u'\\begin{matrix}\n')
        render_children(context, node)
        context.write(u'\\end{matrix}\n')
    return node


def set_mfenced_without_border(context, node):
    context.write(node.opener)
    render_children(context, node)
    context.write(node.close)
    return node


def render_math_run(context, node):
    """
    render MathRun node
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


@component.adapter(IMath)
class MathRenderer(RendererMixin):
    func = staticmethod(render_math_html)


@component.adapter(IMRow)
class MRowRenderer(RendererMixin):
    func = staticmethod(render_mrow)


@component.adapter(IMFenced)
class MFencedRenderer(RendererMixin):
    func = staticmethod(render_mfenced)


@component.adapter(IMathRun)
class MathRunRenderer(RendererMixin):
    func = staticmethod(render_math_run)
