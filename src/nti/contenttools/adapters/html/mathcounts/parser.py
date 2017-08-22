#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: parser.py 81889 2016-01-28 16:40:10Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml import html

from nti.contenttools.adapters.html.mathcounts.run import HTMLBody

from nti.contenttools.renderers.LaTeX.base import render_output

def adapt(fragment):
    body = fragment.find('body')
    html_body = HTMLBody.process(body)
    return html_body

class MathcountsHTMLParser(object):

	def __init__(self, script):
		self.script = script

	def process(self):
		element = html.fromstring(self.script)
		nodes = adapt(element)
		tex = base_renderer(nodes)
		return tex
