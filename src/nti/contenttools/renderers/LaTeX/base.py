#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.renderers.model import DefaultRendererContext


def render_node(context, node):
    renderer = component.getAdapter(node,
                                    IRenderer,
                                    name=context.name)
    return renderer.render(context, node)


def render_iterable(context, iterable):
    for node in iterable or ():
        render_node(context, node)


def render_children(context, node):
    render_iterable(context, node.children or ())
    return node


def render_output(node):
    result = DefaultRendererContext(name="LaTeX")
    render_node(result, node)
    return result.read()
base_renderer = render_children  # alias


def render_children_output(node):
    result = DefaultRendererContext(name="LaTeX")
    render_children(result, node)
    return result.read()
