#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: paragraph.py 47567 2014-08-20 16:59:51Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from IPython.core.debugger import Tracer

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer
from nti.contenttools.docx.paragraph import OMath 
from nti.contenttools.docx.paragraph import OMathFrac
from nti.contenttools.docx.paragraph import OMathNumerator
from nti.contenttools.docx.paragraph import OMathDenominator

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
	result = []
	for child in self.children:
	    result.append(child.render())
	return u''.join(result) + u''

def omath_fraction_rendered(self):
	"""
	to render <m:f> element
	"""
	Tracer()()
	return u'\\frac{%s}{%s}' %(self.children[0].render(), self.children[1].render())


def omath_numerator_rendered(self):
	"""
	to render <m:num>
	"""
	result = []
	for child in self.children:
	    result.append(child.render())
	return u''.join(result) + u''

def omath_denominator_rendered(self):
	"""
	to render <m:den>
	"""
	result = []
	for child in self.children:
	    result.append(child.render())
	return u''.join(result) + u''