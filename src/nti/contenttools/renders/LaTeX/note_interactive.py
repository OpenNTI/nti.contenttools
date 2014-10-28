#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import codecs

from nti.contenttools.import_epub import scoped_registry

def note_interactive_rendered(self):
	new_image_path = u'images/%s' %(self.image_path)
	# save image path infomation to file, in case content team wants to replace those images
	try:
		nticard_images_filename = scoped_registry.nticard_images_filename
	except AttributeError:
		raise ValueError("nticard_images_filename not set")
	else:
		if not nticard_images_filename:
			raise ValueError("nticard_images_filename not set")

	with codecs.open(nticard_images_filename, 'a', 'utf-8') as fp:
		fp.write("%s\n" %new_image_path)

	caption = self.caption.render().rstrip()
	result =  u'\n\\begin{nticard}{%s}\n\\label{%s}\n\\caption{%s}\n\\includegraphics{%s}\n%s\n\\end{nticard}\n' \
	 		  % (self.link, self.label, caption, new_image_path, self.notes)
	return result
