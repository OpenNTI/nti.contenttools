#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer
from nti.contenttools.epub.adapters.generic import Mtable
from nti.contenttools.epub.adapters.generic import MRow
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
	return body

def math_row_html_renderer(self):
	"""
	to render element <mrow>
	"""
	#logger.info("run math_row_html_rendered")
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
	#logger.info("run math_fenced_html_rendered")
	#logger.info("self.children[0].children[0] %s", self.children[0].children[0])
	#logger.info("self.children[0].children[0].children[0] %s", self.children[0].children[0].children[0])
	opener = self.opener
	close = self.close
	separators = self.separators
	result = []
	for child in self.children:
	    result.append(child.render())
	#Tracer()()
	
	if isinstance(self.children[0].children[0], MRow) and isinstance(self.children[0].children[0].children[0], Mtable):
		return u'\\begin{matrix}\n'.join(result) + u'\\end{matrix}'
	elif isinstance(self.children[0].children[0], Mtable):
		return u'\\begin{matrix}\n'.join(result) + u'\\end{matrix}'
	else:
		return opener + u''.join(result) + u'' + close 


def math_run_html_rendered(self):
	"""
	to render types.MathRun
	"""
	#logger.info("run math_run_html_rendered")
	result = []
	for child in self.children:
	    result.append(child.render())
	#Tracer()()
	return u''.join(result) + u''

def math_table_html_rendered(self):
	"""
	to render <mtable> element
	"""
	#logger.info("run math_table_html_rendered")
	body = u''
	for child in self.children:
	    body = body + child.render()
	result = u'\\begin{tabular}\n%s\\end{tabular}\n'
	#Tracer()()
	return result % (body)

def math_tr_html_rendered(self):
	"""
	to render <mtr> element
	"""
	#logger.info("run math_tr_html_rendered")
	result = []
	for child in self.children:
	    result.append(child.render())

	return result[0] + u' & '.join(result[1:len(result)]) + u'\\\\\n'

def math_td_html_rendered(self):
	"""
	to render <mtd> element
	"""
	#logger.info("run math_td_html_rendered")
	result = []
	for child in self.children:
	    result.append(child.render())
	return u''.join(result) + u''

