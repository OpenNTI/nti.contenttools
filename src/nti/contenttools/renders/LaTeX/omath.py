#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: omath.py 47567 2014-08-20 16:59:51Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from IPython.core.debugger import Tracer
from .base import base_renderer

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
		#render sum of
		if u'\\sum' in unicode(self.children[0].render()) or u'\u2211' in unicode(self.children[0].render()):
			return u'\\sum_{%s}^{%s}' %(self.children[1].render(), self.children[2].render())
		if u'\\prod' in unicode(self.children[0].render()) or u'\u220F' in unicode(self.children[0].render()):
			return u'\\prod_{%s}^{%s}' %(self.children[1].render(), self.children[2].render())
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
	return u'%s%s%s' %(self.children[0].children[0].render(),self.children[1].render(), self.children[0].children[1].render())

def omath_dpr_rendered(self):
	"""
	to render <m:dPr>
	"""
	return omath_basic_rendered(self)

def omath_lim_low_rendered(self):
	"""
	to render <m:limlow>
	"""
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







