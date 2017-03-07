#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from StdSuites.AppleScript_Suite import string
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.renderers.LaTeX.base import render_children
from nti.contenttools.renderers.LaTeX.base import render_children_output

from nti.contenttools.renderers.LaTeX.utils import create_label
from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value

from nti.contenttools.types.interfaces import IRow
from nti.contenttools.types.interfaces import ICell
from nti.contenttools.types.interfaces import ITBody
from nti.contenttools.types.interfaces import ITHead
from nti.contenttools.types.interfaces import ITFoot
from nti.contenttools.types.interfaces import ITable


def set_number_of_table_col(node):
    header_index = find_table_child(ITHead, node)
    if header_index is not None:
        ncol = node.children[header_index].number_of_col
        node.set_number_of_col_header(ncol)

    body_index = find_table_child(ITBody, node)
    if body_index is not None:
        ncol = node.children[body_index].number_of_col
        node.set_number_of_col_body(ncol)


def find_table_child(IType, me):
    list_ = me.children
    for index, child in enumerate(list_):
        if IType.providedBy(child):
            return index
    return None


def get_string_col(number_of_col, border):
    cols = []
    cols_append = cols.append

    if border and number_of_col > 0:
        cols_append(u'|')

    for unused in range(number_of_col):
        if border:
            cols_append(u'l|')
        else:
            cols_append(u' l ')

    return u''.join(cols)


def process_table_html(context, node, string_col):
    caption = u''
    if node.type_== u'simplelist':
        context.write(u'\n')
        render_children(context, node)
        context.write(u'\n')
    else:
        context.write(u'\n\\begin{table}\n')
        if node.caption:
            caption = get_variant_field_string_value(node.caption).rstrip()
            context.write(u'\\caption{')
            context.write(caption)
            context.write(u'}\n')
        
        if node.label:
            label = get_variant_field_string_value(node.caption).rstrip()
            if u'\\label{' in label:
                context.write(label)
            else:
                context.write(u'\\label{')
                context.write(label)
                context.write(u'}')
            context.write(u'\n')
        else:
            if caption:
                label = create_label('table', caption)
                context.write(label)
                context.write(u'\n')
            
        context.write(u'\\begin{tabular}{')
        context.write(string_col)
        context.write(u'}\n')
        render_children(context, node)
        context.write(u'\n')
        context.write(u'\\end{tabular}\n\\end{table}\n')
    return node

def render_html_table(context, node):
    set_number_of_table_col(node)
    number_of_col_header = node.number_of_col_header
    number_of_col_body = node.number_of_col_body
    border = node.border
    string_col = u''
    if number_of_col_header == 0 and number_of_col_body > 0:
        string_col = get_string_col(number_of_col_body, border)
    elif number_of_col_body == number_of_col_header:
        string_col = get_string_col(number_of_col_header, border)
    else:
        string_col = get_string_col(number_of_col_body, border)
    return process_table_html(context, node, string_col)
    
def render_html_table_row(context, node):
    result = []
    for child in node.children:
        result.append(child.render())
    if node.border:
        output = u' & '.join(result) + u'\\\\ \hline\n'
    elif node.type_ == u'simplelist':
        output = u''.join(result) + u'\\\\\n'
    else:
        output = u' & '.join(result) + u'\\\\\n'
    context.write(output)


def render_html_table_cell(context, node):
    result = render_children_output(node).rstrip()
    if result.find(u'&') > 0 and result.find(u'\\&') < 0:
        result = result.replace(u'&', u'\\&')
    if result.isspace() or result is None or result == u'':
        result = u' ~ '
    elif node.colspan > 1:
        result = get_multicolumn(
            node.colspan,
            node.border,
            node.is_first_cell_in_the_row,
            result)
    context.write(result)


def get_multicolumn(col_span, border, first_cell, cell_string):
    if border:
        if first_cell:
            result = u'\\multicolumn{%s}{|l|}{%s} ' % (col_span, cell_string)
        else:
            result = u'\\multicolumn{%s}{l|}{%s} ' % (col_span, cell_string)
    else:
        result = u'\\multicolumn{%s}{l}{%s} ' % (col_span, cell_string)
    return result


def render_html_tbody(context, node):
    context.write(u'\\hline\n')
    render_children(context, node)
    return node


def render_html_theader(context, node):
    parent = node.__parent__
    if parent:
        context.write(u'\\hline ')
        render_children(context, node)
        context.write(u' \\hline\n')
    return node


def render_html_tfooter(context, node):
    parent = node.__parent__
    if parent:
        context.write(u'\\hline ')
        render_children(context, node)
        context.write(u' \\hline\n')
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


@component.adapter(ITable)
class HTMLTableRenderer(RendererMixin):
    func = staticmethod(render_html_table)


@component.adapter(IRow)
class HTMLTableRowRenderer(RendererMixin):
    func = staticmethod(render_html_table_row)


@component.adapter(ICell)
class HTMLTableCellRenderer(RendererMixin):
    func = staticmethod(render_html_table_cell)


@component.adapter(ITHead)
class HMTLTHeaderRenderer(RendererMixin):
    func = staticmethod(render_html_theader)


@component.adapter(ITFoot)
class HMTLTFooterRenderer(RendererMixin):
    func = staticmethod(render_html_tfooter)


@component.adapter(ITBody)
class HMTLTBodyRenderer(RendererMixin):
    func = staticmethod(render_html_tbody)
