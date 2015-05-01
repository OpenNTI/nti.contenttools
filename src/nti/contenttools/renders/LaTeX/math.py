#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re

from ... import types
from .base import base_renderer

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
	return u'$'+body+u'$'

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
	# separators = self.separators
	result = []
	for child in self.children:
		result.append(child.render())

	if isinstance(self.children[0], types.Mtable):
		return set_matrix_border(opener, result)
	elif isinstance(self.children[0], types.MRow):
		if self.children[0].children:
			if isinstance(self.children[0].children[0], types.Mtable):
				return set_matrix_border(opener, result)
			else:
				return opener + u''.join(result) + u'' + close
		else:
			return opener + u''.join(result) + u'' + close 
	else:
		return opener + u''.join(result) + u'' + close 


def set_matrix_border (opener, result):
	if opener == '[':
		return u'\\begin{bmatrix}\n'+ u''.join(result) + u'\\end{bmatrix}\n'
	elif opener == '(':
		return u'\\begin{pmatrix}\n'+ u''.join(result) + u'\\end{pmatrix}\n'
	else:
		return u'\\begin{matrix}\n'+ u''.join(result) + u'\\end{matrix}\n'

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

	if isinstance(self.__parent__, types.MFenced):
		#when it is a matrix
		return u'%s' %(body)
	elif isinstance (self.__parent__, types.MRow):
		if self.__parent__.__parent__:
			if isinstance(self.__parent__.__parent__, types.MFenced):
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
	return u'$' + result +u'$'

def math_frac_html_rendered(self):
	"""
	to render <mfrac> element
	"""
	if len(self.children) > 2 :
		raise Exception("<mfrac> should only have 2 children")
	else:
		return u'\\frac{%s}{%s}' %(self.children[0].render(), self.children[1].render())

def math_sub_html_rendered(self):
	"""
	to render <msub> element
	"""
	if len(self.children)> 2 :
		raise Exception("<msub> should only have 2 children")
	else:
		return u'{%s}_{%s}' %(self.children[0].render(), self.children[1].render())

def math_sup_html_rendered(self):
	"""
	to render <msup> element
	"""
	if len(self.children)!= 2 :
		logger.warn("<msup> should have 2 children")
		return u''
	else:
		return u'{%s}^{%s}' %(self.children[0].render(), self.children[1].render())

def math_subsup_html_rendered(self):
	"""
	to render <msubsup> element
	"""
	if len(self.children) > 3:
		raise Exception("<msubsup> should only have 3 children")
	elif "int" in self.children[0].render():
		return u'\\int_%s^\\%s' %(self.children[1].render(), self.children[2].render())
	else:
		return u'{%s}_{%s}^{%s}' %(self.children[0].render(), self.children[1].render(), \
			self.children[1].render()) 


def math_msqrt_html_rendered(self):
	"""
	to render <msqrt> element
	"""
	return u'\\sqrt{%s}' %(base_renderer(self))

def math_mroot_html_rendered(self):
	"""
	to render <mroot> element
	"""
	if len(self.children) != 2:
		logger.warn("<mroot> should only have 2 children")
		return u''
	else:
		return u'\\sqrt[%s]{%s}' %(self.children[1].render(), self.children[0].render())

def math_munder_html_rendered(self):
	"""
	to render <munder> element
	"""
	if len(self.children[0].children) == 2:
		base_1  = self.children[0].render()
		base_2 = self.children[1].render()
		if u'23df' in base_2.lower() or u'\u23df' in unicode(base_2).split():
			return u'\\underbracket{%s}' %(base_1)
		elif u'\u220f' in unicode(base_1).split() or u'\\prod' in base_1:
			return u'\\prod_{%s}' %(base_2)
		else:
			return u'\\underset{%s}{%s}' %(base_2, base_1)
	else:
		raise Exception ("mathml <munder> element should have 2 children")

def math_munderover_html_rendered(self):
	"""
	to render <munderover> element
	"""
	if len(self.children) == 3 :
		token = self.children[0].render()
		base_1  = self.children[1].render()
		base_2 = self.children[2].render()
		if u'\u2211' in unicode(token).split() or u'\\sum' in token:
			return u'\\sum_{%s}^{%s}' % (base_1, base_2)
		elif u'\u222b' in unicode(token).split() or u'\\int' in token:
			return u'\\int_{%s}^{%s}' % (base_1, base_2)
		elif u'\u220f' in unicode(token).split() or u'\\prod' in token:
			return u'\\prod_{%s}^{%s}' % (base_1, base_2)
		else :
			return u'\\overset{%s}{\\underset{%s}{%s}}' %(base_2, base_1, token)
	else:
		return u''

def math_mover_html_rendered(self):
	"""
	to render <mover> element
	"""
	if u'23de' in self.children[1].render().lower() or u'\u23de' in unicode(self.children[1].render()).split():
			return u'\\overbracket{%s}' %(self.children[0].render())
	else:
			return u'\\overset{%s}{%s}' %(self.children[1].render(), self.children[0].render())


