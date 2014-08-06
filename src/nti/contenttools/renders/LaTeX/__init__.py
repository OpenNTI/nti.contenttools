#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: views.py 44701 2014-07-29 20:30:15Z carlos.sanchez $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os

from ... import types
from ...docx.table import Table
from ...tag_parser import NAQuestion, NAQuestionPart, NAQChoices, NAQChoice, NAQSolutions, NAQSolution, NAQHints, NAQHint
from .base import base_renderer
from .assessment import *
from .document import *
from .body import *
from .image import *
from .list import *
from .paragraph import *
from .run import *
from .sectioning import *
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
    elif self.type == 'Pageref':
        result = u'\\pageref{%s}' % self.target
    return result

def label_renderer(self):
    return u'\\label{%s}' % self.name

def sidebar_renderer(self):
    body = base_renderer(self)
    title = u''
    if self.title:
        title = u'%s' % base_renderer(self.title)
    return u'\\begin{sidebar}{%s}\n%s\\end{sidebar}\n' % (title, body)

def blockquote_renderer(self):
    body = base_renderer(self)
    return u'\\begin{quote}\n%s\\end{quote}\n' % body

def video_renderer(self):
    body = base_renderer(self)
    parameters = 'width=%spx,height=%spx' % (self.width, self.height)
    src = os.path.splitext( self.path )[0]
    s = (parameters, src, self.caption, self.thumbnail, body)
    t = u'\n\\begin{ntilocalvideo}\n\\ntiincludelocalvideo[%s]{%s}{%s}{%s}\n%s\n\\end{ntilocalvideo}\n'
    return t % s

types.Document.render = document_renderer
types.Body.render = body_renderer
types.Chapter.render = chapter_renderer
types.Section.render = section_renderer
types.SubSection.render = subsection_renderer
types.SubSubSection.render = subsubsection_renderer
types.Paragraph.render = paragraph_renderer
types.Run.render = run_renderer
types.OrderedList.render = ordered_list_renderer
types.UnorderedList.render = list_renderer
types.List.render = list_renderer
types.Item.render = item_renderer
types.Note.render = note_renderer
types.Newline.render = newline_renderer
types.Hyperlink.render = hyperlink_renderer
types.Label.render = label_renderer
types.Sidebar.render = sidebar_renderer
types.BlockQuote.render = blockquote_renderer
Table.render = table_renderer
Table.Row.render = table_row_renderer
Table.Row.Cell.render = table_cell_renderer
types.Image.render = image_annotation_renderer
types.Video.render = video_renderer
NAQuestion.render = question_renderer
NAQuestionPart.render = question_part_renderer
NAQChoices.render = choices_renderer
NAQChoice.render = choice_renderer
NAQSolutions.render = solutions_renderer
NAQSolution.render = solution_renderer

types.Table =  table_renderer
types.Row = table_row_renderer
types.Cell = table_cell_renderer
