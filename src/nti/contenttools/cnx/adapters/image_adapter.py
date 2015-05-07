#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: math_adapter.py 58552 2015-01-29 23:10:30Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ... import types
from lxml.html import HtmlComment
import os
import codecs
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
		head, filename = os.path.split(path)
		me.predefined_image_path = True
		me.path = u'Images/CourseAssets/%s/%s' %(scoped_registry.book_title, filename)
		me.inline_image = inline_image
		if 'alt' in element.attrib.keys():
		    me.caption = element.attrib['alt']
		source = get_image_path(filename)
		if not os.path.exists(source):
			logger.warn('COULD NOT FIND Image : %s', source) 
			return types.Run()
		me.width, me.height = PILImage.open(source).size
		save_image(source, filename)
		return me

def get_image_path(image_title):
	image_dir = scoped_registry.current_dir
	return u'%s/%s' %(image_dir, image_title) 
	

def save_image(source, filename):
	with open (source, 'rb') as file_:
		data = StringIO.StringIO(file_.read()).getvalue()

	filepath = u'%s/Images/CourseAssets/%s/%s' % (scoped_registry.output_directory, scoped_registry.book_title, filename)
	if not os.path.exists(os.path.dirname(filepath)):
		os.makedirs(os.path.dirname(filepath))

	with open(filepath, 'wb') as file_:
		file_.write(data)


	
