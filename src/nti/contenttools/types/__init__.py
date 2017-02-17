#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contentfragments.interfaces import PlainTextContentFragment

from nti.contentfragments.latex import PlainTextToLatexFragmentConverter

from .. import unicode_to_latex

from nti.contenttools.types.document import Body
from nti.contenttools.types.document import Document
from nti.contenttools.types.document import EPUBBody

from nti.contenttools.types.lists import DD
from nti.contenttools.types.lists import DT
from nti.contenttools.types.lists import Item
from nti.contenttools.types.lists import List
from nti.contenttools.types.lists import OrderedList
from nti.contenttools.types.lists import ItemWithDesc
from nti.contenttools.types.lists import UnorderedList
from nti.contenttools.types.lists import DescriptionList

from nti.contenttools.types.node import Node
from nti.contenttools.types.node import DocumentStructureNode

from nti.contenttools.types.paragraph import Paragraph

from nti.contenttools.types.run import Run

from nti.contenttools.types.sectioning import Chapter
from nti.contenttools.types.sectioning import Section
from nti.contenttools.types.sectioning import SubSection
from nti.contenttools.types.sectioning import SubSubSection
from nti.contenttools.types.sectioning import SubSubSubSection
from nti.contenttools.types.sectioning import SubSubSubSubSection

from nti.contenttools.types.table import Row
from nti.contenttools.types.table import Cell
from nti.contenttools.types.table import TBody
from nti.contenttools.types.table import THead
from nti.contenttools.types.table import TFoot
from nti.contenttools.types.table import Table

from nti.contenttools.types.media import Figure
from nti.contenttools.types.media import Image
from nti.contenttools.types.media import DocxImage
from nti.contenttools.types.media import Video

from nti.contenttools.types.math import Math
from nti.contenttools.types.math import MRow
from nti.contenttools.types.math import MSup
from nti.contenttools.types.math import MSub
from nti.contenttools.types.math import MSubSup
from nti.contenttools.types.math import MathRun
from nti.contenttools.types.math import MFenced
from nti.contenttools.types.math import MSpace
from nti.contenttools.types.math import Mtable
from nti.contenttools.types.math import Mtr
from nti.contenttools.types.math import Mtd
from nti.contenttools.types.math import Mfrac
from nti.contenttools.types.math import Msqrt
from nti.contenttools.types.math import Mroot
from nti.contenttools.types.math import MUnder
from nti.contenttools.types.math import MUnderover
from nti.contenttools.types.math import MOver
from nti.contenttools.types.math import MMenclose
from nti.contenttools.types.math import MMprescripts
from nti.contenttools.types.math import MMultiscripts
from nti.contenttools.types.math import MText

from nti.contenttools.types.omath import OMath, OMathFunc, OMathFName
from nti.contenttools.types.omath import OMathRun
from nti.contenttools.types.omath import OMathFrac
from nti.contenttools.types.omath import OMathDenominator
from nti.contenttools.types.omath import OMathNumerator
from nti.contenttools.types.omath import OMathRadical
from nti.contenttools.types.omath import OMathDegree
from nti.contenttools.types.omath import OMathBase
from nti.contenttools.types.omath import OMathSuperscript
from nti.contenttools.types.omath import OMathSup
from nti.contenttools.types.omath import OMathSubscript
from nti.contenttools.types.omath import OMathSub
from nti.contenttools.types.omath import OMathSubSup
from nti.contenttools.types.omath import OMathNary
from nti.contenttools.types.omath import OMathNaryPr
from nti.contenttools.types.omath import OMathDelimiter
from nti.contenttools.types.omath import OMathDPr
from nti.contenttools.types.omath import OMathLim
from nti.contenttools.types.omath import OMathLimLow
from nti.contenttools.types.omath import OMathBar
from nti.contenttools.types.omath import OMathAcc
from nti.contenttools.types.omath import OMathPara
from nti.contenttools.types.omath import OMathMPr
from nti.contenttools.types.omath import OMathMcs
from nti.contenttools.types.omath import OMathMc
from nti.contenttools.types.omath import OMathMcPr
from nti.contenttools.types.omath import OMathMatrix
from nti.contenttools.types.omath import OMathMr
from nti.contenttools.types.omath import OMathEqArr
from nti.contenttools.types.omath import OMathSPre
from nti.contenttools.types.omath import OMathBox
from nti.contenttools.types.omath import OMathGroupChr
from nti.contenttools.types.omath import OMathLimUpp
from nti.contenttools.types.omath import OMathBorderBox

from nti.contenttools.types.note import Note
from nti.contenttools.types.note import NoteInteractive
from nti.contenttools.types.note import NoteInteractiveImage


def _to_latex(text, type_text):
    # replace special unicode in TextNode with latex tag when text is
    # a part of equation (math element)
    # we use unicode_to_latex._replace_unicode_with_latex_tag(text) to
    # avoid going through large extended escape_list
    # otherwise the text replacement will take place when calling in
    # nti.contentfragments.latex.PlainTextToLatexFragmentConverter
    # and try to keep escape list for
    # nti.contentfragments.latex.PlainTextToLatexFragmentConverter small
    new_text = text
    if type_text == 'omath':
        string_list = list(text)
        if len(string_list) > 1:
            new_text = unicode_to_latex._replace_multi_char(new_text)
        else:
            new_text = unicode_to_latex._replace_unicode_with_latex_tag(
                new_text)
        return new_text
    else:
        return PlainTextToLatexFragmentConverter(new_text)

from nti.contenttools.types.node import _Node


class TextNode(_Node, PlainTextContentFragment):

    __slots__ = PlainTextContentFragment.__slots__ + ('children', '__parent__')

    def __new__(cls, text='', type_text=None):
        return super(TextNode, cls).__new__(cls, _to_latex(text, type_text))

    def __init__(self, text='', type_text=None):
        # Note: __new__ does all the actual work, because these are immutable
        # as strings
        super(TextNode, self).__init__(self, _to_latex(text, type_text))

    def render(self):
        return unicode(self)


class Newline(DocumentStructureNode):
    pass


class Hyperlink(DocumentStructureNode):

    def __init__(self, target=None, type_='Normal'):
        super(Hyperlink, self).__init__()
        self.target = target
        self.type = type_


class Iframe(DocumentStructureNode):
    pass


class Label(DocumentStructureNode):

    def __init__(self, name=''):
        super(Label, self).__init__()
        self.name = name


class Sidebar(DocumentStructureNode):

    def __init__(self, title=''):
        super(Sidebar, self).__init__()
        self.title = None
        self.label = None
        self.type = None


class BlockQuote(DocumentStructureNode):

    def __init__(self, source=''):
        super(BlockQuote, self).__init__()
        self.source = source


class MNone(DocumentStructureNode):
    pass


class CodeLine(DocumentStructureNode):
    pass


class Code(DocumentStructureNode):
    pass


class Verbatim(DocumentStructureNode):
    pass


class AlternateContent(DocumentStructureNode):
    pass


class TextBoxContent(DocumentStructureNode):
    pass


class Glossary(DocumentStructureNode):

    def __init__(self, title=None, filename=None, glossary_dict=None):
        self.title = title
        self.filename = filename
        self.glossary_dict = glossary_dict

    def set_title(self, title):
        self.title = title

    def set_filename(self, filename):
        self.filename = filename

    def set_glossary_dict(self, glossary_dict):
        self.glossary_dict = glossary_dict


class GlossaryList(DocumentStructureNode):
    pass


class GlossaryItem(DocumentStructureNode):
    pass


class GlossaryDT(DocumentStructureNode):

    def __init__(self, desc=None):
        self.desc = desc

    def set_description(self, desc):
        self.desc = desc


class GlossaryDD(DocumentStructureNode):
    pass


class GlossaryTerm(DocumentStructureNode):
    pass


class Exercise(DocumentStructureNode):

    def __init__(self, problem=None, solution=None, label=None):
        self.problem = problem
        self.solution = solution
        self.label = label

    def set_problem(self, problem):
        self.problem = problem

    def set_solution(self, solution):
        self.solution = solution

    def set_label(self, label):
        self.label = label


class Problem (DocumentStructureNode):

    def __init__(
            self, question=None, problem_type=None, solution=None, label=None):
        self.question = question
        self.problem_type = problem_type
        self.solution = solution
        self.label = label

    def set_question(self, question):
        self.question = question

    def set_problem_type(self, problem_type):
        self.problem_type = problem_type

    def set_solution(self, solution):
        self.solution = solution

    def set_label(self, label):
        self.label = label


class Solution (DocumentStructureNode):

    def __init__(self, solution=None, label=None, problem_type=None):
        self.solution = solution
        self.label = label
        self.problem_type = problem_type

    def set_solution(self, solution):
        self.solution = solution

    def set_label(self, label):
        self.label = label

    def set_problem_type(self, problem_type):
        self.problem_type = problem_type


class MultipleChoices(DocumentStructureNode):

    def __init__(self, solution=None, choices=None):
        self.solution = solution
        self.choices = choices

    def set_solution(self, solution):
        self.solution = solution

    def set_choices(self, choices):
        self.choices = choices


class ChapterExercise(DocumentStructureNode):
    pass


class ExerciseSection(DocumentStructureNode):
    pass


class ExerciseElement(DocumentStructureNode):
    pass


class ExerciseDiv(DocumentStructureNode):
    pass


class Example(DocumentStructureNode):
    pass


class ProblemExercise(DocumentStructureNode):

    def __init__(self, title=None, problem_type=None, label=None):
        super(ProblemExercise, self).__init__()
        self.title = title
        self.problem_type = problem_type
        self.label = label


class ExerciseCheck(DocumentStructureNode):

    def __init__(self, title=None, solution=None):
        self.title = title
        self.solution = solution

    def set_title(self, title):
        self.title = title

    def set_solution(self, solution):
        self.solution = solution


class EndOfChapterSolution(DocumentStructureNode):

    def __init__(self, label=None, title=None, body=None):
        super(EndOfChapterSolution, self).__init__
        self.label = label
        self.title = title
        self.body = body


class OpenstaxNote (DocumentStructureNode):

    def __init__(self, title=None, body=None, label=None):
        self.title = title
        self.body = body
        self.label = label

    def set_title(self, title):
        self.title = title

    def set_body(self, body):
        self.body = body

    def set_label(self, label):
        self.label = label


class OpenstaxExampleNote(OpenstaxNote):
    pass


class OpenstaxNoteBody(DocumentStructureNode):
    pass


class EquationImage(DocumentStructureNode):

    def __init__(self, label=None, image=None, text=None):
        super(EquationImage, self).__init__()
        self.label = label
        self.image = image
        self.text = text


class OpenstaxAttributions(DocumentStructureNode):
    pass


class OpenstaxTitle(DocumentStructureNode):
    pass


class CNXCollection(DocumentStructureNode):

    def __init__(self):
        self.content = None
        self.metadata = None


class CNXSubcollection(DocumentStructureNode):

    def __init__(self):
        self.content = None
        self.title = None


class CNXContent(DocumentStructureNode):

    def __init__(self):
        self.modules = []
        self.subcollections = []


class CNXModule(DocumentStructureNode):

    def __init__(self):
        self.document = None
        self.title = None


class CNXHTMLBody(DocumentStructureNode):
    pass


class CNXGlossary(DocumentStructureNode):
    pass


class CNXProblemSolution(DocumentStructureNode):

    def __init__(self):
        self.title = None
        self.label = None


class GlossaryDefinition(DocumentStructureNode):

    def __init__(self):
        self.term = None
        self.meaning = None


class Footnote(DocumentStructureNode):

    def __init__(self):
        self.label = None
        self.text = None


class FootnoteText(DocumentStructureNode):

    def __init__(self):
        self.text = None
        self.label = None
        self.num = None


class FootnoteMark(DocumentStructureNode):

    def __init__(self):
        self.text = None
        self.num = None


class PreTag(DocumentStructureNode):
    pass


class NaqSymmathPart(DocumentStructureNode):

    def __init__(self):
        self.text = u''
        self.solution = u''
        self.label = u''


class NaqSymmathPartSolution(DocumentStructureNode):
    pass


class NaqSymmathPartSolutionValue(DocumentStructureNode):

    def __init__(self):
        self.option = u''
        self.value = u''
