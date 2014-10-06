#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
this module is used to process equation images found in openstax book

.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml.html import HtmlComment

from ... import types
from IPython.core.debugger import Tracer

class EquationImage(types.EquationImage):

	@classmethod
	def process(cls, element, epub):
		from .openstax import Run
		me = cls()
		for child in element:
			if child.tag == 'span' and child.attrib['class'] == 'label':
				me.label = Run.process(child, epub)
			elif child.tag == 'div' and child.attrib['class'] == 'mediaobject':
				me.image = Run.process(child, epub)
				me.image = set_equation_image(me.image)
			elif isinstance(child, HtmlComment):
				pass
			else:
				me.text = Run.process(child, epub)
		return me

def set_equation_image(node):
	for child in node:
		if isinstance(child, types.Image):
			child.equation_image = True
	return node

