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

from nti.contenttools.renderers.LaTeX.base import render
from nti.contenttools.renderers.LaTeX.base import render_children

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import IChapter, ISection


def get_title(context):
    if isinstance(context, string_types):
        result = context
    elif context is not None:
        result = render(context).strip()
    else:
        result = u''
    return result


def get_label(context):
    if isinstance(context, string_types):
        result = u'\\label{%s}' % (context)
    elif context is not None:
        result = render(context).strip()
    else:
        result = u''
    return result


# def subsection_renderer(self):
#     title = get_title(self.title)
#     label = get_label(self.label)
#     return u'\\subsection{%s}\n%s\n%s' % (title, label, base_renderer(self))
#
#
# def subsubsection_renderer(self):
#     title = get_title(self.title)
#     label = get_label(self.label)
#     return u'\\subsubsection{%s}\n%s\n%s' % (title, label, base_renderer(self))
#
#
# def subsubsubsection_renderer(self):
#     return _command_renderer(
#         'subsubsubsection', base_renderer(self).strip()) + u'\n'
#
#
# def subsubsubsubsection_renderer(self):
#     return _command_renderer(
#         'subsubsubsubsection', base_renderer(self).strip()) + u'\n'


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


@component.adapter(IChapter)
@interface.implementer(IRenderer)
class ChapterRenderer(object):

    __slots__ = ('chapter',)

    def __init__(self, chapter):
        self.chapter = chapter

    def render(self, context, node=None):
        chapter = self.chapter if node is None else node
        return render_chapter(context, chapter)
    __call__ = render


@component.adapter(ISection)
@interface.implementer(IRenderer)
class SectionRenderer(object):

    __slots__ = ('section',)

    def __init__(self, section):
        self.section = section

    def render(self, context, node=None):
        section = self.section if node is None else node
        return render_section(context, section)
    __call__ = render
