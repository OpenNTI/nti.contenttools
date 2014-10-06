#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from IPython.core.debugger import Tracer

logger = __import__('logging').getLogger(__name__)
from .base import base_renderer
from ... import types

def _image_renderer(self, command):
    params, command = set_image_params_and_command(self,command)
    #to make sure we always keep images under images dir (especially when we work on Epub)
    new_path = 'images/%s' %(self.path)
    return u'\\%s[%s]{%s}' % (command, params, new_path)

def image_annotation_renderer(self):
    return _image_renderer(self, 'ntiincludeannotationgraphics')

def image_noannotation_renderer(self):
    return _image_renderer(self, 'ntiincludenoannotationgraphics')

def docx_image_annotation_renderer(self):
    return docx_image_renderer(self, 'ntiincludeannotationgraphics')

def docx_image_renderer(self, command):
    params, command = set_image_params_and_command(self,command)
    return u'\\%s[%s]{%s}' % (command, params, self.path)

def set_image_params_and_command(self, command):
    check_table, image_in_a_row = check_image_in_table(self)
    width = self.width
    height = self.height

    if check_table :
        width = 600/image_in_a_row
        if self.width > width:
            if self.height != 0:
                height = int(float(width / self.width) * self.height)
    else: 
        if self.width > 600:
            if self.height != 0:
                height = int(float(600.0 / self.width) * self.height)
            width = 600

    params = 'width=%spx,height=%spx' % (width, height)

    # Output 'small' images as ordinary graphics instead of some fancy type
    threshold = 30
    if self.width < threshold or self.height < threshold:
        command = u'includegraphics'

    #make sure if image is an equation image, the command will be 'includegraphics'
    if self.equation_image == True:
        command = u'includegraphics'

    return params, command

def base_figured_rendered(info):
    result = []
    for child in info:
        result.append(child.render())
    return u''.join(result)

def figure_rendered(self):
    
    if self.caption is not None:
        caption = base_renderer(self.caption)
    else:
        logger.info("caption for figure is empty")
        caption = self.caption
    
    label = self.label

    return u'\\begin{figure}\n\\begin{center}\n%s\n\\caption{%s}\n\\label{%s}\n\\end{center}\n\\end{figure}\n'\
         %(base_renderer(self), caption, label)

def check_image_in_table(self):
    """
    check if image is located inside table
    """
    parent = self.__parent__
    while parent is not None:
        if isinstance(parent,types.Cell):
            if isinstance(parent.__parent__, types.Row):
                return True, parent.__parent__.number_of_col
        else:
            parent = parent.__parent__
    return False, 0





