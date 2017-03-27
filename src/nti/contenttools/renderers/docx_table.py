#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)


from nti.contenttools.renderers.LaTeX.base import render_node


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
    if      'start' in node.borders.keys() \
        and node.borders['start']['val'] not in ['nil', 'none']:
        colspec = u'|'
    elif 'left' in node.borders.keys() \
            and node.borders['left']['val'] not in ['nil', 'none']:
        colspec = u'|'

    alignment = get_alignment(node)
    for _ in xrange(len(node.grid) - 1):
        colspec = colspec + alignment
        if      'insideV' in node.borders.keys() \
            and node.borders['insideV']['val'] not in ['nil', 'none']:
            colspec = colspec + u'|'
    if      'end' in node.borders.keys() \
        and node.borders['end']['val'] not in ['nil', 'none']:
        colspec = colspec + alignment + u'|'
    elif    'right' in node.borders.keys() \
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
    if      'top' in node.borders.keys() \
        and node.borders['top']['val'] not in ['nil', 'none']:
        context.write(u'\\hline\n')

    for child in node.children:
        render_node(context, child)
        if      'insideH' in node.borders.keys() \
            and node.borders['insideH']['val'] not in ['nil', 'none']:
            context.write(u'\\hline\n')

    if      'bottom' in node.borders.keys() \
        and node.borders['bottom']['val'] not in ['nil', 'none']:
        context.write(u'\\hline\n')

    return node
