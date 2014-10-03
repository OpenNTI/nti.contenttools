#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
module to render equation image found in openstax epub

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

def equation_image_renderer(self):

	label = self.label.render().rstrip()
	if self.image is not None:
		image = self.image.render()
		return u'\n\\begin{center}\n%s \\hspace{20 mm} %s\n\\end{center}\n' %(image, label)
	elif self.text is not None:
		text = self.text.render().rstrip()
		return u'\n\\begin{center}\n%s \\hspace{20 mm} %s\n\\end{center}\n' %(text, label)
