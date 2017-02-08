#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from six import string_types

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_output
from nti.contenttools.renderers.LaTeX.base import render_children
from nti.contenttools.renderers.LaTeX.base import render_children_output

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import IChapter
from nti.contenttools.types.interfaces import ISection
from nti.contenttools.types.interfaces import ISubSection
from nti.contenttools.types.interfaces import ISubSubSection
from nti.contenttools.types.interfaces import ISubSubSubSection
from nti.contenttools.types.interfaces import ISubSubSubSubSection


def get_title(context):
    if isinstance(context, string_types):
        result = context
    elif context is not None:
        result = render_output(context).strip()
    else:
        result = u''
    return result


def get_label(context):
    if isinstance(context, string_types):
        result = u'\\label{%s}' % (context)
    elif context is not None:
        result = render_output(context).strip()
    else:
        result = u''
    return result


def render_subsubsubsubsection(context, node):
    context.write('\\subsubsubsubsection{')
    output = render_children_output(node)
    context.write(output.strip())
    context.write('}\n')
    return node


def render_subsubsubsection(context, node):
    context.write('\\subsubsubsection{')
    output = render_children_output(node)
    context.write(output.strip())
    context.write('}\n')
    return node


def render_subsubsection(context, node):
    title = get_title(node.title)
    label = get_label(node.label)
    context.write('\\subsubsection{%s}\n%s\n' % (title, label))
    render_children(context, node)
    return node


def render_subsection(context, node):
    title = get_title(node.title)
    label = get_label(node.label)
    context.write('\\subsection{%s}\n%s\n' % (title, label))
    render_children(context, node)
    return node


def render_section(context, section):
    title = get_title(section.title)
    label = get_label(section.label)
    if section.suppressed:
        context.write('\\sectiontitlesuppressed{%s}\n%s\n' % (title, label))
    else:
        context.write('\\section{%s}\n%s\n' % (title, label))
    render_children(context, section)
    return section


def render_chapter(context, chapter):
    title = get_title(chapter.title)
    label = get_label(chapter.label)
    if chapter.suppressed:
        context.write('\\chaptertitlesuppressed{%s}\n%s\n' % (title, label))
    else:
        context.write('\\chapter{%s}\n%s\n' % (title, label))
    render_children(context, chapter)
    return chapter


@interface.implementer(IRenderer)
class RendererMixin(object):

    func = None

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None):
        node = self.node if node is None else node
        return self.func(context, node)
    __call__ = render


@component.adapter(IChapter)
class ChapterRenderer(RendererMixin):
    func = staticmethod(render_chapter)


@component.adapter(ISection)
class SectionRenderer(RendererMixin):
    func = staticmethod(render_section)


@component.adapter(ISubSection)
class SubSectionRenderer(RendererMixin):
    func = staticmethod(render_subsection)


@component.adapter(ISubSubSection)
class SubSubSectionRenderer(RendererMixin):
    func = staticmethod(render_subsubsection)


@component.adapter(ISubSubSubSection)
class SubSubSubSectionRenderer(RendererMixin):
    func = staticmethod(render_subsubsubsection)


@component.adapter(ISubSubSubSubSection)
class SubSubSubSubSectionRenderer(RendererMixin):
    func = staticmethod(render_subsubsubsubsection)
