#!/usr/bin/python

# word2lyx is a document parsing script used to 
# convert Microsoft Word documents to LyX documents.
# (C) Robert Oakes, 2012. Released under the terms
# of the GNU Lesser General Public License (LGPL).

# This file contains data classes and methods used for creating character styles

# Table of font family descriptions and an approximate LyX equivalent
# (roman, sans, type-writer). These are used for creating the screen
# the screen representation only. The actual LaTeX/HTML styles will need
# to be defined by the user prior to exporting the document.
FONT_FAMILIES = {'swiss':'Sans', 'modern':'Sans', 'roman':'Roman'}
LATEX_COMMANDS = {
	# Font-Family
	'Roman': '\\rmfamily', 'Sans':'\\sffamily', 'Typewriter':'\\ttfamily',
	# Font-Shape
	'Up':'\\MakeUppercase', 'SmallCaps':'\\scshape', 'Italic':'\\itshape',
	# Font-Series
	'Bold':'\\bfseries'}


class lyxStyle:
	'''Data structure used to represent custom styles used in the document.'''
	
	def __init__(self, styleName):
		self.styleName = styleName
		self.lyxType = u''
		self.latexType = u''
		self.labelString = u''

		# Data structure which contains information about the font
		# Family: Roman, Sans, Typewriter
		# Shape: Uppercase (Up), SmallCaps, Italic, Slanted
		# Series: Medium, Bold
		# Size: Tiny, Small, Normal, Large, Larger, Largest, Huge, Giant
		# Color: None, Black, White, Red, Green, Blue, Cyan Magenta, Yellow
		# Misc: emph, noun, strikeout, underbar, uuline, uwave, no_emph,
		#  no_noun, no_wave
		self.fontData = {'lyx_family':'', 'lyx_shape':'', 'lyx_series':'',
			'lyx_size':'', 'lyx_color':'', 'lyx_misc':'', 'fontname':'', 'ParentStyle':''}


class lyxCharacterStyle(lyxStyle):
	'''Data structure used to represent character styles in a LyX document.'''

	def __init__(self, styleName):
		lyxStyle.__init__(self, styleName)
		self.lyxType = u'charstyle'
		self.latexType = u'command'
		self.latexName = styleName.lower()
		self.labelString = styleName.lower()


def writeLyxCharstyle(lyx_charstyle):
	'''Parses a lyxCharacterstyle to a structure that that can be 
		exported to a LyX document.'''
	
	# Basic Components of the Character Style
	lyx_chardef = u'InsetLayout Flex:' + lyx_charstyle.styleName + '\n'
	lyx_chardef = lyx_chardef + '\tLyxType\t\t\t' + lyx_charstyle.lyxType + '\n'
	lyx_chardef = lyx_chardef + '\tLatexType\t\t' + lyx_charstyle.latexType + '\n'
	lyx_chardef = lyx_chardef + '\tLatexName\t\t' + lyx_charstyle.latexName + '\n'
	lyx_chardef = lyx_chardef + '\tLabelString\t\t' + lyx_charstyle.labelString + '\n'

	# Font Settings
	font_settings = u'\tFont\n'
	
	# Font Family
	if (lyx_charstyle.fontData['ParentStyle'] == 'DefaultParagraphFont') \
		& (lyx_charstyle.fontData['lyx_family'] == ''):
		font_settings = font_settings + '\t\tFamily\t\tRoman\n'
	elif lyx_charstyle.fontData['lyx_family'] is not '':
		font_settings = font_settings + '\t\tFamily\t\t' + lyx_charstyle.fontData['lyx_family'] + '\n'
	
	# Font Shape
	if lyx_charstyle.fontData['lyx_shape'] is not '':
		font_settings = font_settings + '\t\tShape\t\t' + lyx_charstyle.fontData['lyx_shape'] + '\n'
	
	# Font Series
	if lyx_charstyle.fontData['lyx_series'] is not '':
		font_settings = font_settings + '\t\tSeries\t\t' + lyx_charstyle.fontData['lyx_series'] + '\n'

	font_settings = font_settings + '\tEndFont\n'

	lyx_chardef = lyx_chardef + font_settings

	# Create LaTeX Command
	preamble_command = createLatexCommand(lyx_charstyle)
	lyx_chardef = lyx_chardef + '\tPreamble\n\t\t' + preamble_command + '\n\tEndPreamble\n' + 'End'

	return lyx_chardef


def createLatexCommand(lyx_charstyle):
	'''Creates a LaTeX document command that can be added to the local layout section 
		of the document. Parses fontData from the lyx_charstyle.'''

	latex_command = u'\\newcommand{\\' + lyx_charstyle.latexName + '}[1]{{'
	commandoptions = u''
	makeupper = False
	for fontprop in lyx_charstyle.fontData:
		
		# Process Properties, excluding ParentStyle
		if (fontprop != 'ParentStyle') & (fontprop != 'fontname'):
			font_data = lyx_charstyle.fontData[fontprop].split(',')
			
			# Iterate through the command properties, translating to LaTeX
			for commandprop in font_data:
				if (commandprop != '') & (commandprop != 'Up'):
					commandoptions = commandoptions + LATEX_COMMANDS[commandprop] 
				if (commandprop == 'Up'):
					makeupper = True

	# Use \MakeUppercase
	if makeupper == True:
		latex_command = latex_command + '\\MakeUppercase{' + commandoptions + ' #1}}}'
	# Only font properties
	else:
		latex_command = latex_command + commandoptions + ' #1}}'
	return latex_command