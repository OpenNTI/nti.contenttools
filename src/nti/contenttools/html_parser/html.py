#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: html.py 58552 2015-01-29 23:10:30Z egawati.panjei $

"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml import etree, html

import os
import codecs
from lxml import html
from .adapters import adapt
from .. import types
from ..renders.LaTeX.base import base_renderer

class HTMLParser(object):
	def __init__(self, script):
		self.script = script
	
	def process(self):
		element = html.fromstring(self.script)
		nodes = adapt(element)
		tex = base_renderer(nodes)
		return tex

