#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_node
from nti.contenttools.renderers.LaTeX.base import render_children_output

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import IFootnote
from nti.contenttools.types.interfaces import IFootnoteText
from nti.contenttools.types.interfaces import IFootnoteMark

from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value

def render_footnote(context, node):
    base = render_children_output(node)
    if base:
        context.write(u'\\footnote{')
        if node.label:
            label = get_variant_field_string_value(node.label).rstrip()
            context.write(u'\\label{')
            context.write(label)
            context.write(u'}')
        context.write(base)
        context.write(u'}')
    return node


def render_footnote_mark(context, node):
    if node.num:
        context.write(u'\\footnotemark[')
        context.write(node.num)
        context.write(u']')
    else:
        context.write(u'\\footnotemark')
    return node


def render_footnote_text(context, node):
    context.write(u'\\footnotetext')
    if node.num:
        context.write(u'[')
        context.write(node.num)
        context.write(u']')
    context.write(u'{')
    if node.text:
        if isinstance(node.text, six.string_types):
            context.write(node.text)
        else:
            render_node(context, node.text)
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


@component.adapter(IFootnote)
class FootnoteRenderer(RendererMixin):
    func = staticmethod(render_footnote)


@component.adapter(IFootnoteMark)
class FootnoteMarkRenderer(RendererMixin):
    func = staticmethod(render_footnote_mark)


@component.adapter(IFootnoteText)
class FootnoteTextRenderer(RendererMixin):
    func = staticmethod(render_footnote_text)
