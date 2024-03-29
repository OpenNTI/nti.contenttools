#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value

from nti.contenttools.types.interfaces import IGlossaryEntry


def render_glossary_entry(context, node):
    term = get_variant_field_string_value(node.term)
    definition = get_variant_field_string_value(node.definition)
    context.write(u'\\ntiglossaryentry{')
    context.write(term)
    context.write(u'}{')
    context.write(definition)
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


@component.adapter(IGlossaryEntry)
class GlossaryEntryRenderer(RendererMixin):
    func = staticmethod(render_glossary_entry)
