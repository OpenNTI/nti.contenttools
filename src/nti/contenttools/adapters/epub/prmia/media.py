#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re

import os
from six import StringIO

from PIL import Image as PILImage

from nti.contenttools import types

from nti.contenttools.adapters.epub.tcia import check_child
from nti.contenttools.adapters.epub.tcia import check_element_tail

from nti.contenttools.adapters.epub.tcia.run import Run


class Image(types.Image):

    @classmethod
    def process(cls, element, inline_image=False, epub=None):
        me = cls()
        if not 'src' in element.attrib.keys():
            logger.warning('<image> has no src')
            return 
        path = element.attrib['src']

        if '../' in path:
            path = path.replace('../', '')
        _, filename = os.path.split(path)
        me.predefined_image_path = True
        me.path = u'Images/CourseAssets/%s/%s' % (epub.book_title, filename) 

        if epub.input_file:
            zipfile = epub.zipfile
            image_path = os.path.join(epub.content_path, path)
            if image_path in zipfile.namelist():
                image_data = StringIO(zipfile.read(image_path))
                save_image(image_data, me.path, epub)
                me.width, me.height = PILImage.open(image_data).size
            else:
                logger.warn('COULD NOT FIND Image : %s', image_path)
                return types.Run()

        return me

def save_image(image_data, filepath, epub):
    filepath = u'%s/%s' % (epub.output_directory, filepath)
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    with open(filepath, 'wb') as fp:
        fp.write(image_data.read())


class Figure(types.Figure):

    @classmethod
    def process(cls, element, epub=None):
        me = cls()
        for child in element:
            if child.tag == 'img':
                el = Image.process(child, epub=epub)
                me.add_child(el)
            else:
                logger.warning('Unhandled Figure element child %s', child.tag)
        return me
