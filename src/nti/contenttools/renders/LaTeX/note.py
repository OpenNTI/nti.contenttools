#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: note.py 50214 2014-09-30 22:01:38Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from IPython.core.debugger import Tracer

from .base import base_renderer

"""
module to render note found in each chapter of openstax epub
"""

def openstax_note_renderer(self):
	logger.info("found note sidebar")
	title = self.title.render()
	body = self.body.render()
	return u'\n\\begin{sidebar}{%s}\n%s\n\\end{sidebar}\n' %(title, body)
