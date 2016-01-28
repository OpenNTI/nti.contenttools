#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: image_adapter.py 58552 2015-01-29 23:10:30Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import shutil
import requests
from lxml.html import HtmlComment

from PIL import Image as PILImage
import os
try:
    import cStringIO as StringIO
except:
    import StringIO

from ... import types
from ... import scoped_registry

class Image(types.Image):
	@classmethod
	def process(cls, element, inline_image=False):
		me = cls()
		path = element.attrib['src']
		if u'../' in path :
			path = path.replace('../', '')
			image_url = u'%s/%s' %(scoped_registry.image_url, path)
			filepath = u'%s/%s' %(scoped_registry.output_directory, path)
			save_image(image_url, filepath)

		head, filename = os.path.split(path)
		me.predefined_image_path = True
		me.path = path
		me.inline_image = inline_image
		if 'alt' in element.attrib.keys():
		    me.caption = types.TextNode(element.attrib['alt'])
		return me	

def save_image(image_url, filepath):
	r = requests.get(image_url, stream=True)
	if r.status_code == 200:
		if not os.path.exists(os.path.dirname(filepath)):
			os.makedirs(os.path.dirname(filepath))
		with open(filepath, 'wb') as f:
		    r.raw.decode_content = True
		    shutil.copyfileobj(r.raw, f)   


	
