#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: html.py 81889 2016-01-28 16:40:10Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml import html

from nti.contenttools.html_parser.adapters import adapt

from nti.contenttools.renders.LaTeX.base import base_renderer

class HTMLParser(object):

	def __init__(self, script):
		self.script = script

	def process(self):
		element = html.fromstring(self.script)
		nodes = adapt(element)
		tex = base_renderer(nodes)
		return tex
