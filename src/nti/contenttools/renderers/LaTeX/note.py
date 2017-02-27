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
    
