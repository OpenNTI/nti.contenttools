#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: media.py 106584 2017-02-15 04:19:57Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IDocxImage
from nti.contenttools.types.interfaces import IImage
from nti.contenttools.types.interfaces import IVideo
from nti.contenttools.types.interfaces import IFigure

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties

@interface.implementer(IImage)
class Image(DocumentStructureNode):
    createFieldProperties(IImage)

@interface.implementer(IDocxImage)
class DocxImage(Image):
    createFieldProperties(IDocxImage)

@interface.implementer(IVideo)
class Video(DocumentStructureNode):
    createFieldProperties(IVideo)

@interface.implementer(IFigure)
class Figure(DocumentStructureNode):
    createFieldProperties(IFigure)
    
    def set_caption(self, caption):
        self.caption = caption

    def set_label(self, label):
        self.label = label