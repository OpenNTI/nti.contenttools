#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import _environment_renderer

def body_renderer(self):
    return _environment_renderer(self, 'document', '')

def epub_body_renderer(self):
	include_body_child = []
	count_child = 0
	for child in self.children:
		include_body_child.append(u'\\include{file_'+str(count_child)+ u'.tex}\n')
		count_child = count_child + 1
	result = u''.join(include_body_child)
	return u'\\begin{document} \n %s \n \\end{document}' %(result)