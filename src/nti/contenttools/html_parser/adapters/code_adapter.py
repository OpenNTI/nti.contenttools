#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml.html import HtmlComment

from nti.contenttools import types

from nti.contenttools.html_parser.adapters.run_adapter import check_child
from nti.contenttools.html_parser.adapters.run_adapter import check_element_text
from nti.contenttools.html_parser.adapters.run_adapter import check_element_tail

class Code (types.Code):
	@classmethod
	def process(cls, element):
		me = cls()
		me = check_element_text(me, element)
		me = check_child(me, element)
		me = check_element_tail(me, element)
		return me


class Verbatim(types.Verbatim):
	@classmethod
	def process(cls, element):
		me = cls()
		me = check_element_text(me, element)
		me = check_verbatim_child(me,element)
		me = check_element_tail(me, element)
		return me

class VerbatimChild(types.Run):
	@classmethod
	def process(cls, element):
		me = cls()
		me = check_element_text(me, element)
		me = check_verbatim_child(me,element)
		me = check_element_tail(me, element)
		return me

def check_verbatim_child(me, element):
	for child in element:
		node = VerbatimChild.process(child)
		me.add_child(node)
		if child.tag == 'span':
			class_ = element.attrib['class'] if 'class' in element.attrib else u''
			if class_ in ('pysrc-output', 'pysrc-prompt', 'pysrc-more'):
				me.add_child(types.TextNode('\n'))
	return me 

