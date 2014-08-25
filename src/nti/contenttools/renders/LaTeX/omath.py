#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: omath.py 47567 2014-08-20 16:59:51Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from IPython.core.debugger import Tracer
from .base import base_renderer
from nti.contenttools.docx.omath import OMathDPr
from nti.contenttools.docx.omath import OMathMatrix
from nti.contenttools.docx.omath import OMathFName

logger = __import__('logging').getLogger(__name__)

def omath_basic_rendered(self):
	result = u''
	for child in self.children:
	    result = result + child.render()
	return u''+result

def omath_rendered(self):
	"""
	to render <m:OMath> element
	"""
	global begMatrixBorder 
	global endMatrixBorder
	begMatrixBorder = None
	endMatrixBorder = None

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
	else:
		logger.warn('Unhandled <m:nary> render')
		return u''


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
			return u'%s' %(self.children[1].render())
		elif self.children[0].begChr is not None and isinstance(self.children[1].children[0], OMathMatrix):
			#if it is a matrix
			check_matrix_border(self.children[0].begChr, self.children[0].endChr)
			return u'%s' %(self.children[1].render())
		else:
			return u'%s%s%s' %(self.children[0].children[0].render(),self.children[1].render(),self.children[0].children[1].render())		
	else:
		return u'%s' %(self.children[0].render())


begMatrixBorder = None
endMatrixBorder = None
def check_matrix_border(begChr, endChr):
	global begMatrixBorder
	global endMatrixBorder
	begMatrixBorder = begChr
	endMatrixBorder = endChr

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
		return u'\\lim_{%s \\to %s}' %(self.children[1].children[0].render(), self.children[1].children[2].render())


def omath_bar_rendered(self):
	"""
	to render <m:bar>
	"""
	return u'\\bar{%s}' %(self.children[0].render())

def omath_acc_rendered(self):
	"""
	to render <m:acc>
	"""
	return u'\\hat{%s}' %(self.children[0].render())


def omath_matrix_rendered(self):
	"""
	to render <m:m>
	"""
	body = u''
	for child in self.children:
	    body = body + child.render()
	if begMatrixBorder == '(':
		return u'\\begin{pmatrix}\n'+ body + u'\\end{pmatrix}\n'
	elif begMatrixBorder == '[':
		return u'\\begin{bmatrix}\n'+ body + u'\\end{bmatrix}\n'
	else:
		return u'\\begin{matrix}\n'+ body + u'\\end{matrix}\n'

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
