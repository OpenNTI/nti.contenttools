#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: footnote.py 107525 2017-02-27 09:43:34Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import IGlossaryEntry

from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value


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
