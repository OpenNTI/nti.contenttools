#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: mathcounts.py 66352 2015-06-01 21:38:46Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re

from ... import types
from .base import base_renderer, list_renderer

def naq_symmath_part_renderer(self):
	"""
	render NaqSymmathPart
	"""
	content = self.text.render()
	if content.isspace() or len(content) == 0:
		logger.warn('Empty NaqSymmathPart')
		return u''
	
	solution_part = self.solution.render()

	result = u"\n\\begin{naqsymmathpart}\n%s\n%s\n\\end{naqsymmathpart}\n" %(content, solution_part)

	return result


def naq_symmath_part_solution_renderer(self):
	"""
	render NaqSymmathPartSolution
	"""
	solution = base_renderer(self)

	result = u"\\begin{naqsolutions}\n%s\n\\end{naqsolutions}" %(solution)

	return result


def naq_symmath_part_solution_value_renderer(self):
	"""
	render NaqSymmathPartSolution
	"""
	if self.option.isspace or len (self.option) == 0:
		option = self.option
	else:
		option = u"<%s>" %(self.option)
	
	value = self.value.render()

	result = u"\\naqsolution[1] %s %s\n" %(option, value)
	return result

