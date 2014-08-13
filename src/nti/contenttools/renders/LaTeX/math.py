#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer
from nti.contenttools.epub.adapters.generic import Mtable
from nti.contenttools.epub.adapters.generic import MRow
from nti.contenttools.epub.adapters.generic import MFenced
import re

"""
rendering MathML element
"""
def math_html_renderer(self):
	"""
	to render element <math>
	"""
	body = u''
	for child in self.children:
	    body = body + child.render()
	return body
 
def math_row_html_renderer(self):
	"""
	to render element <mrow>
	"""
	result = []
	for child in self.children:
	    result.append(child.render())
	return u''.join(result) + u''

def math_fenced_html_rendered(self):
	"""
	to render element <mfenced>
	"""
	opener = self.opener
	close = self.close
	separators = self.separators
	result = []
	for child in self.children:
	    result.append(child.render())

	if isinstance(self.children[0], Mtable):
		return set_matrix_border(opener, result)
	elif isinstance(self.children[0], MRow):
		if self.children[0].children:
			if isinstance(self.children[0].children[0], Mtable):
				return set_matrix_border(opener, result)
			else:
				return opener + u''.join(result) + u'' + close
		else:
			return opener + u''.join(result) + u'' + close 
	else:
		return opener + u''.join(result) + u'' + close 


def set_matrix_border (opener, result):
	if opener == '[':
		return u'$\\begin{bmatrix}\n'+ u''.join(result) + u'\\end{bmatrix}$\n'
	elif opener == '(':
		return u'$\\begin{pmatrix}\n'+ u''.join(result) + u'\\end{pmatrix}$\n'
	else:
		return u'$\\begin{matrix}\n'+ u''.join(result) + u'\\end{matrix}$\n'

def math_run_html_rendered(self):
	"""
	to render types.MathRun
	"""
	result = []
	for child in self.children:
	    result.append(child.render())
	return u''.join(result) + u''

def math_table_html_rendered(self):
	"""
	to render <mtable> element
	"""
	number_of_col = self.number_of_col
	count_col = 0
	string_col = u''
	while count_col < number_of_col:
		string_col = string_col + u' l '
		count_col = count_col + 1
	
	body = u''
	for child in self.children:
	    body = body + child.render()

	if isinstance(self.__parent__, MFenced):
		#when it is a matrix
		return u'%s' %(body)
	elif isinstance (self.__parent__, MRow):
		if self.__parent__.__parent__:
			if isinstance(self.__parent__.__parent__, MFenced):
				#when it is a matrix
				return u'%s' %(body)
			else:
				return u'$\\begin{tabular}{%s}\n%s\\end{tabular}$' %(string_col, body)
		else:
			return u'$\\begin{tabular}{%s}\n%s\\end{tabular}$' % (string_col, body)	
	else:
		return u'$\\begin{tabular}{%s}\n%s\\end{tabular}$'	% (string_col, body)


def replace_special_char(char_list, string, replacer):
	new_string = string
	for char in string:
		if char in char_list:
			new_string = new_string.replace(char, replacer)
	return new_string

def find_and_replace_char_inside_matrix(string,old_char, new_char):
	return re.sub("begin{.*}.*end{.*?}", lambda x:x.group(0).replace(old_char,new_char), string)

def math_tr_html_rendered(self):
	"""
	to render <mtr> element
	"""
	result = []
	for child in self.children:
	    result.append(child.render())

	return u' & '.join(result) + u'\\\\\n'

def math_td_html_rendered(self):
	"""
	to render <mtd> element
	"""
	result = base_renderer(self)
	return result

def math_frac_html_rendered(self):
	"""
	to render <mfrac> element
	"""
	if len(self.children) > 2 :
		raise Exception("<mfrac> should only have 2 children")
	else:
		return u'$\\frac{%s}{%s}$' %(self.children[0].render(), self.children[1].render())

def math_sub_html_rendered(self):
	"""
	to render <msub> element
	"""
	if len(self.children[0].children)> 2 :
		raise Exception("<msub> should only have 2 children")
	else:
		return u'${%s}_{%s}$' %(self.children[0].children[0].render(), self.children[0].children[1].render())

def math_sup_html_rendered(self):
	"""
	to render <msup> element
	"""
	if len(self.children[0].children)> 2 :
		raise Exception("<msup> should only have 2 children")
	else:
		return u'${%s}^{%s}$' %(self.children[0].children[0].render(), self.children[0].children[1].render())

def math_subsup_html_rendered(self):
	"""
	to render <msubsup> element
	"""
	if len(self.children[0].children) > 3:
		raise Exception("<msubsup> should only have 3 children")
	elif "int" in self.children[0].children[0].render():
		return u'$\\int_%s^\\%s$' %(self.children[0].children[1].render(), self.children[0].children[2].render())
	else:
		return u'${%s}_{%s}^{%s}$' %(self.children[0].children[0].render(), self.children[0].children[1].render(), \
			self.children[0].children[1].render()) 


def math_msqrt_html_rendered(self):
	"""
	to render <msqrt> element
	"""
	if len(self.children[0].children) > 1:
		raise Exception ("<msqrt> should only have a child")
	else:
		return u'$\\sqrt{%s}$' %(self.children[0].children[0].render())

def math_mroot_html_rendered(self):
	"""
	to render <mroot> element
	"""
	if len(self.children[0].children) > 2:
		raise Exception ("<mroot> should only have 2 children")
	else:
		return u'$\\sqrt[%s]{%s}$' %(self.children[0].children[1].render(), self.children[0].children[0].render())

