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
from nti.contenttools.types.table import Table
from nti.contenttools.types.table import TBody
from nti.contenttools.types.table import THead
from nti.contenttools.types.table import TFoot

from nti.contenttools.types.media import Image
from nti.contenttools.types.media import Video
from nti.contenttools.types.media import Figure
from nti.contenttools.types.media import DocxImage
from nti.contenttools.types.media import EquationImage

from nti.contenttools.types.math import Mtr
from nti.contenttools.types.math import Mtd
from nti.contenttools.types.math import Math
from nti.contenttools.types.math import MRow
from nti.contenttools.types.math import MSup
from nti.contenttools.types.math import MSub
from nti.contenttools.types.math import MFrac
from nti.contenttools.types.math import MRoot
from nti.contenttools.types.math import MOver
from nti.contenttools.types.math import Msqrt
from nti.contenttools.types.math import MText
from nti.contenttools.types.math import MUnder
from nti.contenttools.types.math import MSpace
from nti.contenttools.types.math import Mtable
from nti.contenttools.types.math import MathRun
from nti.contenttools.types.math import MFenced
from nti.contenttools.types.math import MSubSup
from nti.contenttools.types.math import MMenclose
from nti.contenttools.types.math import MUnderover
from nti.contenttools.types.math import MMprescripts
from nti.contenttools.types.math import MMultiscripts

from nti.contenttools.types.omath import OMath
from nti.contenttools.types.omath import OMathMc
from nti.contenttools.types.omath import OMathMr
from nti.contenttools.types.omath import OMathAcc
from nti.contenttools.types.omath import OMathBar
from nti.contenttools.types.omath import OMathBox
from nti.contenttools.types.omath import OMathDPr
from nti.contenttools.types.omath import OMathLim
from nti.contenttools.types.omath import OMathMcs
from nti.contenttools.types.omath import OMathMPr
from nti.contenttools.types.omath import OMathRun
from nti.contenttools.types.omath import OMathSub
from nti.contenttools.types.omath import OMathSup
from nti.contenttools.types.omath import OMathBase
from nti.contenttools.types.omath import OMathFrac
from nti.contenttools.types.omath import OMathFunc
from nti.contenttools.types.omath import OMathMcPr
from nti.contenttools.types.omath import OMathNary
from nti.contenttools.types.omath import OMathPara
from nti.contenttools.types.omath import OMathSPre
from nti.contenttools.types.omath import OMathEqArr
from nti.contenttools.types.omath import OMathFName
from nti.contenttools.types.omath import OMathLimLow
from nti.contenttools.types.omath import OMathLimUpp
from nti.contenttools.types.omath import OMathMatrix
from nti.contenttools.types.omath import OMathNaryPr
from nti.contenttools.types.omath import OMathDegree
from nti.contenttools.types.omath import OMathSubSup
from nti.contenttools.types.omath import OMathRadical
from nti.contenttools.types.omath import OMathGroupChr
from nti.contenttools.types.omath import OMathBorderBox
from nti.contenttools.types.omath import OMathDelimiter
from nti.contenttools.types.omath import OMathNumerator
from nti.contenttools.types.omath import OMathSubscript
from nti.contenttools.types.omath import OMathDenominator
from nti.contenttools.types.omath import OMathSuperscript

from nti.contenttools.types.note import Note
from nti.contenttools.types.note import NoteInteractive
from nti.contenttools.types.note import NoteInteractiveImage

from nti.contenttools.types.glossary import Glossary
from nti.contenttools.types.glossary import GlossaryDT
from nti.contenttools.types.glossary import GlossaryDD
from nti.contenttools.types.glossary import GlossaryList
from nti.contenttools.types.glossary import GlossaryItem
from nti.contenttools.types.glossary import GlossaryTerm
from nti.contenttools.types.glossary import GlossaryDefinition

from nti.contenttools.types.footnote import Footnote
from nti.contenttools.types.footnote import FootnoteText
from nti.contenttools.types.footnote import FootnoteMark

from nti.contenttools.types.cnx import CNXModule
from nti.contenttools.types.cnx import CNXContent
from nti.contenttools.types.cnx import CNXHTMLBody
from nti.contenttools.types.cnx import CNXGlossary
from nti.contenttools.types.cnx import CNXCollection
from nti.contenttools.types.cnx import CNXSubcollection
from nti.contenttools.types.cnx import CNXProblemSolution

from nti.contenttools.types.exercise import Example
from nti.contenttools.types.exercise import Problem
from nti.contenttools.types.exercise import Exercise
from nti.contenttools.types.exercise import Solution
from nti.contenttools.types.exercise import ExerciseDiv
from nti.contenttools.types.exercise import ExerciseCheck
from nti.contenttools.types.exercise import ChapterExercise
from nti.contenttools.types.exercise import ExerciseSection
from nti.contenttools.types.exercise import ExerciseElement
from nti.contenttools.types.exercise import MultipleChoices
from nti.contenttools.types.exercise import ProblemExercise
from nti.contenttools.types.exercise import EndOfChapterSolution

from nti.contenttools.types.note import OpenstaxNote
from nti.contenttools.types.note import OpenstaxNoteBody
from nti.contenttools.types.note import OpenstaxExampleNote


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


class OpenstaxAttributions(DocumentStructureNode):
    pass


class OpenstaxTitle(DocumentStructureNode):
    pass


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
