#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer

from IPython.core.debugger import Tracer

def table_renderer(self):
    caption = u''
    colspec = u''
    if 'start' in self.borders.keys() and self.borders['start']['val'] not in ['nil', 'none']:
        colspec = u'|'
    elif 'left' in self.borders.keys() and self.borders['left']['val'] not in ['nil', 'none']:
        colspec = u'|'

    for _ in xrange(len(self.grid)-1):
        colspec = colspec + u' c '
        if 'insideV' in self.borders.keys() and self.borders['insideV']['val'] not in ['nil', 'none']:
            colspec = colspec + u'|'
    if 'end' in self.borders.keys() and self.borders['end']['val'] not in ['nil', 'none']:
        colspec = colspec + u' c |'
    elif 'right' in self.borders.keys() and self.borders['right']['val'] not in ['nil', 'none']:
        colspec = colspec + u' c |'
    else:
        colspec = colspec + u' c '

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
    number_of_col = self.number_of_col
    count_col = 0
    string_col = u''
    border = self.border
    if border:
        string_col = u'|'
    while count_col < number_of_col:
        #by default we use 'l' as caption, however we can modify this code later
        if border:
            string_col = string_col + u' l |' 
        else:
            string_col = string_col = u' l '
        count_col = count_col + 1
    
    body = base_renderer(self)

    if self.label is not None and self.caption is not None:
        label = self.label
        caption = self.caption.render()
        #TODO: the text_label only works for openstax epub, we need to modify line 84-85 if we work on different publisher
        text_label = self.caption.children[0].render() + self.caption.children[1].children[0].render()
        caption = caption.replace(text_label, u'')
        result = u'\\begin{table}\n\\label{%s}\n\\caption {%s}\n\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\n\\newline '
        return result % (label, caption, string_col, body)
    elif self.label is not None and self.caption is None:
        label = self.label
        result = u'\\begin{table}\n\\label{%s}\n\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\n\\newline '
        return result % (label, string_col, body)
    elif self.label is None and self.caption is not None:
        caption = self.caption.render()
        result = u'\\begin{table}\n\\caption {%s}\n\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\n'
        return result % (caption, string_col, body)
    elif self.label is None and self.caption is None :
        result = u'\\begin{table}\n\\begin{tabular}{%s}\n%s\\end{tabular}\n\\end{table}\n'
        return result % (string_col, body)
        
def table_row_html_renderer(self):
    result = []
    for child in self.children:
        result.append(child.render())
    if self.border:
        return u' & '.join(result) + u'\\\\ \hline\n' 
    else :
        return u' & '.join(result) + u'\\\\\n'

def table_cell_html_renderer(self):
    result = base_renderer(self).rstrip()
    return result


def tbody_html_renderer(self):
    result = base_renderer(self)
    return result

def theader_html_renderer(self):
    result = u'\\hline %s \\hline\n'
    return result %(base_renderer(self))

def tfooter_html_renderer(self):
    result = base_renderer(self)
    return result
