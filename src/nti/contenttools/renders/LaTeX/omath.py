#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools.docx.omath import OMathDPr
from nti.contenttools.docx.omath import OMathFName
from nti.contenttools.docx.omath import OMathMatrix
from nti.contenttools.docx.omath import OMathNaryPr
from nti.contenttools.docx.omath import OMathEqArr
from nti.contenttools.unicode_to_latex import _replace_unicode_with_latex_tag

logger = __import__('logging').getLogger(__name__)

def omath_basic_rendered(self):
	result = u''
	for child in self.children:
		result = result + child.render()
	return result

def delimiter_child_rendered(children_list):
	result = u''
	for child in children_list:
		result = result + child.render()
	return result

def omath_rendered(self):
	"""
	to render <m:OMath> element
	"""
	global begMatrixBorder 
	global endMatrixBorder
	begMatrixBorder = None
	endMatrixBorder = None

	global begEqArrBorder
	global endEqArrBorder
	begEqArrBorder = None
	endEqArrBorder = None

	body = u''
	for child in self.children:
		body = body + child.render()
	return u'$'+body+u'$'

def omath_para_rendered(self):
	"""
	to render <m:OMathPara> element
	"""
	body = u''
	for child in self.children:
		body = body + child.render()
	return u'$'+body+u'$'

def omath_run_rendered(self):
	"""
	to render <m:r> element
	"""
	return omath_basic_rendered(self)

def omath_fraction_rendered(self):
	"""
	to render <m:f> element
	"""
	if self.frac_type == u'lin':
		return u'{%s}/{%s}' %(self.children[0].render(), self.children[1].render())
	elif self.frac_type == u'skw':
		return u'{^{%s}}/_{%s}' %(self.children[0].render(), self.children[1].render())
	elif self.frac_type == u'noBar':
		return u'{%s \\choose %s}' %(self.children[0].render(), self.children[1].render())
	return u'\\frac{%s}{%s}' %(self.children[0].render(), self.children[1].render())


def omath_numerator_rendered(self):
	"""
	to render <m:num>
	"""
	return omath_basic_rendered(self)

def omath_denominator_rendered(self):
	"""
	to render <m:den>
	"""
	return omath_basic_rendered(self)

def omath_rad_rendered(self):
	"""
	to render <m:rad> element
	"""
	if len(self.children) == 1:
		return u'\\sqrt{%s}' %(self.children[0].render())
	elif len(self.children) == 2:
		return u'\\sqrt[%s]{%s}' %(self.children[0].render(), self.children[1].render())

def omath_base_rendered(self):
	"""
	to render <m:e>
	"""
	return omath_basic_rendered(self)

def omath_deg_rendered(self):
	"""
	to render <m:deg>
	"""
	return omath_basic_rendered(self)

def omath_superscript_rendered(self):
	"""
	to render <m:sSup>
	"""
	return u'{%s}^{%s}' % (self.children[0].render(), self.children[1].render())

def omath_sup_rendered(self):
	"""
	to render <m:sup>
	"""
	return omath_basic_rendered(self)

def omath_subscript_rendered(self):
	"""
	to render <m:sSub>
	"""
	return u'{%s}_{%s}' % (self.children[0].render(), self.children[1].render())

def omath_sub_rendered(self):
	"""
	to render <m:sub>
	"""
	return omath_basic_rendered(self)

def omath_subsup_rendered(self):
	"""
	to render <m:sSubSup>
	"""
	return u'{%s}_{%s}^{%s}' % (self.children[0].render(), self.children[1].render(), self.children[2].render())

def omath_nary_rendered(self):
	"""
	to render <m:nary>
	#example : equation_sample-6.docx, equation_sample-7.docx, 
	"""
	if len(self.children) == 3:
		if u'\\sum' in unicode(self.children[0].render()) or u'\u2211' in unicode(self.children[0].render()):
			return u'\\sum_{%s}^{%s}' %(self.children[1].render(), self.children[2].render())
		elif u'\\prod' in unicode(self.children[0].render()) or u'\u220F' in unicode(self.children[0].render()):
			return u'\\prod_{%s}^{%s}' %(self.children[1].render(), self.children[2].render())
		elif u'\\int' in unicode(self.children[0].render()) or u'\u222B' in unicode(self.children[0].render()):
			return u'\\int_{%s}^{%s}' %(self.children[1].render(), self.children[2].render())
		else:
			logger.warn('Unhandled <m:nary> render when num of children = 3')
			return u''
	elif len(self.children) == 4:
		if isinstance(self.children[0], OMathNaryPr):
			if self.children[0].chrVal is not None:
				return u'%s_{%s}^{%s} %s' %(self.children[0].render(), self.children[1].render(), self.children[2].render(), \
					self.children[3].render())
			else :
				return u'\\int_{%s}^{%s} %s' %(self.children[1].render(), self.children[2].render(), self.children[3].render())


def omath_nary_pr_rendered(self):
	"""
	to render <m:naryPr>
	"""
	return omath_basic_rendered(self)

def omath_delimiter_rendered(self):
	"""
	to render <m:d>
	"""
	if isinstance (self.children[0],OMathDPr):
		if self.children[0].begChr is None:
			children_num = len(self.children)
			result = delimiter_child_rendered(self.children[1:children_num])
			if u'choose' in result:
				return u'%s' %(result)
			else:
				return u'(%s)' %(result)
		elif self.children[0].begChr is not None and isinstance(self.children[1].children[0], OMathMatrix):
			#if it is a matrix
			check_matrix_border(self.children[0].begChr, self.children[0].endChr)
			return u'%s' %(self.children[1].render())
		elif self.children[0].begChr is not None and isinstance(self.children[1].children[0], OMathEqArr):
			#if it is an equation array
			check_equation_arr_border(self.children[0].begChr, self.children[0].endChr)
			return u'%s' %(self.children[1].render())
		else:
			children_num = len(self.children)
			result = delimiter_child_rendered(self.children[1:children_num])
			begChr = _replace_unicode_with_latex_tag(self.children[0].begChr)
			endChr = _replace_unicode_with_latex_tag(self.children[0].endChr)
			return u'%s%s%s' %(begChr,result,endChr)
	else:
		return omath_basic_rendered(self)

begMatrixBorder = None
endMatrixBorder = None

def check_matrix_border(begChr, endChr):
	global begMatrixBorder
	global endMatrixBorder
	begMatrixBorder = begChr
	endMatrixBorder = endChr


begEqArrBorder = None
endEqArrBorder = None
def check_equation_arr_border(begChr, endChr):
	global begEqArrBorder
	global endEqArrBorder
	begEqArrBorder = begChr
	endEqArrBorder = endChr

def omath_dpr_rendered(self):
	"""
	to render <m:dPr>
	"""
	return omath_basic_rendered(self)

def omath_lim_low_rendered(self):
	"""
	to render <m:limlow>
	"""
	if isinstance(self.__parent__, OMathFName):
		func_name = self.children[0].render()
		under = self.children[1].render()
		return u'\\%s_{%s}' %(func_name, under)
	else:
		return u'\\underset{%s}{%s}' %(self.children[1].render(), self.children[0].render())

def omath_bar_rendered(self):
	"""
	to render <m:bar>
	"""

	if self.pos == 'top':
		return u'\\overline{%s}' %(self.children[0].render())
	else:
		return u'\\underline{%s}' %(self.children[0].render())
	


def omath_acc_rendered(self):
	"""
	to render <m:acc>
	"""
	if self.accChr is not None:
		accChr =self.accChr
		if accChr == u'\u0300': 
			return u'\\grave{%s}' %(self.children[0].render())
		elif accChr == u'\u0301': 
			return u'\\acute{%s}' %(self.children[0].render())
		elif accChr == u'\u0302': 
			return u'\\hat{%s}' %(self.children[0].render())
		elif accChr == u'\u0303': 
			return u'\\tilde{%s}' %(self.children[0].render())
		elif accChr == u'\u0304':
			return u'\\bar{%s}' %(self.children[0].render())
		elif accChr == u'\u0306':
			return u'\\breve{%s}' %(self.children[0].render())
		elif accChr == u'\u0307':
			return u'\\dot{%s}' %(self.children[0].render())
		elif accChr == u'\u0308':
			return u'\\ddot{%s}' %(self.children[0].render())
		elif accChr == u'\u030C':
			return u'\\check{%s}' %(self.children[0].render())
		elif accChr == u'\u2190' or accChr == u'\u20d6':
			return u'\\overleftarrow{%s}' %(self.children[0].render())
		elif accChr == u'\u2192' or accChr == u'\u20d7':
			return u'\\overrightarrow{%s}' %(self.children[0].render())
		elif accChr == u'\u20e1':
			return u'\\overleftrightarrow{%s}' %(self.children[0].render())
		elif accChr == u'\u20d0':
			return u'\\overset{\\leftharpoonup}{%s}' %(self.children[0].render())
		elif accChr == u'\u20d1':
			return u'\\overset{\\rightharpoonup}{%s}' %(self.children[0].render())
		elif accChr == u'\u0305':
			return u'\\overline{%s}' %(self.children[0].render())
		else:
			logger.warn('Unhandled accent unicode render')
			return u''
	else:
		return u'\\hat{%s}' %(self.children[0].render())

def omath_matrix_rendered(self):
	"""
	to render <m:m>
	"""
	body = u''
	for child in self.children:
		body = body + child.render()
	if begMatrixBorder == '(':
		return u'\\begin{pmatrix}\n %s \\end{pmatrix}\n' %(body)
	elif begMatrixBorder == '[':
		return u'\\begin{bmatrix}\n %s \\end{bmatrix}\n' %(body)
	else:
		return u'\\begin{matrix}\n %s \\end{matrix}\n' %(body)

def omath_mr_rendered(self):
	"""
	to render <m:mr>
	"""
	result = []
	for child in self.children:
		result.append(child.render())
	return u' & '.join(result) + u' \\\\\n'

def omath_func_rendered(self):
	"""
	to render <m:func>
	"""
	return omath_basic_rendered(self)

def omath_fname_rendered(self):
	"""
	to render <m:fName>
	"""
	return omath_basic_rendered(self)

def omath_eqarr_rendered(self):
	"""
	to render <m:eqArr>
	"""
	result = []
	for child in self.children:
		result.append(child.render())
		result.append(u' \\\\\n')
	body = u'\\begin{array}{lr}\n'+ u''.join(result) +u'\\end{array}'
	if self.rowSpace == 1:
		if begEqArrBorder is None and endEqArrBorder is None:
			return body
		else:	
			if begEqArrBorder == u'{' and endEqArrBorder == u'':
				return u'\\left \\{ %s \\right.' %(body)
			if begEqArrBorder == u'' and endEqArrBorder == u'}':
				return u'\\left. %s \\right \\}' %(body)
			else:
				logger.warn('Unhandled equation array element render')
				return u''
	else:
		number_of_space = self.rowSpace
		count_space = 0
		string_space = u''
		while count_space < number_of_space:
			string_space = string_space + u' l '
			count_space = count_space + 1
		return u'\\begin{array}{%s}\n' +u''.join(result)+ u'\\end{array}' %(string_space)


def omath_spre_rendered(self):
	"""
	to render <m:sPre>
	"""
	if len(self.children) == 3:
		return u'{^%s_%s}%s' %(self.children[0].render(), self.children[1].render(), self.children[2].render())
	else:
		logger.warn('Unhandled <m:sPre> render, number of children = %s', self.children)
		return u''

def omath_box_rendered(self):
	"""
	to render <m:box>
	"""
	return omath_basic_rendered(self)

def omath_groupchr_rendered(self):
	"""
	to render <m:groupChr>
	"""
	if self.pos is not None:
		groupChr = _replace_unicode_with_latex_tag(self.groupChr)
		pos = self.pos
		if pos == u'top':
			if self.groupChr == u'\u23de':
				return u'\\overbrace{%s}' %(self.children[0].render())	
			else:
				return u'\\underset{%s}{%s}' %(self.children[0].render(), groupChr)
		elif pos == u'bot':
			if self.groupChr == u'\u23df':
				return u'\\underbrace{%s}' %(self.children[0].render())	
			else:
				return u'\\underset{%s}{%s}' %(groupChr,self.children[0].render())
		else:
			logger.warn('Unhandled <m:groupChr> element when groupChrPr have position %s', self.pos)
			return u''
	elif self.vertJc is not None:
		groupChr = _replace_unicode_with_latex_tag(self.groupChr)
		vertJc = self.vertJc
		if vertJc == u'top':
			return u'\\underset{%s}{%s}' %(self.children[0].render(), groupChr)
		elif vertJc == u'bot':
			return u'\\underset{%s}{%s}' %(groupChr,self.children[0].render())
		else:
			logger.warn('Unhandled <m:groupChr> having groupChrPr position %s', self.pos)
			return u''
	else:
		return u'\\underbrace{%s}' %(self.children[0].render())	

def omath_limupp_rendered(self):
	"""
	to render <m:limUpp>
	"""
	return u'\\overset{%s}{%s}' %(self.children[1].render(), self.children[0].render())

def omath_bdr_box_rendered(self):
	"""
	to render <m:borderBox>
	"""
	return u"\\boxed {%s}" %(omath_basic_rendered(self))
