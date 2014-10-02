#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

"""
module to render note found in each chapter of openstax epub
"""

def openstax_note_renderer(self):
	logger.debug("found note sidebar")
	title = self.title.render()
	body = self.body.render()
	return u'\n\\begin{sidebar}{%s}\n%s\n\\end{sidebar}\n' %(title, body)
