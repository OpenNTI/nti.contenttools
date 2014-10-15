#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

def note_interactive_rendered(self):
	new_image_path = u'images/%s' %(self.image_path)
	caption = self.caption.render().rstrip()
	return u'\n\\begin{nticard}{%s}\n\\label{%s}\n\\caption{%s}\n\\includegraphics{%s}\n%s\n\\end{nticard}\n'\
	 	%(self.link, self.label, caption, new_image_path, self.notes)