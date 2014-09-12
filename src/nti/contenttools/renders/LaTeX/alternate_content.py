#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)
from IPython.core.debugger import Tracer
from .base import base_renderer

def alternate_content_rendered(self):
	return base_renderer(self)

def text_box_content_rendered(self):
	return u'\\parbox[c]{\\textwidth}{%s}' %(base_renderer(self))
	