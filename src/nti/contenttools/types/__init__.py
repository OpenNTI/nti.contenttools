#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools import unicode_to_latex

from nti.contentfragments.interfaces import PlainTextContentFragment

from nti.contentfragments.latex import PlainTextToLatexFragmentConverter

from nti.contenttools.types.document import Body
from nti.contenttools.types.document import Document
from nti.contenttools.types.document import EPUBBody
from nti.contenttools.types.document import ChapterCounter

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
from nti.contenttools.types.math import MNone
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
from nti.contenttools.types.math import MLabeledTr
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
from nti.contenttools.types.glossary import GlossaryEntry
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

from nti.contenttools.types.chapter_assessment import Example
from nti.contenttools.types.chapter_assessment import Problem
from nti.contenttools.types.chapter_assessment import Exercise
from nti.contenttools.types.chapter_assessment import Solution
from nti.contenttools.types.chapter_assessment import ExerciseDiv
from nti.contenttools.types.chapter_assessment import ExerciseCheck
from nti.contenttools.types.chapter_assessment import ChapterExercise
from nti.contenttools.types.chapter_assessment import ExerciseSection
from nti.contenttools.types.chapter_assessment import ExerciseElement
from nti.contenttools.types.chapter_assessment import MultipleChoices
from nti.contenttools.types.chapter_assessment import ProblemExercise
from nti.contenttools.types.chapter_assessment import EndOfChapterSolution

from nti.contenttools.types.note import OpenstaxNote
from nti.contenttools.types.note import OpenstaxNoteBody
from nti.contenttools.types.note import OpenstaxExampleNote

from nti.contenttools.types.node import _Node

from nti.contenttools.types.text import TextNode

from nti.contenttools.types.note import Sidebar
from nti.contenttools.types.note import BlockQuote
from nti.contenttools.types.note import CenterNode

from nti.contenttools.types.code import Code
from nti.contenttools.types.code import CodeLine
from nti.contenttools.types.code import Verbatim

from nti.contenttools.types.link import Hyperlink
from nti.contenttools.types.link import RealPageNumber

from nti.contenttools.types.alternate_content import AlternateContent
from nti.contenttools.types.alternate_content import TextBoxContent

from nti.contenttools.types.symmath import NaqSymmath
from nti.contenttools.types.symmath import NaqSymmathPart
from nti.contenttools.types.symmath import NaqSymmathPartSolution
from nti.contenttools.types.symmath import NaqSymmathPartSolutionValue
from nti.contenttools.types.symmath import NaqSymmathPartSolutionExplanation

from nti.contenttools.types.concept import ConceptHierarchy
from nti.contenttools.types.concept import Concept


class Newline(DocumentStructureNode):
    pass


class Iframe(DocumentStructureNode):
    pass


class Label(DocumentStructureNode):

    def __init__(self, name=u''):
        super(Label, self).__init__()
        self.name = name


class OpenstaxAttributions(DocumentStructureNode):
    pass


class OpenstaxTitle(DocumentStructureNode):
    pass


class PreTag(DocumentStructureNode):
    pass
