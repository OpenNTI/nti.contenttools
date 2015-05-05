#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: base.py 63145 2015-04-14 23:37:52Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

def footnotemark_renderer(self):
	result =  u'\\footnotemark[%s]' %self.num if self.num is not None else u'\\footnotemark'
	return result

def footnotetext_renderer(self):
	text = self.text.render()
	result = u'\\footnotetext[%s]{%s}' %(self.num, text) if self.num is not None else u'\\footnotetext{%s}' %(text)	
	return result