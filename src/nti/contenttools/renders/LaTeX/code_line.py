#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: code.py 48574 2014-09-03 22:06:35Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer

def code_line_rendered(self):
	
	#return u'\\begin{lstlisting} %s \\end{lstlisting}' %(base_renderer(self))
	return u'\\begin{verbatim} %s \\end{verbatim}' %(base_renderer(self))
