#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer
from ... import types

from IPython.core.debugger import Tracer

def table_renderer(self):
    caption = u''
    colspec = u''
    if 'start' in self.borders.keys() and self.borders['start']['val'] not in ['nil', 'none']:
        colspec = u'|'
    elif 'left' in self.borders.keys() and self.borders['left']['val'] not in ['nil', 'none']:
        colspec = u'|'

    alignment = u''
    if self.alignment in ['center']:
        alignment = u' c '
    elif self.alignment in ['left']:
        alignment = u' l '
    elif self.alignment in ['right']:
        alignment = u' r '
    elif self.alignment is None:
        alignment = u' l '
    else:
        logger.warn('Unhandled alignment type : %s', self.alignment)

    for _ in xrange(len(self.grid)-1):
        colspec = colspec + alignment
        if 'insideV' in self.borders.keys() and self.borders['insideV']['val'] not in ['nil', 'none']:
            colspec = colspec + u'|'
    if 'end' in self.borders.keys() and self.borders['end']['val'] not in ['nil', 'none']:
        colspec = colspec + alignment + u'|'
    elif 'right' in self.borders.keys() and self.borders['right']['val'] not in ['nil', 'none']:
        colspec = colspec + alignment + u'|'
    else:
        colspec = colspec + alignment

    body = u''
    if 'top' in self.borders.keys() and self.borders['top']['val'] not in ['nil', 'none']:
        body = body + u'\\hline\n'
    for child in self.children:
        body = body + child.render()
        if 'insideH' in self.borders.keys() and self.borders['insideH']['val'] not in ['nil', 'none']:
            body = body + u'\\hline\n'
    if 'bottom' in self.borders.keys() and self.borders['bottom']['val'] not in ['nil', 'none']:
        body = body + u'\\hline\n'

    result = u'\\begin{table}\n%s\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\n'

    return result % (caption, colspec, body)

def table_row_renderer(self):
    result = []
    for child in self.children:
        result.append(child.render())

    return u' & '.join(result) + u'\\\\\n'

def table_cell_renderer(self):
    result = u''
    if self.grid_span > 1:
        result = u'\\multicolumn{%s}{c}{%s}' % ( self.grid_span, base_renderer(self) )
    else:
        result = base_renderer(self)
    return result

def basic_renderer(self):
    body = u''
    for child in self.children:
        body = body + child.render()
    return body

def table_html_renderer(self):
    set_number_of_table_col(self)
    number_of_col_header = self.number_of_col_header
    number_of_col_body = self.number_of_col_body
    border = self.border
    string_col = u''
    if number_of_col_header == 0 and number_of_col_body > 0:
        string_col = get_string_col(number_of_col_body, border)
    elif number_of_col_body == number_of_col_header:
        string_col = get_string_col(number_of_col_header, border)
    else:
        string_col = get_string_col(number_of_col_body, border)
    result = process_table_html(self, string_col)
    return result

def set_number_of_table_col(self):
    header_index = find_table_child(types.THead, self)
    if header_index is not None:
        self.set_number_of_col_header(self.children[header_index].number_of_col)
    
    body_index = find_table_child(types.TBody, self)
    if body_index is not None:
        self.set_number_of_col_body(self.children[body_index].number_of_col)

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

def process_table_html(self, string_col):
    body = base_renderer(self)

    if self.label is not None and self.caption is not None:
        label = self.label
        caption = self.caption.render().rstrip()
        #logger.info(caption)
        #TODO: the text_label only works for openstax epub, we need to modify line 136-137 if we work on different publisher
        text_label = self.caption.children[0].render() + self.caption.children[1].children[0].render().rstrip()
        #logger.info(text_label)
        caption = caption.replace(text_label, u' ')
        #logger.info(caption)
        result = u'\n\\begin{table}\n\\caption {%s}\n\\label{%s}\n\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\\newline\n'
        return result % (caption, label, string_col, body)
    elif self.label is not None and self.caption is None:
        label = self.label
        result = u'\n\\begin{table}\n\\label{%s}\n\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\\newline\n'
        return result % (label, string_col, body,)
    elif self.label is None and self.caption is not None:
        caption = self.caption.render()
        #logger.info(caption)
        #TODO: the text_label only works for openstax epub, we need to modify line 147-148 if we work on different publisher
        text_label = self.caption.children[0].render() + self.caption.children[1].children[0].render()
        #logger.info(text_label)
        caption = caption.replace(text_label, u'')
        #logger.info(caption)
        result = u'\n\\begin{table}\n\\caption {%s}\n\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\n'
        return result % (caption, string_col, body)
    elif self.label is None and self.caption is None and self.type_ is None:
        result = u'\n\\begin{table}\n\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\n'
        return result % (string_col, body)
    elif self.type_== u'simplelist':
        result = u'\n%s\n\\newline '
        return result %(body)

        
def table_row_html_renderer(self):
    result = []
    for child in self.children:
        result.append(child.render())
    if self.border:
        return u' & '.join(result) + u'\\\\ \hline\n' 
    elif self.type_ == u'simplelist':
        return u''.join(result) + u'\\\\\n'
    else :
        return u' & '.join(result) + u'\\\\\n'

def table_cell_html_renderer(self):
    result = base_renderer(self).rstrip()
    if result.find(u'&') > 0 and result.find(u'\\&') < 0 : result = result.replace(u'&', u'\\&')
    if result.isspace() or result is None or result == u'':
        result = u' ~ '
    elif self.colspan > 1:
        result = get_multicolumn(self.colspan, self.border, self.is_first_cell_in_the_row, result)

    return result

def get_multicolumn(col_span, border, first_cell, cell_string):
    if border:
        if first_cell: result = u'\\multicolumn{%s}{|l|}{%s} ' %(col_span, cell_string)
        else: result = u'\\multicolumn{%s}{l|}{%s} ' %(col_span, cell_string)
    else: result = u'\\multicolumn{%s}{l}{%s} ' %(col_span, cell_string)        
    return result

def tbody_html_renderer(self):
    result = base_renderer(self)
    if self.border is not None:
        result =  u'\\hline\n%s' %(result)
    return result

def theader_html_renderer(self):
    result = u'\\hline %s \\hline\n'
    return result %(base_renderer(self))

def tfooter_html_renderer(self):
    result = u'\\hline %s \\hline\n'
    return result %(base_renderer(self))