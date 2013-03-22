from ...docx.paragraph import Item, List, Paragraph, Run, OrderedList, UnorderedList, Note, Newline, Hyperlink, Image
from ...docx.table import Table
from .base import base_renderer
from .assessment import *
from .image import *
from .list import *
from .paragraph import *
from .run import *
from .table import *


def note_renderer(self):
    return u'\\footnote{%s}' % base_renderer(self)

def hyperlink_renderer(self):
    result = u''
    if self.type == 'Normal':
        result = u'\\href{%s}{%s}' % (self.target, base_renderer(self))
    elif self.type == 'YouTube':
        result = u'\\ntiincludevideo{%s}' % self.target
    elif self.type == 'Thumbnail':
        result = u'\\href{%s}{%s}' % (self.target, base_renderer(self))
    return result

Paragraph.render = paragraph_renderer
Run.render = run_renderer
OrderedList.render = ordered_list_renderer
UnorderedList.render = list_renderer
List.render = list_renderer
Item.render = item_renderer
Note.render = note_renderer
Newline.render = newline_renderer
Hyperlink.render = hyperlink_renderer
Table.render = table_renderer
Table.Row.render = table_row_renderer
Table.Row.Cell.render = table_cell_renderer
Image.render = image_annotation_renderer
