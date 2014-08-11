#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer
from nti.contenttools.epub.adapters.generic import Mtable
from nti.contenttools.epub.adapters.generic import MRow
from nti.contenttools.epub.adapters.generic import MFenced
from IPython.core.debugger import Tracer


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
	return u'$ ' + body + u' $'
 
def math_row_html_renderer(self):
	"""
	to render element <mrow>
	"""
	result = []
	for child in self.children:
	    result.append(child.render())
	return u''.join(result) + u''

def math_sup_html_renderer(self):
	"""
	to render element <msup>
	"""
	result = []
	for child in self.children:
	    result.append(child.render())
	return u''.join(result) + u' '

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
		if opener = '[':
			return u'\\begin{bmatrix}\n'+ u''.join(result) + u'\\end{bmatrix}\n'
		elif opener = '(':
			return u'\\begin{pmatrix}\n'+ u''.join(result) + u'\\end{pmatrix}\n'
		else:
			return u'\\begin{matrix}\n'+ u''.join(result) + u'\\end{matrix}\n'
	elif isinstance(self.children[0], MRow):
		if self.children[0].children:
			if isinstance(self.children[0].children[0], Mtable):
				if opener = '[':
					return u'\\begin{bmatrix}\n'+ u''.join(result) + u'\\end{bmatrix}\n'
				elif opener = '(':
					return u'\\begin{pmatrix}\n'+ u''.join(result) + u'\\end{pmatrix}\n'
				else:
					return u'\\begin{matrix}\n'+ u''.join(result) + u'\\end{matrix}\n'
			else:
				return opener + u''.join(result) + u'' + close
		else:
			return opener + u''.join(result) + u'' + close 
	else:
		return opener + u''.join(result) + u'' + close 


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
	body = u''
	for child in self.children:
	    body = body + child.render()
	logger.info('type of mtable parent %s',type(self.__parent__))
	if isinstance(self.__parent__, MFenced):
		result = u'%s'
	elif isinstance (self.__parent__, MRow):
		if self.__parent__.__parent__:
			if isinstance(self.__parent__.__parent__, MFenced):
				logger.info('type of mtable parent.parent %s',type(self.__parent__.__parent__))
				result = u'%s'
			else:
				body = remove_special_char("&\\", body)
				result = u'\\begin{tabular}\n%s\\end{tabular}\n' 
		else:
			result = u'\\begin{tabular}\n%s\\end{tabular}\n' 
	else:
		logger.info("else")
		result = u'\\begin{tabular}\n%s\\end{tabular}\n' 	
	
	return result % (body)

def remove_special_char(char_list, string):
	for char in string:
		if char in char_list:
			string.replace(char, u'')
	return string

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
		raise Exception("mfrac should only have 2 children")
	else:
		return u'\\frac{%s}{%s}' %(self.children[0].render(), self.children[1].render())

def math_sub_html_rendered(self):
	if len(self.children[0].children)> 2 :
		raise Exception("msub should only have 2 children")
	else:
		return u'{%s}_{%s}' %(self.children[0].children[0].render(), self.children[0].children[1].render())

def math_sup_html_rendered(self):
	if len(self.children[0].children)> 2 :
		raise Exception("msup should only have 2 children")
	else:
		return u'{%s}^{%s}' %(self.children[0].children[0].render(), self.children[0].children[1].render())
