#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: views.py 44701 2014-07-29 20:30:15Z carlos.sanchez $
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

def table_html_renderer(self):
    #logger.info(" self.number_of_col : %s",self.number_of_col)
    number_of_col = self.number_of_col
    count_col = 0
    string_col = u''
    while count_col < number_of_col:
        string_col = string_col + u' l '
        count_col = count_col + 1
    body = u''
    for child in self.children:
        body = body + child.render()
    result = u'\\begin{table}{%s}\n\\begin{tabular}\n%s\\end{tabular}\n\\end{table}\n'
    return result % (string_col, body)

def table_row_html_renderer(self):
    result = []
    for child in self.children:
        result.append(child.render())
    #Tracer()()
    return u' & '.join(result) + u'\\\\\n'

def table_cell_html_renderer(self):
    result = base_renderer(self)
    return result
