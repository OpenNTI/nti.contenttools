from ..types import _Node
from ..types import *

# These classes encapsulate WordprocessingML structures
class _DocxStructureElement( _Node ):
	STYLES = {}

	def __init__( self ):
		super( _DocxStructureElement, self ).__init__()
		self.styles = []

	def __str__( self ):
		val = u''
		for child in self.children:
			if isinstance( child, _DocxStructureElement ):
				val = val + child.__str__()
			else:
				val = val + child


		for style in self.styles:
			if val:
				if style in self.__class__.STYLES:
					val = self.__class__.STYLES[style](val)
				else:
					print('Unhandled style: %s' % style)

		return val

	def raw( self ):
		val = u''
		for child in self.children:
			if isinstance( child, _DocxStructureElement ):
				val = val + child.raw()
			else:
				val = val + child
		return val

	def addStyle( self, style ):
		self.styles.append(style)

	def removeStyle( self, style ):
		self.styles.remove(style)


class _TextRun( _DocxStructureElement ):
	STYLES = { 'bold': TextBF,
		   'inserted': Modified,
		   'italic': TextIT,
		   'strike': Strikeout,
		   'underline': Uline}

class _Paragraph( _DocxStructureElement ):
	STYLES = { 'Heading1': Chapter,
		   'Heading2': Section,
		   'Heading3': SubSection,
		   'Heading4': SubSubSection,
		   'Heading5': Paragraph,
		   'Heading6': SubParagraph,
		   'Heading7': SubSubParagraph}

	def __str__( self ):
		return '' + super(_Paragraph, self).__str__() + '\n'

