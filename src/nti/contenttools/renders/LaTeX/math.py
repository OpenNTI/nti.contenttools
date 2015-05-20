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
from .base import base_renderer, list_renderer

"""
rendering MathML element
"""
def math_html_renderer(self):
	"""
	to render element <math>
	"""
	content = base_renderer(self)
	if content.isspace() or len(content) == 0:
		logger.warn('Empty math mode')
		return u''
	if self.equation_type == u'inline' : return u' \(%s\) ' %content
	else :return u'\[%s\]' %content
	

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
				return u'\\begin{array}{%s}\n%s\\end{array}' %(string_col, body)
		else:
			return u'\\begin{array}{%s}\n%s\\end{array}' % (string_col, body)	
	else:
		return u'\\begin{array}{%s}\n%s\\end{array}'	% (string_col, body)


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
		return u'\\frac{%s}{%s}' %(self.children[0].render(), self.children[1].render())

def math_sub_html_rendered(self):
	"""
	to render <msub> element
	"""
	if len(self.children) != 2 :
		logger.warn('<msub> element should have 2 children')
		return u''
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
		logger.warn("<msubsup> should only have 3 children")
		return u''
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
	if len(self.children) == 2:
		base_1  = self.children[0].render()
		base_2 = self.children[1].render()
		if u'23df' in base_2.lower() or u'\u23df' in unicode(base_2).split():
			return u'\\underbracket{%s}' %(base_1)
		elif u'\u220f' in unicode(base_1).split() or u'\\prod' in base_1:
			return u'\\prod_{%s}' %(base_2)
		else:
			return u'\\underset{%s}{%s}' %(base_2, base_1)
	else:
		logger.warn("mathml <munder> element should have 2 children")
		return u''

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

def math_mmultiscript_html_rendered(self):
	"""
	render <mmultiscript> element 
	"""
	if self.prescripts is not None and self.base is not None:
		prescripts = self.prescripts.render()
		base = list_renderer(self.base)
		return u'%s%s' %(prescripts, base)
	else:
		logger.warn(u'<mmultiscript> prescripts or base is None')
		return u''

def math_mnone_html_rendered(self):
	return u''

def math_mprescripts_html_rendered(self):
	if self.sub is not None and self.sup is not None:
		sub = list_renderer(self.sub)
		sup = list_renderer(self.sup)
		return u'{_{%s}^{%s}}' %(sub, sup)
	else:
		logger.warn('prescripts sub or sup is None')
		logger.warn(self.__parent__)
		logger.warn(self.__parent__.children)


def math_menclose_html_rendered(self):
	notation = list(self.notation.split())
	base = base_renderer(self)
	for item in notation:
		if item == u'updiagonalstrike':
			#TODO : need to use package : cancel, uncomment if we are able to use cancel
			#base = m_updiagonalstrike(base) 
			pass
		elif item == u'downdiagonalstrike':
			#TODO : need to use package : cancel, uncomment if we are able to use cancel
			#base = m_downdiagonalstrike(base)
			pass
		elif item == 'radical':
			base = m_radical(base)
		elif item == 'left':
			base = m_left(base)
		elif item == 'right':
			base = m_right(base)
		elif item == 'top':
			base = m_top(base)
		elif item == 'bottom':
			base = m_bottom(base)
		elif item == 'verticalstrike':
			#TODO : need to use package : cancel, uncomment if we are able to use cancel
			#base = m_verticalstrike(base)
			pass
		elif item == 'horizontalstrike':
			#TODO : need to use package : cancel, uncomment if we are able to use cancel
			#base = m_horizontalstrike(base)
			pass
		elif item == 'madruwb':
			#TODO : create a method to handle this notation
			pass
		elif item == 'updiagonalarrow':
			#TODO : create a method to handle this notation
			pass
		elif item == 'phasorangle':
			#TODO : create a method to handle this notation
			pass
		elif item == 'actuarial':
			#TODO : create a method to handle this notation
			pass
		elif item == 'box':
			base = m_box(base)
		elif item == 'roundedbox':
			#TODO : create a method to handle this notation
			pass
		elif item == 'circle':
			#TODO : create a method to handle this notation
			pass
		elif item == 'longdiv':
			base = m_longdiv(base)
	return base

def m_radical(base):
	return u'\\sqrt{%s}' %base

def m_updiagonalstrike(base):
	return u'\\cancel{%s}' %base

def m_downdiagonalstrike(base):
	return u'\\bcancel{%s}' %base

def m_horizontalstrike(base):
	return u'\\hcancel{%s}' %base

def m_top(base):
	return u'\\overline{%s}' %base

def m_bottom(base):
	return u'\\underline{%s}' %base

def m_box(base):
	return u'\\boxed{%s}' %base

def m_longdiv(base):
	#TODO : the render result will look odd, find a better command
	return u'\\overline{)%s}' %base

def m_left(base):
	return u'\\Big|%s' %base

def m_right(base):
	return u'%s\Big|' %base

def math_mtext_html_rendered(self):
	content = base_renderer(self)
	if len(content) > 0 : return u'\\text{%s}' %content 
	else : return u''




