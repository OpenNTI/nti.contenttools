#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: exercise.py 50214 2014-09-30 22:01:38Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from IPython.core.debugger import Tracer

from ... import types

from lxml.html import HtmlComment

"""
used to process note found in each chapter of openstax epub
"""

class OpenstaxNote (types.OpenstaxNote):
	@classmethod
	def process(cls, element, epub):
		from . openstax import Run
		me = cls()
		for child in element:
			if child.tag  == 'div' and child.attrib['class'] == 'title':
				title = Run.process(child, epub)
				me.set_title(title)
			elif child.tag == 'div' and child.attrib['class'] == 'body':
				body = Run.process(child, epub)
				me.set_body(body)
		return me