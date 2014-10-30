#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
this module is useful to convert glossary stored in txt file to json file
assumption : 
	key-definition pair of each glossary term is in the same line
	key and definition is separated using particular char (token)
	
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)
import codecs
import simplejson as json

def map_key_value(content, token):
	"""
	Map strings found in a txt file to pairs of dictionary key-value
	"""
	dictionary = {}
	token_length = len(token)
	for item in content:
		index = find(item, token)
		if len(index) == 1:
			key = item[:index[0]-1]
			value = item[index[0]+token_length:].rstrip()
			dictionary.update({key:value})
		elif len(index) == 0:
			pass
		else:
			print('Unhandled condition')
	return dictionary

def find(string, char):
	"""
	find index where char is found
	"""
	return [i for i, ltr in enumerate(string) if ltr == char]

def dictionary_to_json(dictionary, json_file):
	"""
	save dictionary to json file
	"""
	dict_json = json.dumps(dictionary, sort_keys=True, indent=4 * ' ')
	with codecs.open( json_file, 'w', 'utf-8' ) as fp:
		fp.write(dict_json)

def get_content(filename):
	content = []
	with codecs.open(filename) as fp:
		content  = fp.readlines()
	return content

def main():
	content = get_content('glossary.txt')
	dictionary = map_key_value(content, ':')
	dictionary_to_json(dictionary, 'glossary.json')

if __name__ == '__main__': # pragma: no cover
    main()