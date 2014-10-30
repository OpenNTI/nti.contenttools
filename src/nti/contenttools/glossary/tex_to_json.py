#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
this module is useful to convert glossary stored in tex file to json file
if the glossary list is written in docx, convert it to latex using nti_import_docx
then use this module to convert to json
user needs to determine what kind of pattern used to define the term key
for example:
	glossary list can be written in form of: \\textbf{'key'}{'definition'}
	or \\textif{'key'}{'definition'}, where key and definition can be any value
	
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re
import codecs
import simplejson as json

def map_key_value_tex(content, pattern, open_token, close_token):
	"""
	Map strings found in a txt file to create pairs of dictionary key-value
	"""
	dictionary = {}
	new_pattern = r'^\\%s%s.*%s' %(pattern, open_token, close_token)
	for item in content:
		string_match = find_string(item, new_pattern)
		if string_match is not None:
			index = string_match.span()
			key = get_key(string_match.group(), open_token, close_token, pattern)
			value = item[index[1]:].rstrip()
			dictionary.update({key:value})
	return dictionary

def get_key(string, open_token, close_token, pattern):
	list_substr = []
	new_pattern = u'\\%s' %(pattern)
	if open_token is not None:
		text_list =  string.split(open_token)
		for _, substr in enumerate(text_list):
			if new_pattern == substr:
				pass
			else:
				list_substr.append(substr.split(close_token)[0].rstrip())
	return u''.join(list_substr)


def dictionary_to_json(dictionary, json_file):
	"""
	save dictionary to json file
	"""
	dict_json = json.dumps(dictionary, sort_keys=True, indent=4 * ' ')
	with codecs.open( json_file, 'w', 'utf-8' ) as fp:
		fp.write(dict_json)

def find_string(text, pattern):
	"""
	find particular pattern in text
	pattern could be: r'^\\textbf{.*}'
	"""
	return re.match(pattern, text)  

def get_line_from_tex(filename):
	"""
	return list of line inside tex
	"""
	with codecs.open(filename) as fp:
		content = fp.readlines()
	return content

def main():
	latex_files = (u'test.tex')
	content = get_line_from_tex(latex_files)
	pattern = u'textbf'
	open_token = u'{'
	close_token = u'}'
	dictionary = map_key_value_tex(content, pattern, open_token, close_token)
	dictionary_to_json(dictionary, u'glossary.json')

if __name__ == '__main__': # pragma: no cover
	main()
