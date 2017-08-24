#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: media.py 119034 2017-08-09 13:43:34Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os

import base64

import codecs

import shutil

from nti.contenttools import types

from nti.contenttools.adapters.html.mathcounts.run import Run

class Image(types.Image):
    @classmethod
    def process(cls, element, inline_image=True, html=None):
        me = cls()
        me.inline_image = inline_image
        if 'src' in element.attrib:
        	src = element.attrib['src']
        	if 'base64' in src:
        		img_data_idx = src.find(',')
        		img_str = src[img_data_idx:]
        		img_data = base64.b64decode(img_str)
        		
        		img_type_idx_start = src.find('/') + 1
        		img_type_idx_end = src.find(';')
        		img_type = src[img_type_idx_start:img_type_idx_end]

        		if html:
        			html.image_counter = html.image_counter + 1
        			filepath = u'Images/%s/%s.%s' % (html.labelling, html.image_counter, img_type)
        			save_image(img_data, filepath, html)
        	else:
        		img_idx_start = src.find('/') + 1
        		img_idx_last = src.rfind('/') + 1
        		img_filename = src[img_idx_last:]
        		
        		filepath = u'Images/%s/%s' %(html.labelling, img_filename)
        		img_path = u'%s/%s' % (html.output_dir, filepath)

        		img_source = src[img_idx_start:]

        		shutil.copy(img_source,img_path)
        	
        	me.predefined_image_path = True
        	me.path = filepath

        return me
        
def save_image(image_data, filepath, html):
    filepath = u'%s/%s' % (html.output_dir, filepath)
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    with codecs.open(filepath, 'wb') as fp:
        fp.write(image_data)