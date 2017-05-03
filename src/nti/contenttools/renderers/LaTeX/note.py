#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_node
from nti.contenttools.renderers.LaTeX.base import render_children
from nti.contenttools.renderers.LaTeX.base import render_environment
from nti.contenttools.renderers.LaTeX.base import render_children_output

from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import INote
from nti.contenttools.types.interfaces import ISidebar
from nti.contenttools.types.interfaces import IBlockQuote
from nti.contenttools.types.interfaces import IOpenstaxNote
from nti.contenttools.types.interfaces import INoteInteractive
from nti.contenttools.types.interfaces import IOpenstaxNoteBody
from nti.contenttools.types.interfaces import IOpenstaxExampleNote


def render_sidebar(context, node):
    base = render_children_output(node)

    # this is useful for glossary term
    # (for example glossary term in IFSTA epub)
    if node.type == u"sidebar_term":
        str_pos = base.find('-')
        if str_pos > -1:
            term = base[0:str_pos].strip()
            if node.title is None:
                node.title = term
            if node.label is None:
                node.label = u'sidebar_term:%s' % term.replace(u" ", u"_")
        node.base = base

    title = label = u''
    if node.title:
        title = get_variant_field_string_value(node.title)
        title = title.rstrip()
    if node.label:
        label = get_variant_field_string_value(node.label)
        if label:
            label = u'\\label{%s}' % (label)
            node.label = label

    context.write(u'\n\\begin{sidebar}')

    found_math_env = False
    if any(chars in title for chars in [u'\\(', u'\\[']):
        logger.warn("Math element found in sidebar's title. "
                    "It may cause issues while rendering, therefore no "
                    "title for this sidebar. Use textbf to write title in sidebar body")
        found_math_env = True
        context.write(u'{}\n')
    else:
        context.write(u'{')
        context.write(title)
        context.write(u'}\n')
    context.write(label)
    if found_math_env:
        context.write(u'\\textbf{')
        context.write(title)
        context.write(u'}\n')
    context.write(base)
    context.write(u'\n\\end{sidebar}\n')
    return node


def render_blockquote(context, node):
    return render_environment(context, u'quote', node)


def render_note(context, node):
    base = render_children_output(node)
    if base:
        context.write(u'\\footnote{')
        context.write(base)
        context.write(u'}')
    return node


def render_note_interactive(context, node):
    new_image_path = node.complete_image_path
    if not new_image_path:
        new_image_path = u'images/%s' % (node.image_path)

    caption = get_variant_field_string_value(node.caption)
    notes = get_variant_field_string_value(node.notes)

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


def render_openstax_note(context, node):
    context.write(u'\n\\begin{sidebar}{')
    if node.title:
        title = get_variant_field_string_value(node.title).rstrip()
        context.write(title)
    context.write(u'}\n')

    if node.label:
        label = get_variant_field_string_value(node.label).rstrip()
        if label:
            context.write(u'\\label{')
            context.write(label)
            context.write(u'}\n')
    render_node(context, node.body)
    context.write(u'\n\\end{sidebar}\n')
    return node


def render_openstax_example_note(context, node):
    return render_openstax_note(context, node)


def render_openstax_note_body(context, node):
    return render_children(context, node)


@interface.implementer(IRenderer)
class RendererMixin(object):

    func = None

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None):
        node = self.node if node is None else node
        return self.func(context, node)
    __call__ = render


@component.adapter(ISidebar)
class SidebarRenderer(RendererMixin):
    func = staticmethod(render_sidebar)


@component.adapter(IBlockQuote)
class BlockQuoteRenderer(RendererMixin):
    func = staticmethod(render_blockquote)


@component.adapter(INote)
class NoteRenderer(RendererMixin):
    func = staticmethod(render_note)


@component.adapter(INoteInteractive)
class NoteInteractiveRenderer(RendererMixin):
    func = staticmethod(render_note_interactive)


@component.adapter(IOpenstaxNote)
class OpenstaxNoteRenderer(RendererMixin):
    func = staticmethod(render_openstax_note)


@component.adapter(IOpenstaxExampleNote)
class OpenstaxExampleNoteRenderer(RendererMixin):
    func = staticmethod(render_openstax_example_note)


@component.adapter(IOpenstaxNoteBody)
class OpenstaxNoteBodyRenderer(RendererMixin):
    func = staticmethod(render_openstax_note_body)
