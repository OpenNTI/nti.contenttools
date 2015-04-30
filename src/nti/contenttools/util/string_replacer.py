#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: string_replacer.py 51594 2014-10-20 22:54:02Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)


def modify_string(text, old_char, new_char):
	"""
	replace a particular character found in a text
	for example in latex files, we need to make sure that if a url contains percentage sign (%), there should be '\' in front of the '%'
	the old_char = u'%' , the new_char = u'\\%'
	"""
	new_text = text
	index_char = find(text, old_char)
	new_char_length = len(new_char)
	temp_length = 0
	temp_index= 0
	for i in index_char:
		i = i + temp_length
		if i > 0:
			temp = text[i-1:i+1]
			if temp == new_char:
				temp_index = i+1
			else:
				new_text = new_text[:temp_index]+ new_text[temp_index:i+1].replace(old_char, new_char) + new_text[i+1:]
				temp_length = temp_length + new_char_length
				temp_index = i+new_char_length
		else:
			new_text = new_text[:temp_index]+ new_text[temp_index:i+1].replace(old_char, new_char) + new_text[i+1:]
			temp_length = temp_length + new_char_length
			temp_index = i+new_char_length
	return new_text

def find(string, char):
	"""
	find all index where a particular character located in a string
	"""
	return [i for i, ltr in enumerate(string) if ltr == char]

def rename_filename(filename):
	"""
	replace some characters in a filename
	"""
	FORBIDDEN_CHARACTERS = [u'<', u'>', u':', u'"', u'/', u'\\', u'|', u'?', u'*', u' ', '-', u',', u'\t', u"'", u'!']
	for ch in FORBIDDEN_CHARACTERS : 
		if ch in filename : filename = filename.replace(ch, u'_')
	return filename