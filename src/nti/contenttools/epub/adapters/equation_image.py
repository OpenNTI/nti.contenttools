#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: equation_image.py 50369 2014-10-02 18:24:13Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from IPython.core.debugger import Tracer

from ... import types
from lxml import etree
from lxml.html import HtmlComment

"""
this module is used to process equation images found in openstax book
"""

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
			elif isinstance(child, HtmlComment):
				pass
			else:
				me.text = Run.process(child, epub)
		return me
		

