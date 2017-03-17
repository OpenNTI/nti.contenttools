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

from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import IHyperlink


def render_hyperlink(context, node):
    if not node.target:
        render_children(context, node)
    else:
        target = get_variant_field_string_value(node.target)
        target = target.replace(u'%', u'\\%')
        if node.type == u'Normal' or node.type == u'Thumbnail':
            context.write(u'\\href{')
            context.write(target)
            context.write(u'}{')
            render_children(context, node)
            context.write(u'}')
        elif node.type == u'Youtube':
            set_link(context, u'ntiincludevideo', target)
        elif node.type == u'Pageref':
            set_link(context, u'ntiidref', target)
    return node


def set_link(context, command, target):
    context.write(u'\\')
    context.write(command)
    context.write(u'{')
    context.write(target)
    context.write(u'}')


@component.adapter(IHyperlink)
@interface.implementer(IRenderer)
class HyperlinkRenderer(object):

    __slots__ = ('node',)

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None, *args, **kwargs):
        node = self.node if node is None else node
        return render_hyperlink(context, node)
    __call__ = render
