#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import INote
from nti.contenttools.types.interfaces import INoteInteractive
from nti.contenttools.types.interfaces import INoteInteractiveImage

from nti.contenttools.types.interfaces import IOpenstaxNote
from nti.contenttools.types.interfaces import IOpenstaxNoteBody
from nti.contenttools.types.interfaces import IOpenstaxExampleNote

from nti.contenttools.types.interfaces import ISidebar

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties

@interface.implementer(ISidebar)
class Sidebar(DocumentStructureNode):
    createFieldProperties(ISidebar)

@interface.implementer(INote)
class Note(DocumentStructureNode):
    createFieldProperties(INote)


@interface.implementer(INoteInteractive)
class NoteInteractive(DocumentStructureNode):
    createFieldProperties(INoteInteractive)

    def set_image_path(self, image_path):
        self.image_path = image_path

    def set_label(self, label):
        self.label = label

    def set_link(self, link):
        self.link = link

    def set_caption(self, caption):
        self.caption = caption

    def set_notes(self, notes):
        self.notes = notes


@interface.implementer(INoteInteractiveImage)
class NoteInteractiveImage(DocumentStructureNode):
    createFieldProperties(INoteInteractiveImage)


@interface.implementer(IOpenstaxNote)
class OpenstaxNote(DocumentStructureNode):
    createFieldProperties(IOpenstaxNote)

    def set_title(self, title):
        self.title = title

    def set_body(self, body):
        self.body = body

    def set_label(self, label):
        self.label = label


@interface.implementer(IOpenstaxExampleNote)
class OpenstaxExampleNote(OpenstaxNote):
    createFieldProperties(IOpenstaxExampleNote)


@interface.implementer(IOpenstaxNoteBody)
class OpenstaxNoteBody(DocumentStructureNode):
    createFieldProperties(IOpenstaxNoteBody)
