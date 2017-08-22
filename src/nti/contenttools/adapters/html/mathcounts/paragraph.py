#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: paragraph.py 119034 2017-08-09 13:43:34Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)


from nti.contenttools import types

from nti.contenttools.adapters.html.mathcounts import check_child
from nti.contenttools.adapters.html.mathcounts import check_element_text
from nti.contenttools.adapters.html.mathcounts import check_element_tail


class Paragraph(types.Paragraph):

	@classmethod
	def process(cls, element, styles=(), html=None):
		attrib = element.attrib
		node = cls()
		node = check_element_text(node, element)
		node = check_child(node, element, html)
		node = check_element_tail(node, element)

		if 'class' in attrib:
			if 'Normal' in attrib['class']:
				node = create_symmath_node(node)

		return node

def create_symmath_node(node):
	"""
	This function basically creates {naqsymmathpart} env with empty solution and explanation
	"""
	naqsymmath = types.NaqSymmath()
	naqsymmathpart = types.NaqSymmathPart()
	naqsymmathpart.text = node
	naqsymmathpart.solution = types.NaqSymmathPartSolution()
	naqsymmathpart.solution.value = types.NaqSymmathPartSolutionValue()
	naqsymmathpart.explanation = types.NaqSymmathPartSolutionExplanation()
	naqsymmath.add(naqsymmathpart)
	return naqsymmath