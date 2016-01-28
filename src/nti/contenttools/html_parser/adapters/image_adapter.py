#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: image_adapter.py 58552 2015-01-29 23:10:30Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ... import types
from lxml.html import HtmlComment
import os
from ... import scoped_registry

from ... import types

from PIL import Image as PILImage
import os
try:
    import cStringIO as StringIO
except:
    import StringIO

class Image(types.Image):
	@classmethod
	def process(cls, element, inline_image=False):
		me = cls()
		path = element.attrib['src']
		if u'../' in path :
			path = path.replace('../', '')
		head, filename = os.path.split(path)
		me.predefined_image_path = True
		me.path = u'Images/CourseAssets/%s' %(filename)
		me.inline_image = inline_image
		if 'alt' in element.attrib.keys():
		    me.caption = types.TextNode(element.attrib['alt'])
		return me	

def save_image(image_data, filepath):
	filepath = u'%s/%s' % (scoped_registry.output_directory, filepath)
	if not os.path.exists(os.path.dirname(filepath)):
		os.makedirs(os.path.dirname(filepath))

	with open( filepath, 'wb' ) as file:
		file.write(image_data.read())


	
