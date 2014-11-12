#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import codecs

def process_untoken_glossary(glossary_dict, filename):
	content = get_file_content(filename)
	content = content.decode("utf-8") if isinstance(content, bytes) else content
	for key in glossary_dict.keys():
		key_text =key.rstrip()
		definition = glossary_dict[key].rstrip()
		search_text = u'%s' %(key)
		new_text = u'\\ntiglossaryentry{%s}{%s}' % (key, definition)
		if content.find(search_text) < 0:
			logger.warn("Could not find glossary key %s", key)
		content = content.replace(search_text, new_text)
	replace_file_content(filename, content)

def process_glossary(glossary_dict, filename, search_text=None):
	content = get_file_content(filename)
	content = content.decode("utf-8") if isinstance(content, bytes) else content

	for key in glossary_dict.keys():
		check_key = 0
		key_text =key.rstrip()
		definition = glossary_dict[key].rstrip()
		content, check_key= add_definition(key_text, definition, content, search_text, check_key)

		#if the glossary term located in the beginning of a sentence
		cap_key = key_text.capitalize()
		content, check_key = add_definition(cap_key, definition, content, search_text, check_key)

		#if the key use capital letter in the beginning of word 
		#while glossary term found in the chapter use lower case
		lower_key = capital_to_lower_case(key_text)
		content, check_key = add_definition(lower_key, definition, content, search_text, check_key)
		#incase lower key located in the beginning of a sentence
		b_lower_key = lower_key.capitalize()
		content, check_key = add_definition(b_lower_key, definition, content, search_text, check_key)


		#if the glossary term has textit tag
		italic_key = u'\\textit{%s}' %(key_text)
		content, check_key = add_definition(italic_key, definition, content, search_text, check_key)

		#if the glossary term is singular but listed as a plural word in the glossary dict
		single_key = plural_to_single_word(key_text)
		content, check_key = add_definition(single_key, definition, content, search_text, check_key)
		single_key = plural_to_single_word(lower_key)
		content, check_key = add_definition(single_key, definition, content, search_text, check_key)
		single_key = plural_to_single_word(b_lower_key)
		content, check_key = add_definition(single_key, definition, content, search_text, check_key)

		#if the glossary term is plural but listed as a single word in the glossary dict
		plural_key = single_to_plural_word(key_text)
		content, check_key = add_definition(plural_key, definition, content, search_text, check_key)
		plural_key = single_to_plural_word(cap_key)
		content, check_key = add_definition(plural_key, definition, content, search_text, check_key)
		plural_key = single_to_plural_word(italic_key)
		content, check_key = add_definition(plural_key, definition, content, search_text, check_key)
		plural_key = single_to_plural_word(lower_key)
		content, check_key = add_definition(plural_key, definition, content, search_text, check_key)
		plural_key = single_to_plural_word(b_lower_key)
		content, check_key = add_definition(plural_key, definition, content, search_text, check_key)

		if check_key == 0:
			logger.warn('Could not find glossary key %s',key)

	new_content = content
	replace_file_content(filename, new_content)

def capital_to_lower_case(text):
	words = text.split()
	result = []
	for word in words:
		result.append(word.lower())
	new_text = u' '.join(result)
	return new_text

def single_to_plural_word(word):
	end_char = ['ch', 'x', 's']
	length = len(word)
	if length == 0:
		return word
	elif word[length-1] in end_char:
		return word + u'es'
	elif word[length-2:length-1] in end_char:
		return word + u'es'
	else:
		return word + u's'

def plural_to_single_word(word):
	length = len(word)
	end_char = ['ch', 'x', 's']
	if length == 0:
		return word
	elif word[length-2:length-1] == 'es' and word[length-1] in end_char:
		return word[0:length-3]
	elif word[length-2:length-1] == 'es' and word[length-2:length-1] in end_char:
		return word[0:length-3]
	elif word[length-1] == 's':
		return word[0:length-2]
	else:
		return word

def add_definition(key, definition, content, search_text, check_key):
	new_text = u''
	if search_text is None:
		# logger.info('Use default search text')
		search_text = u'\\ntiglossaryentry{\\textbf{%s}}{definition}' % (key)
		new_text = u'\\ntiglossaryentry{\\textbf{%s}}{%s}' % (key, definition)
	elif search_text ==u'textbf':
		search_text = u'\\textbf{%s}' %(key)
		new_text = u'\\ntiglossaryentry{%s}{%s}' % (key, definition)
	elif search_text == u'textit':
		search_text = u'\\textit{%s}' %(key)
		new_text = u'\\ntiglossaryentry{%s}{%s}' % (key, definition)
	if check_key == 0 and content.find(search_text) > -1:
		check_key = 1
	new_content = content.replace(search_text, new_text)
	return new_content, check_key

def get_file_content(filename):
	with codecs.open(filename) as fp:
		file_str = fp.read()
	return file_str

def replace_file_content(filename, new_content):
	with codecs.open( filename, 'w', 'utf-8' ) as fp:
		fp.write(new_content)
