#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: omath.py 47567 2014-08-20 16:59:51Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

#from IPython.core.debugger import Tracer

logger = __import__('logging').getLogger(__name__)

def omath_basic_rendered(self):
	result = []
	for child in self.children:
	    result.append(child.render())
	return u''.join(result) + u''

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
