#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: media.py 110445 2017-04-10 13:34:47Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools import types 


from PIL import Image as PILImage

import os

try:
    import cStringIO as StringIO
except:
    import StringIO

class Image(types.Image):
    @classmethod
    def process(cls, element,inline_image=False, epub=None):
        me = cls()
        path = element.attrib['src']
        if u'../' in path :
            path = path.replace('../', '')
        head, filename = os.path.split(path)
        me.predefined_image_path = True
        me.path = u'Images/CourseAssets/%s/%s' %(epub.book_title, filename)
        me.inline_image = inline_image
        if 'alt' in element.attrib.keys():
            me.caption = types.TextNode(element.attrib['alt'])

        zipfile = epub.zipfile

        image_path = os.path.join(epub.content_path, path)
        if image_path in zipfile.namelist():
            image_data = StringIO.StringIO(zipfile.read(image_path))
            save_image(image_data, me.path, epub)
            me.width, me.height = PILImage.open(image_data).size
        else:
            logger.warn('COULD NOT FIND Image : %s',image_path) 
            return types.Run()

        return me    

def save_image(image_data, filepath, epub):
    filepath = u'%s/%s' % (epub.output_directory, filepath)
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    with open( filepath, 'wb' ) as file:
        file.write(image_data.read())