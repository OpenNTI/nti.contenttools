#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer

def cnx_problem_solution_renderer(self):
	title = u'\\textbf{%s}' %self.title.render()
	body  = base_renderer(self)
	return u'%s\n\\newline\n%s' %(title, body)
