from .base import base_renderer

def table_renderer(self):
    caption = u''
    colspec = u''
    if 'start' in self.borders.keys() and self.borders['start']['val'] not in ['nil', 'none']:
        colspec = u'|'
    elif 'left' in self.borders.keys() and self.borders['left']['val'] not in ['nil', 'none']:
        colspec = u'|'

    for i in xrange(len(self.grid)-1):
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

