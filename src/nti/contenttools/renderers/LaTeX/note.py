#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: note.py 107525 2017-02-27 09:43:34Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_node
from nti.contenttools.renderers.LaTeX.base import render_output
from nti.contenttools.renderers.LaTeX.base import render_children
from nti.contenttools.renderers.LaTeX.base import render_children_output

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import INote
from nti.contenttools.types.interfaces import INoteInteractive
from nti.contenttools.types.interfaces import INoteInteractiveImage

from nti.contenttools.types.interfaces import IOpenstaxNote
from nti.contenttools.types.interfaces import IOpenstaxNoteBody
from nti.contenttools.types.interfaces import IOpenstaxExampleNote


def render_note(context, node):
    base = render_children_output(node)
    if base:
        context.write(u'\\footnote{')
        context.write(base)
        context.write(u'')
    return node


def render_note_interactive(context, node):
    new_image_path = node.complete_image_path if node.complete_image_path else u'images/%s' % (
        node.image_path)

    if isinstance(node.caption, unicode) or isinstance(node.caption, str):
        caption = node.caption
    else:
        caption = render_output(node.caption).strip()

    if isinstance(node.notes, unicode) or isinstance(node.notes, str):
        notes = node.notes
    else:
        notes = render_output(node.notes).strip()

    context.write(u'\n\\begin{nticard}{')
    context.write(node.link)
    context.write(u'}\n\\label{')
    context.write(node.label)
    context.write(u'}\n\\caption{')
    context.write(caption)
    context.write(u'}\n\\includegraphics{')
    context.write(new_image_path)
    context.write(u'}\n')
    context.write(notes)
    context.write(u'\n\\end{nticard}\n')

    return node


@interface.implementer(IRenderer)
class RendererMixin(object):

    func = None

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None):
        node = self.node if node is None else node
        return self.func(context, node)
    __call__ = render


@component.adapter(INote)
class NoteRenderer(RendererMixin):
    func = staticmethod(render_note)


@component.adapter(INoteInteractive)
class NoteInteractiveRenderer(RendererMixin):
    func = staticmethod(render_note_interactive)
