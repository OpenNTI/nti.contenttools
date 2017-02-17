#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: list.py 65711 2015-05-20 21:08:17Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_children_output

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import IRow
from nti.contenttools.types.interfaces import ICell
from nti.contenttools.types.interfaces import ITBody
from nti.contenttools.types.interfaces import ITHead
from nti.contenttools.types.interfaces import ITFoot
from nti.contenttools.types.interfaces import ITable

from nti.contenttools.types.table import TBody
from nti.contenttools.types.table import THead

def set_number_of_table_col(node):
    header_index = find_table_child(THead, node)
    if header_index is not None:
        node.set_number_of_col_header(node.children[header_index].number_of_col)
    
    body_index = find_table_child(TBody, node)
    if body_index is not None:
        node.set_number_of_col_body(node.children[body_index].number_of_col)

def find_table_child(type_, me):
    list_ = me.children
    for index, child in enumerate(list_):
        if isinstance(child, type_):
            return index
    return None

def get_string_col(number_of_col,border):
    cols = []
    cols_append = cols.append

    if border and number_of_col > 0 : cols_append(u'|')

    for i in range (number_of_col):
        if border: cols_append(u'l|')
        else: cols_append(u' l ')

    return u''.join(cols)

def process_table_html(context, node, string_col):
    body = render_children_output(node)

    if node.label is not None and node.caption is not None:
        label = node.label
        caption = node.caption.render().rstrip()
        result = u'\n\\begin{table}\n\\caption {%s}\n\\label{%s}\n\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\\newline\n'
        return result % (caption, label, string_col, body)
    elif node.label is not None and node.caption is None:
        label = node.label
        result = u'\n\\begin{table}\n\\label{%s}\n\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\\newline\n'
        return result % (label, string_col, body,)
    elif node.label is None and node.caption is not None:
        caption = node.caption.render()
        #TODO: the text_label only works for openstax epub, we need to modify the following line
        text_label = node.caption.children[0].render() + node.caption.children[1].children[0].render()
        caption = caption.replace(text_label, u'')
        result = u'\n\\begin{table}\n\\caption {%s}\n\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\n'
        return result % (caption, string_col, body)
    elif node.label is None and node.caption is None and node.type_ is None:
        result = u'\n\\begin{table}\n\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\n'
        return result % (string_col, body)
    elif node.type_== u'simplelist':
        result = u'\n%s\n\\newline '
        return result %(body)

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
    result = process_table_html(context, node, string_col)
    context.write(result)

def render_html_table_row(context, node):
    result = []
    for child in node.children:
        result.append(child.render())
    if node.border:
        output =  u' & '.join(result) + u'\\\\ \hline\n' 
    elif node.type_ == u'simplelist':
        output =  u''.join(result) + u'\\\\\n'
    else :
        output = u' & '.join(result) + u'\\\\\n'
    context.write(output)

def render_html_table_cell(context, node):
    result = render_children_output(node).rstrip()
    if result.find(u'&') > 0 and result.find(u'\\&') < 0 : result = result.replace(u'&', u'\\&')
    if result.isspace() or result is None or result == u'':
        result = u' ~ '
    elif node.colspan > 1:
        result = get_multicolumn(node.colspan, node.border, node.is_first_cell_in_the_row, result)
    return result


def get_multicolumn(col_span, border, first_cell, cell_string):
    if border:
        if first_cell: result = u'\\multicolumn{%s}{|l|}{%s} ' %(col_span, cell_string)
        else: result = u'\\multicolumn{%s}{l|}{%s} ' %(col_span, cell_string)
    else: result = u'\\multicolumn{%s}{l}{%s} ' %(col_span, cell_string)        
    return result

def render_html_tbody(context, node):
    result = render_children_output(node)
    if node.border is not None:
        result =  u'\\hline\n%s' %(result)
    return result

def render_html_theader(context, node):
    result = u'\\hline %s \\hline\n' if node.__parent__.border else u'%s'
    base = render_children_output(node)
    return result %(base)

def render_html_tfooter(context, node):
    result = u'\\hline %s \\hline\n' if node.__parent__.border else u'%s'
    base = render_children_output(node)
    return result %(base)


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