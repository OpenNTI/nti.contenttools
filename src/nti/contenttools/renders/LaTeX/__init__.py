#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
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
from .math import *
from .omath import*
from .code_line import*
from .alternate_content import*
from .note_interactive import*
from .chapter_assessment import *
from .glossary import *
from .note import *
from .equation_image import *
from ... util import string_replacer
from .footnote import *
from .cnx_alternate_content import *

def note_renderer(self):
    content = base_renderer(self)
    if len(content) > 0 : content = u'\\footnote{%s} ' % content
    return content

def hyperlink_renderer(self):
    result = u''
    if self.target is None : return base_renderer(self)
    target = string_replacer.modify_string(self.target, u'%', u'\\%')
    if self.type == 'Normal':
        result = u'\\href{%s}{%s} ' % (target, base_renderer(self))
    elif self.type == 'YouTube':
        result = u'\\ntiincludevideo{%s} ' % target
    elif self.type == 'Thumbnail':
        result = u'\\href{%s}{%s} ' % (target, base_renderer(self))
    elif self.type == 'Pageref':
        #result = u'\\pageref{%s} ' % self.target
        result = u'\\ntiidref{%s} ' % target
    return result

def label_renderer(self):
    return u'\\label{%s} ' % self.name

def sidebar_renderer(self):
    body = base_renderer(self)
    
    title = u''
    if isinstance(self.title, str) or isinstance(self.title, unicode): title = self.title.strip()
    elif self.title is None : pass
    else: title = u'%s' % base_renderer(self.title).strip() 

    label = u'\\label{%s}\n' % self.label if self.label else u''

    if any(chars in title for chars in [u'\\(', u'\\[' ]):
        logger.warn("Math element found in sidebar's title. It may cause TROUBLE with nti_render, therefore no title for this sidebar. Use textbf to write title in sidebar body")
        return u'\n\\begin{sidebar}%s\n\\textbf{%s}\n%s\n\\end{sidebar}\n' % (label,title,body)
    
    return u'\n\\begin{sidebar}{%s}\n%s%s\n\\end{sidebar}\n' % (title, label,body)

def blockquote_renderer(self):
    body = base_renderer(self)
    return u'\n\\begin{quote}\n%s\n\\end{quote}\n' % body

def video_renderer(self):
    body = base_renderer(self)
    parameters = 'width=%spx,height=%spx' % (self.width, self.height)
    src = os.path.splitext( self.path )[0]
    s = (parameters, src, self.caption, self.thumbnail, body)
    t = u'\n\\begin{ntilocalvideo}\n\\ntiincludelocalvideo[%s]{%s}{%s}{%s}\n%s\n\\end{ntilocalvideo}\n'
    return t % s

types.Document.render = document_renderer
types.Body.render = body_renderer
types.EPUBBody.render = epub_body_renderer
types.Chapter.render = chapter_renderer
types.Section.render = section_renderer
types.SubSection.render = subsection_renderer
types.SubSubSection.render = subsubsection_renderer
types.SubSubSubSection.render = subsubsubsection_renderer
types.SubSubSubSubSection.render = subsubsubsubsection_renderer
types.Paragraph.render = paragraph_renderer
types.Run.render = run_renderer

types.OrderedList.render = ordered_list_renderer
types.UnorderedList.render = unordered_list_renderer
types.DescriptionList.render = list_desc_renderer
types.List.render = list_renderer
types.Item.render = item_renderer
types.ItemWithDesc.render = item_with_desc_renderer
types.DT.render = dt_renderer
types.DD.render = dd_renderer

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
types.DocxImage.render = docx_image_annotation_renderer
types.Video.render = video_renderer

NAQuestion.render = question_renderer
NAQuestionPart.render = question_part_renderer
NAQChoices.render = choices_renderer
NAQChoice.render = choice_renderer
NAQSolutions.render = solutions_renderer
NAQSolution.render = solution_renderer

types.Table.render =  table_html_renderer
types.Row.render = table_row_html_renderer
types.Cell.render = table_cell_html_renderer
types.THead.render = theader_html_renderer
types.TFoot.render = tfooter_html_renderer
types.TBody.render = tbody_html_renderer

types.Math.render = math_html_renderer
types.MRow.render = math_row_html_renderer
types.MFenced.render = math_fenced_html_rendered
types.MathRun.render = math_run_html_rendered
types.Mtable.render = math_table_html_rendered
types.Mtr.render = math_tr_html_rendered
types.Mtd.render = math_td_html_rendered
types.Mfrac.render = math_frac_html_rendered
types.MSup.render = math_sup_html_rendered
types.MSub.render = math_sub_html_rendered
types.MSubSup.render = math_subsup_html_rendered
types.Msqrt.render = math_msqrt_html_rendered
types.Mroot.render = math_mroot_html_rendered
types.MUnder.render = math_munder_html_rendered
types.MUnderover.render = math_munderover_html_rendered
types.MOver.render = math_mover_html_rendered
types.MMultiscripts.render = math_mmultiscript_html_rendered
types.MNone.render = math_mnone_html_rendered
types.MMprescripts.render = math_mprescripts_html_rendered
types.MMenclose.render = math_menclose_html_rendered
types.MText.render = math_mtext_html_rendered

types.OMath.render = omath_rendered
types.OMathPara.render = omath_para_rendered
types.OMathRun.render = omath_run_rendered
types.OMathFrac.render = omath_fraction_rendered
types.OMathNumerator.render = omath_numerator_rendered
types.OMathDenominator.render = omath_denominator_rendered
types.OMathRadical.render = omath_rad_rendered
types.OMathDegree.render = omath_deg_rendered
types.OMathBase.render = omath_base_rendered
types.OMathSuperscript.render = omath_superscript_rendered
types.OMathSup.render = omath_sup_rendered
types.OMathSubscript.render = omath_subscript_rendered
types.OMathSub.render = omath_sub_rendered
types.OMathSubSup.render = omath_subsup_rendered
types.OMathNary.render = omath_nary_rendered
types.OMathNaryPr.render = omath_nary_pr_rendered
types.OMathDelimiter.render = omath_delimiter_rendered
types.OMathDPr.render = omath_dpr_rendered
types.OMathLimLow.render = omath_lim_low_rendered
types.OMathBar.render = omath_bar_rendered
types.OMathAcc.render = omath_acc_rendered
types.OMathMatrix.render = omath_matrix_rendered
types.OMathMr.render = omath_mr_rendered
types.OMathFunc.render = omath_func_rendered
types.OMathFName.render = omath_fname_rendered
types.OMathEqArr.render = omath_eqarr_rendered
types.OMathSPre.render = omath_spre_rendered
types.OMathBox.render = omath_box_rendered
types.OMathGroupChr.render = omath_groupchr_rendered
types.OMathLimUpp.render = omath_limupp_rendered
types.OMathBorderBox.render = omath_bdr_box_rendered

types.CodeLine.render = code_line_rendered
types.Code.render = code_line_rendered
types.Verbatim.render = verbatim_code_renderer

types.AlternateContent.render = alternate_content_rendered
types.TextBoxContent.render = text_box_content_rendered
types.NoteInteractive.render = note_interactive_rendered
types.Figure.render = figure_rendered

types.Glossary.render = glossary_renderer
types.GlossaryList.render = glossary_list_renderer
types.GlossaryItem.render = glossary_item_renderer
types.GlossaryDT.render = glossary_dt_renderer
types.GlossaryDD.render = glossary_dd_renderer
types.GlossaryTerm.render = glossary_term_renderer

types.ChapterExercise.render = chapter_exercise_renderer
types.ExerciseSection.render = exercise_section_renderer
types.ExerciseElement.render = exercise_element_renderer
types.Exercise.render = exercise_renderer
types.Problem.render = problem_renderer
types.Solution.render = solution_renderer
types.MultipleChoices.render = multiple_choice_renderer
types.ExerciseCheck.render = exercise_check_renderer
types.ProblemExercise.render = problem_exercise_renderer
types.EndOfChapterSolution.render = chapter_solution_renderer

types.OpenstaxNote.render = openstax_note_renderer
types.OpenstaxExampleNote.render = openstax_example_note_renderer
types.OpenstaxNoteBody.render = openstax_ex_note_body_renderer

types.EquationImage.render = equation_image_renderer
types.OpenstaxAttributions.render = openstax_attribution_renderer
types.OpenstaxTitle.render = openstax_title_renderer

types.FootnoteMark.render = footnotemark_renderer
types.FootnoteText.render = footnotetext_renderer

types.CNXProblemSolution.render  = cnx_problem_solution_renderer

def register():
    pass

