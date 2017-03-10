#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: lists.py 107252 2017-02-23 04:34:29Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_environment
from nti.contenttools.renderers.LaTeX.base import render_command

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import ICode
from nti.contenttools.types.interfaces import ICodeLine
from nti.contenttools.types.interfaces import IVerbatim


def render_code_line(context, node):
    return render_command(context, u'texttt', node)


def render_verbatim(context, node):
    return render_environment(context, u'verbatim', node)    


def render_code_listings(context, node):
    return render_environment(context, u'lstlisting', node)  

@interface.implementer(IRenderer)
class RendererMixin(object):

    func = None

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None):
        node = self.node if node is None else node
        return self.func(context, node)
    __call__ = render


@component.adapter(ICode)
class CodeRenderer(RendererMixin):
    func = staticmethod(render_code_listings)

@component.adapter(ICodeLine)
class CodeLineRenderer(RendererMixin):
    func = staticmethod(render_code_line)
    
@component.adapter(IVerbatim)
class VerbatimRenderer(RendererMixin):
    func = staticmethod(render_verbatim)

