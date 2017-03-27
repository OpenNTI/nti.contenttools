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

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.renderers.LaTeX.base import render_node
from nti.contenttools.renderers.LaTeX.base import render_children

from nti.contenttools.types.interfaces import IDocxTRow
from nti.contenttools.types.interfaces import IDocxTCell
from nti.contenttools.types.interfaces import IDocxTable


def render_docx_table(context, node):
    context.write(u'\\begin{table}\n\\begin{tabular}{')
    colspec = get_colspec(node)
    context.write(colspec)
    context.write(u'}\n')
    node = get_table_body(context, node)
    context.write(u'\\end{tabular}\n\\end{table}\n')
    return node


def get_colspec(node):
    colspec = u''
    if      'start' in node.borders \
        and node.borders['start']['val'] not in ['nil', 'none']:
        colspec = u'|'
    elif    'left' in node.borders \
        and node.borders['left']['val'] not in ['nil', 'none']:
        colspec = u'|'

    alignment = get_alignment(node)
    for _ in xrange(len(node.grid) - 1):
        colspec = colspec + alignment
        if      'insideV' in node.borders \
            and node.borders['insideV']['val'] not in ['nil', 'none']:
            colspec = colspec + u'|'

    if     'end' in node.borders \
        and node.borders['end']['val'] not in ['nil', 'none']:
        colspec = colspec + alignment + u'|'
    elif    'right' in node.borders \
        and node.borders['right']['val'] not in ['nil', 'none']:
        colspec = colspec + alignment + u'|'
    else:
        colspec = colspec + alignment

    return colspec


def get_alignment(node):
    alignment = u''
    if node.alignment in ['center']:
        alignment = u' c '
    elif node.alignment in ['left']:
        alignment = u' l '
    elif node.alignment in ['right']:
        alignment = u' r '
    elif node.alignment is None:
        alignment = u' l '
    else:
        logger.warn('Unhandled alignment type : %s', node.alignment)
    return alignment


def get_table_body(context, node):
    if      'top' in node.borders \
        and node.borders['top']['val'] not in ['nil', 'none']:
        context.write(u'\\hline\n')

    for child in node.children:
        render_node(context, child)
        if      'insideH' in node.borders \
            and node.borders['insideH']['val'] not in ['nil', 'none']:
            context.write(u'\\hline\n')

    if      'bottom' in node.borders \
        and node.borders['bottom']['val'] not in ['nil', 'none']:
        context.write(u'\\hline\n')

    return node


def render_docx_trow(context, node):
    check = len(node.children) - 1
    for index, child in enumerate(node.children):
        render_node(context, child)
        if index < check:
            context.write(u' & ')
    context.write(u'\\\\\n')
    return node


def render_docx_tcell(context, node):
    if node.grid_span > 1:
        context.write(u'\\multicolumn{')
        context.write(node.grid_span)
        context.write(u'}{c}{')
        render_children(context, node)
        context.write(u'}')
    else:
        render_children(context, node)
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


@component.adapter(IDocxTable)
class DocxTableRenderer(RendererMixin):
    func = staticmethod(render_docx_table)


@component.adapter(IDocxTRow)
class DocxTRowRenderer(RendererMixin):
    func = staticmethod(render_docx_trow)


@component.adapter(IDocxTCell)
class DocxTCellRenderer(RendererMixin):
    func = staticmethod(render_docx_tcell)
