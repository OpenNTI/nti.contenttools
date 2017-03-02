#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: media.py 107708 2017-03-01 08:30:02Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
from nti.contenttools.renderers.LaTeX.base import render_node, render_children
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import IImage
from nti.contenttools.types.interfaces import IVideo
from nti.contenttools.types.interfaces import IFigure
from nti.contenttools.types.interfaces import IDocxImage
from nti.contenttools.types.interfaces import IEquationImage

from nti.contenttools.types.interfaces import ICell
from nti.contenttools.types.interfaces import IRow

from nti.contenttools.types.interfaces import ISidebar
from nti.contenttools.types.interfaces import IOpenstaxNote
from nti.contenttools.types.interfaces import IOpenstaxExampleNote
from nti.contenttools.types.interfaces import IOpenstaxNoteBody

def render_image_annotation(context, node):
    return render_image(context, node, u'ntiincludeannotationgraphics')

def render_image_noannotation(context, node):
    return render_image(context, node, u'ntiincludenoannotationgraphics')

def render_image(context, node, command):
    params, command = set_image_params_and_command(node,command)
    new_path = node.path if node.predefined_image_path else 'images/%s' %(node.path)
    context.write(u'\\')
    context.write(command)
    context.write(u'[')
    context.write(params)
    context.write(u']')
    context.write(u'{')
    context.write(new_path)
    context.write(u'}')
    return node

def set_image_params_and_command(node, command):
    width = node.width
    height = node.height
    MAX_WIDTH = 650.0 #600 is the maximum width of images in the platform (webapp)

    check_sidebar = check_image_in_sidebar(node)
    if check_sidebar:
        MAX_WIDTH = 500 #500 is the maximum width of an image if it is located inside a sidebar

    check_table, image_in_a_row = check_image_in_table(node)
    if check_table :
        width_cell = MAX_WIDTH/image_in_a_row
        if node.width > width_cell:
            if node.height != 0:
                height = int(float(width_cell / node.width) * node.height)
            width = width_cell
    else: 
        if node.width > MAX_WIDTH:
            if node.height != 0:
                height = int(float(MAX_WIDTH / node.width) * node.height)
            width = MAX_WIDTH

    params = 'width=%spx,height=%spx' % (width, height)

    # Output 'small' images as ordinary graphics instead of some fancy type
    threshold = 30
    if node.width < threshold or node.height < threshold:
        command = u'includegraphics'

    #make sure if image is an equation image or inline_image, the command will be 'includegraphics'
    if node.equation_image == True or node.inline_image == True:
        command = u'includegraphics'

    return params, command

def check_image_in_table(node):
    """
    check if image is located inside table
    """
    parent = node.__parent__
    while parent is not None:
        if ICell.providedBy(parent):
            if IRow.providedBy(parent.__parent__):
                return True, parent.__parent__.number_of_col
        else:
            parent = parent.__parent__
    return False, 0

def check_image_in_sidebar(self):
    """
    check if image is located inside sidebar
    """
    parent = self.__parent__
    sidebar = [ISidebar, IOpenstaxNote, IOpenstaxExampleNote, IOpenstaxNoteBody]
    while parent is not None:
        for IType in sidebar:
            if IType.providedBy(parent):
                return True
        parent = parent.__parent__
    return False


def render_docx_image(context, node):
    command = u'ntiincludeannotationgraphics'
    params, command = set_image_params_and_command(node,command)
    context.write(u'\\')
    context.write(command)
    context.write(u'[')
    context.write(params)
    context.write(u']')
    context.write(u'{')
    context.write(node.path)
    context.write(u'}')
    return node


def render_figure(context, node):
    caption = u''
    title = u''
    label = u''
    if node.caption:
        caption = get_variant_field_string_value(node.caption).rstrip()
    else:
        caption = get_variant_field_string_value(node.image_alt).rstrip()
    
    if node.title:
        title = get_variant_field_string_value(node.title).rstrip()
    
    if node.label:
        label = get_variant_field_string_value(node.label).rstrip()
         
    context.write(u'\\begin{figure}\n\\begin{center}\n')
    if title:
        title = u'\\textbf{%s}\\\\\n' %(title)
        context.write(title)
    render_children(context, node)
    if caption:
        context.write(u'\\caption{')
        context.write(caption)
        context.write(u'}\n')
    if label:
        context.write(u'\\label{')
        context.write(label)
        context.write(u'}')
    context.write(u'\n\\end{center}\n\\end{figure}\n')
    return node

@component.adapter(IImage)
@interface.implementer(IRenderer)
class ImageRenderer(object):

    __slots__ = ('node',)

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None, *args, **kwargs):
        node = self.node if node is None else node
        if node.annotation:
            return render_image_annotation(context, node)
        else:
            return render_image_noannotation(context, node)
    __call__ = render

@component.adapter(IFigure)
@interface.implementer(IRenderer)
class FigureRenderer(object):

    __slots__ = ('node',)

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None, *args, **kwargs):
        node = self.node if node is None else node
        return render_figure(context, node)
    __call__ = render

@component.adapter(IDocxImage)
@interface.implementer(IRenderer)
class DocxImageRenderer(object):

    __slots__ = ('node',)

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None, *args, **kwargs):
        node = self.node if node is None else node
        return render_docx_image(context, node)
    
    __call__ = render