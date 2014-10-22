#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)
from .base import base_renderer

"""
module to render note found in each chapter of openstax epub
"""

def openstax_note_renderer(self):
	title = self.title.render()
	body = self.body.render()
	if self.label is None:
		return u'\n\\begin{sidebar}{%s}\n%s\n\\end{sidebar}\n\\newline ' %(title, body)
	elif isinstance(self.label, str):
		return u'\n\\begin{sidebar}{%s}\\label{%s}\n%s\n\\end{sidebar}\n\\newline ' %(title, self.label, body)

def openstax_example_note_renderer(self):
	title = None
	if isinstance(self.title, unicode):
		title = self.title
	else:
		title = self.title.render()
	body = self.body.render()
	if self.label is None:
		return u'\n\\begin{sidebar}{%s}\n%s\n\\end{sidebar}\n\\newline ' %(title, body)
	elif isinstance(self.label, str):
		return u'\n\\begin{sidebar}{%s}\\label{%s}\n%s\n\\end{sidebar}\n\\newline ' %(title, self.label, body)

def openstax_ex_note_body_renderer(self):
	return base_renderer(self)

def openstax_attribution_renderer(self):
	return base_renderer(self)

def openstax_title_renderer(self):
	return u'\\\\\\textbf{%s} \\newline\n' %(base_renderer(self))