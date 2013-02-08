#!/usr/bin/python

# word2lyx is a document parsing script used to 
# convert Microsoft Word documents to LyX documents.
# (C) Robert Oakes, 2012. Released under the terms
# of the GNU Lesser General Public License (LGPL).
# Preferred Dependencies: lxml, elyxer

# Import ConfigObj, used to read custom templates
import os
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

from configobj import ConfigObj


class DocumentOptions:
	'''Class structure used to import and process templates.
		Used to create important global variables PARAGRAPH_STYLES,
		TABLE_STYLES, and CHARACTER STYLES.'''

	def __init__(self, template):
		self.config = ConfigObj(template)
		self.DocOptions = ConfigObj(os.path.join(TEMPLATE_DIR, 'docdefaults.w2l'))
		# Modify Default DocOptions with those found in the template
		if 'DocOptions' in self.config.sections:
			for option in self.config['DocOptions']:
				# Iterate through sections in self.DocOptions
				for section in self.DocOptions.sections:
					# Find option in the structure, change the value
					if option in self.DocOptions[section]:
						self.DocOptions[section][option] = \
							self.config['DocOptions'][option]
						break

	def returnStyles(self, stylesection):
		'''Retrieve a dictionary of style definitions defined from the 
			template configuration file.'''

		if stylesection in self.config.sections:
			return self.config[stylesection]
		else:
			return {}

	def returnSetting(self, option):
		'''Return an individual option defined in the configuration file.'''
		return self.config[option]

	def optionSections(self):
		'''Retrieve a list of the option sections defined in the configuration file.
			This function can be used to create the document document header.'''
		return self.DocOptions.sections

	def getDocOptions(self, section):
		'''Retrieve the options for a particular section, which can then be iterated over
			to write the LyX file format.'''
		if section in self.DocOptions.sections:
			return self.DocOptions[section]
		else:
			return {}