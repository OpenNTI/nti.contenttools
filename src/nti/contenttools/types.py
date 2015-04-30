#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contentfragments.interfaces import PlainTextContentFragment
from nti.contentfragments.latex import PlainTextToLatexFragmentConverter

from nti.contenttools import unicode_to_latex

class _Node( object ):
	__parent__ = None
	children = ()
	
	def add_child( self, child ):
		if self.children == ():
			self.children = []
		if isinstance( child, _Node ):
			self.children.append( child )
			child.__parent__ = self

	def remove_child( self, child ):
		self.children.remove( child )
		child.__parent__ = None

	def render( self):
		result = u''

		if not hasattr(self, 'children'):
			return self

		for child in self:
			result = result + child.render()

		return result

	def __iter__(self):
		current_item = 0
		while ( current_item < len(self.children) ):
			yield self.children[current_item]
			current_item += 1

def _to_latex(text, type_text):
	#replace special unicode in TextNode with latex tag when text is a part of equation (math element)
	#we use unicode_to_latex._replace_unicode_with_latex_tag(text) to avoid going through large extended escape_list
	#otherwise the text replacement will take place when calling in nti.contentfragments.latex.PlainTextToLatexFragmentConverter 
	#and try to keep escape list for nti.contentfragments.latex.PlainTextToLatexFragmentConverter small
	new_text = text
	if type_text == 'omath':
		string_list = list(text)
		if len(string_list) > 1:
			new_text = unicode_to_latex._replace_multi_char(new_text)
		else:
			new_text = unicode_to_latex._replace_unicode_with_latex_tag(new_text)
		return new_text
	else:
		return PlainTextToLatexFragmentConverter(new_text)

class TextNode(_Node, PlainTextContentFragment):

	__slots__ = PlainTextContentFragment.__slots__ + ('children','__parent__')

	def __new__( cls, text ='', type_text = None):
		return super(TextNode,cls).__new__( cls, _to_latex(text, type_text) )

	def __init__( self, text='', type_text = None):
		# Note: __new__ does all the actual work, because these are immutable as strings
		super(TextNode,self).__init__( self, _to_latex(text, type_text) )

	def render( self ):
		return unicode( self )

class DocumentStructureNode( _Node ):
	
	STYLES = {}

	def __init__( self ):
		super( DocumentStructureNode, self ).__init__()
		self.styles = []

	def raw( self ):
		val = u''
		for child in self:
			if hasattr( child, 'raw' ):
				val = val + child.raw()
			else:
				val = val + child
		return val

	def addStyle( self, style ):
		self.styles.append(style)

	def removeStyle( self, style ):
		self.styles.remove(style)

class Document( DocumentStructureNode ):

	def __init__( self, doc_type=u'book' ):
		self.doc_type = doc_type
		self.title = u''
		self.author = u''
		self.packages = [ 'graphicx',
						  'hyperref',
						  'ulem',
						  'ntilatexmacros',
						  'ntiassessment',
						  'amsmath',
						  'enumitem',
						  'listings',
						  'ntiglossary',
						  'Tabbing',
						  'textgreek']

class Body( DocumentStructureNode ):
	pass

class EPUBBody(DocumentStructureNode):
	pass

class Chapter( DocumentStructureNode ):

	def __init__( self, suppressed=False, title=None, label=None ):
		super( Chapter, self ).__init__()
		self.suppressed = suppressed
		self.title = title
		self.label = label

	def set_title(self, title):
		self.title = title

	def set_label(self, label):
		self.label = label

class Section( DocumentStructureNode ):

	def __init__( self, suppressed=False, label = None, title = None):
		super( Section, self ).__init__()
		self.suppressed = suppressed
		self.title = title
		self.label = label

	def set_title(self, title):
		self.title = title

	def set_label(self, label):
		self.label = label

class SubSection( DocumentStructureNode ):
	def __init__( self, label = None, title = None):
		super( SubSection, self ).__init__()
		self.title = title
		self.label = label

class SubSubSection( DocumentStructureNode ):
	pass

class SubSubSubSection( DocumentStructureNode ):
	pass

class SubSubSubSubSection( DocumentStructureNode ):
	pass

class Paragraph( DocumentStructureNode ):
	pass

class Run( DocumentStructureNode ):
	pass

class Newline( DocumentStructureNode ):
	pass

class Note( DocumentStructureNode ):
	pass

class Hyperlink( DocumentStructureNode ):

	def __init__(self, target=None, type_='Normal'):
		super( Hyperlink, self ).__init__()
		self.target = target
		self.type = type_

class Iframe(DocumentStructureNode):
	pass
	
class Label( DocumentStructureNode ):

	def __init__(self, name=''):
		super( Label, self ).__init__()
		self.name = name

class Sidebar( DocumentStructureNode ):

	def __init__(self, title=''):
		super( Sidebar, self ).__init__()
		self.title = title

class BlockQuote( DocumentStructureNode ):

	def __init__(self, source=''):
		super( BlockQuote, self ).__init__()
		self.source = source

class Image( DocumentStructureNode ):

	def __init__(self, path=''):
		super( Image, self ).__init__()
		self.path = u''
		self.caption = u''
		self.width = 0
		self.height = 0
		self.equation_image = False
		self.inline_image = False

class DocxImage( Image ):
	pass

class Video( DocumentStructureNode ):

	def __init__(self, path=''):
		super( Video, self ).__init__()
		self.path = u''
		self.thumbnail = u''
		self.caption = u''
		self.width = 0
		self.height = 0

class List( DocumentStructureNode ):

	def __init__(self, level='', group='', start=0, fmt=''):
		self.level = level
		self.group = group
		self.start = start
		self.format = fmt

class DescriptionList(List):
	pass


class UnorderedList( List ):
	pass

class OrderedList( List ):
	def __init__(self):
		super(OrderedList, self).__init__(fmt='decimal')

class Item( DocumentStructureNode ):
	pass

class ItemWithDesc( Item ):
	pass
	
class DT(DocumentStructureNode):
	def __init__(self, desc=None, type_=None):
		self.desc = desc
		self.type_ = type_

	def set_description(self, desc):
		self.desc = desc

	def set_type(self, type_):
		self.type_ = type_


class DD(DocumentStructureNode):
	pass

class Table(DocumentStructureNode):
	def __init__(self, number_of_col_header=0, number_of_col_body=0, caption=None, label=None, border=False, type_=None, alignment=u'left'):
		self.number_of_col_header = number_of_col_header
		self.number_of_col_body = number_of_col_body
		self.caption = caption
		self.label = label
		self.border = border
		self.type_ = type_
		self.alignment = alignment

	def set_number_of_col_header(self, number_of_col_header):
		self.number_of_col_header = number_of_col_header

	def set_number_of_col_body(self, number_of_col_body):
		self.number_of_col_body = number_of_col_body

	def set_caption(self, caption):
		self.caption = caption

	def set_label(self, label):
		self.label = label

	def set_border(self, border):
		self.border = border

	def set_type(self, type_):
		self.type_ = type_

	def set_alignment(self, alignment):
		self.alignment =alignment

class Row(DocumentStructureNode):
	def __init__(self, number_of_col=0, border = False, type_=None):
		self.number_of_col = number_of_col
		self.border = border
		self.type_ = type_
		
	def set_number_of_col(self, number_of_col):
		self.number_of_col = number_of_col

	def set_border(self, border):
		self.border = border

	def set_type(self, type_):
		self.type_ = type_

class Cell (DocumentStructureNode):
	def __init__(self, border=False):
		self.border = border
		self.is_first_cell_in_the_row = False
		self.colspan = 1

	def set_border(self, border):
		self.border = border

class TBody(DocumentStructureNode):
	def __init__(self, number_of_col=0, border=False):
		self.number_of_col = number_of_col
		self.border = border
		
	def set_number_of_col(self, number_of_col):
		self.number_of_col = number_of_col

	def set_border(self, border):
		self.border = border

class THead(DocumentStructureNode):
	def __init__(self, number_of_col=0, border=False):
		self.number_of_col = number_of_col
		
	def set_number_of_col(self, number_of_col):
		self.number_of_col = number_of_col

	def set_border(self, border):
		self.border = border

class TFoot(DocumentStructureNode):
	def __init__(self, number_of_col=0):
		self.number_of_col = number_of_col
		
	def set_number_of_col(self, number_of_col):
		self.number_of_col = number_of_col

class Math(DocumentStructureNode):
	pass

class MRow(DocumentStructureNode):
	pass

class MSup(DocumentStructureNode):
	pass

class MSub(DocumentStructureNode):
	pass

class MSubSup(DocumentStructureNode):
	pass

class MathRun(DocumentStructureNode):
	pass

class MFenced(DocumentStructureNode):
	def __init__(self, opener=u'', close=u'', separators = u''):
		self.opener = opener
		self.close = close
		self.separators = separators

class MSpace(DocumentStructureNode):
	def __init__(self, width=0, height=0):
		self.width = width
		self.height = height

class Mtable(DocumentStructureNode):
	def __init__(self, number_of_col=0):
		self.number_of_col = number_of_col
		
	def set_number_of_col(self, number_of_col):
		self.number_of_col = number_of_col

class Mtr(DocumentStructureNode):
	def __init__(self, number_of_col=0):
		self.number_of_col = number_of_col
		
	def set_number_of_col(self, number_of_col):
		self.number_of_col = number_of_col

class Mtd (DocumentStructureNode):
	pass

class Mfrac(DocumentStructureNode):
	pass

class Msqrt(DocumentStructureNode):
	pass

class Mroot(DocumentStructureNode):
	pass

class MUnder(DocumentStructureNode):
	pass

class MUnderover(DocumentStructureNode):
	pass

class MOver(DocumentStructureNode):
	pass

class OMath(DocumentStructureNode):
	pass

class OMathRun(DocumentStructureNode):
	pass

class OMathFrac(DocumentStructureNode):
	def __init__(self,frac_type= None):
		self.frac_type = frac_type
		
	def set_frac_type(self, frac_type):
		self.frac_type = frac_type

class OMathNumerator(DocumentStructureNode):
	pass

class OMathDenominator(DocumentStructureNode):
	pass

class OMathRadical(DocumentStructureNode):
	pass

class OMathDegree(DocumentStructureNode):
	pass

class OMathBase(DocumentStructureNode):
	pass

class OMathSuperscript(DocumentStructureNode):
	pass

class OMathSup(DocumentStructureNode):
	pass

class OMathSubscript(DocumentStructureNode):
	pass

class OMathSub(DocumentStructureNode):
	pass 

class OMathSubSup(DocumentStructureNode):
	pass

class OMathNary(DocumentStructureNode):
	pass

class OMathNaryPr(DocumentStructureNode):
	def __init__(self, chrVal = None, limLocVal = None):
		self.chrVal = chrVal
		self.limLocVal = limLocVal

	def set_chr_val (self, chrVal):
		self.chrVal = chrVal

	def set_lim_loc_val (self, limLocVal):
		self.limLocVal = limLocVal

class OMathDelimiter(DocumentStructureNode):
	pass

class OMathDPr(DocumentStructureNode):
	def __init__(self, begChr = None, endChr = None):
		self.begChr = begChr
		self.endChr = endChr

	def set_beg_char (self, begChr):
		self.begChr = begChr

	def set_end_char (self, endChr):
		self.endChr = endChr

class OMathLim(DocumentStructureNode):
	pass

class OMathLimLow(DocumentStructureNode):
	pass

class OMathBar(DocumentStructureNode):
	def __init__(self, pos=None):
		self.pos = pos

	def set_bar_pos(self, pos):
		self.pos = pos

class OMathAcc(DocumentStructureNode):
	def __init__(self, accChr=None):
		self.accChr = accChr

	def set_acc_chr(self, accChr):
		self.accChr = accChr

class OMathPara(DocumentStructureNode):
	pass

#handling matrix for docx
class OMathMatrix(DocumentStructureNode):
	def __init__(self, number_of_col=0, number_of_row=0, begChr = None, endChr = None):
		self.number_of_col = number_of_col
		self.number_of_row = number_of_row
		self.begChr = begChr
		self.endChr = endChr
		
	def set_number_of_col(self, number_of_col):
		self.number_of_col = number_of_col

	def set_number_of_row(self, number_of_row):
		self.number_of_row = number_of_row

	def set_beg_char (self, begChr):
		self.begChr = begChr

	def set_end_char (self, endChr):
		self.endChr = endChr

#handling matrix property
class OMathMPr (DocumentStructureNode):
	pass

class OMathMcs (DocumentStructureNode):
	pass

class OMathMc (DocumentStructureNode):
	pass

class OMathMcPr (DocumentStructureNode):
	pass

#handling matrix row
class OMathMr (DocumentStructureNode):
	pass

#omath: handling function apply function
class OMathFunc(DocumentStructureNode):
	pass

class OMathFName(DocumentStructureNode):
	pass

#omath : handling equation-array function
class OMathEqArr(DocumentStructureNode):
	def __init__(self, rowSpace=1):
		self.rowSpace = rowSpace

	def set_row_space (self, rowSpace):
		self.rowSpace = rowSpace

class OMathSPre(DocumentStructureNode):
	pass

class OMathBox(DocumentStructureNode):
	pass

class OMathGroupChr(DocumentStructureNode):
	def __init__(self, groupChr=None, pos=None, vertJc=None):
		self.groupChr = groupChr
		self.pos = pos
		self.vertJc = vertJc

	def set_groupChr(self, groupChr):
		self.groupChr = groupChr

	def set_pos(self, pos):
		self.pos = pos

	def set_vertJc(self, vertJc):
		self.vertJc = vertJc

class OMathLimUpp(DocumentStructureNode):
	pass

class OMathBorderBox(DocumentStructureNode):
	pass

class CodeLine(DocumentStructureNode):
	pass

class AlternateContent(DocumentStructureNode):
	pass

class TextBoxContent(DocumentStructureNode):
	pass

class NoteInteractive(DocumentStructureNode):
	def __init__(self, image_path='', label='', link=None, caption='', notes=''):
		self.image_path = image_path
		self.label = label
		self.link = link
		self.caption = caption
		self.notes = notes

	def set_image_path(self,image_path):
		self.image_path = image_path

	def set_label(self, label):
		self.label = label

	def set_link(self, link):
		self.link = link

	def set_caption(self, caption):
		self.caption = caption

	def set_notes(self, notes):
		self.notes = notes

class NoteInteractiveImage(DocumentStructureNode):
	def __init__(self, path=''):
		super( NoteInteractiveImage, self ).__init__()
		self.path = u''
		self.caption = u''

class Figure(DocumentStructureNode):
	def __init__(self, caption = None, label = None):
		self.caption = caption
		self.label = label

	def set_caption(self, caption):
		self.caption = caption

	def set_label(self, label):
		self.label = label

class Glossary(DocumentStructureNode):
	def __init__(self, title = None, filename=None, glossary_dict=None):
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
	def __init__(self, problem =  None, solution = None, label=None):
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
	def __init__(self, question = None, problem_type = None, solution=None, label=None):
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
	def __init__(self, solution = None, label = None, problem_type = None):
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
	def __init__(self,title=None, problem_type=None, label=None):
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

	def set_solution(self,solution):
		self.solution =solution

class EndOfChapterSolution(DocumentStructureNode):
	def __init__(self,label=None, title=None, body=None):
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
	def __init__(self,label=None, image=None, text=None):
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