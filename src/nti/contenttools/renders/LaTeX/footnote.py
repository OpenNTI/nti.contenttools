#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: base.py 63145 2015-04-14 23:37:52Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)
from .base import base_renderer

def footnotemark_renderer(self):
	result =  u'\\footnotemark[%s]' %self.num if self.num is not None else u'\\footnotemark'
	return result

def footnotetext_renderer(self):
	text = self.text.render()
	child_text = base_renderer(self)
	result = u'\\footnotetext[%s]{%s %s}\n' %(self.num, text, child_text) if self.num is not None else u'\\footnotetext{%s %s}\n' %(text, child_text)	
	return result

