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

from nti.contenttools.types.interfaces import ITextBoxContent
from nti.contenttools.types.interfaces import IAlternateContent


def render_alternate_content(context, node):
    return render_children(context, node)


def render_text_box_content(context, node):
    context.write(u'\\parbox[c]{\\textwidth}{')
    render_children(context, node)
    context.write(u'}')
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


@component.adapter(IAlternateContent)
class AlternateContentRenderer(RendererMixin):
    func = staticmethod(render_alternate_content)


@component.adapter(ITextBoxContent)
class TextBoxContentRenderer(RendererMixin):
    func = staticmethod(render_text_box_content)
