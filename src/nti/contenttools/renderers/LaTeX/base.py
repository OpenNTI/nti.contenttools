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
    logger.debug(node)
    logger.debug(context)
    logger.debug(context.name)
    renderer = component.getAdapter(node,
                                    IRenderer,
                                    name=context.name)
    return renderer.render(context, node)


def render_iterable(context, iterable):
    for node in iterable or ():
        render_node(context, node)
    return context


def render_children(context, node):
    render_iterable(context, node.children or ())
    return node
base_renderer = render_children  # alias


def render_command(context, command, node, optional=u''):
    optional = optional or u''
    optional = u'[%s]' % optional if optional else optional
    context.write(u'\\%s%s{' % (command, optional))
    render_children(context, node)
    context.write('}')
    return node


def render_environment(context, element, node, optional=''):
    context.write(u'\\begin{%s}%s\n' % (element, optional or u''))
    render_children(context, node)
    context.write(u'\n\\end{%s}\n' % element)
    return node


def render_verbatim(context, node):
    if node.children:
        context.write(u'\begin{verbatim}\n')
        render_children(context, node)
        context.write(u'\n\\end{verbatim}\n')
    return node


def render_output(node):
    result = DefaultRendererContext(name="LaTeX")
    render_node(result, node)
    return result.read()


def render_children_output(node):
    result = DefaultRendererContext(name="LaTeX")
    render_children(result, node)
    return result.read()


def render_node_with_newline(node):
    result = []
    for child in node.children or ():
        result.append(render_output(child))
    return u' & '.join(result) + u' \\\\\n'
