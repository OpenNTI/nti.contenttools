#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer

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
	#Tracer()()
	return body

def math_row_html_renderer(self):
	"""
	to render element <mrow>
	"""
	result = []
	for child in self.children:
	    result.append(child.render())
	#Tracer()()
	return u''.join(result) + u''

def math_sup_html_renderer(self):
	"""
	to render element <msup>
	"""
	result = []
	for child in self.children:
	    result.append(child.render())
	#Tracer()()
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

	return opener + u''.join(result) + u'' + close 

def math_run_html_rendered(self):
	"""
	to render types.MathRun
	"""
	result = []
	for child in self.children:
	    result.append(child.render())
	#Tracer()()
	return u''.join(result) + u''

