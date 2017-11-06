#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component
from zope import interface

from nti.contenttools.renderers.LaTeX.base import render_command
from nti.contenttools.renderers.LaTeX.base import render_children
from nti.contenttools.renderers.LaTeX.base import render_verbatim

from nti.contenttools.renderers.LaTeX.utils import create_label

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.types.interfaces import IParagraph

logger = __import__('logging').getLogger(__name__)


def _label_command(context, node, command):
    render_command(context, command, node)
    if node.label:  # check for label
        context.write(u'\n')
        if u'\\label{' in node.label:
            context.write(node.label)
        else:
            context.write(create_label(command, node.label))
    return node


def _chapter(context, node):
    return _label_command(context, node, u'chapter')


def _section(context, node):
    return _label_command(context, node, u'section')


def _subsection(context, node):
    return _label_command(context, node, u'subsection')


def _subsubsection(context, node):
    return render_command(context, u'subsubsection', node)


def _paragraph(context, node):
    return render_command(context, u'paragraph', node)


def _subparagraph(context, node):
    return render_command(context, u'subparagraph', node)


def _subsubparagraph(context, node):
    return render_command(context, u'subsubparagraph', node)


def _abstract(context, node):
    return render_command(context, u'abstract', node)


def _author(context, node):
    return render_command(context, u'author', node)


def _footnotetext(context, node):
    return render_command(context, u'footnotetext', node)


STYLES = {
    'Heading1': _chapter,
    'Heading2': _section,
    'Heading3': _subsection,
    'Heading4': _subsubsection,
    'Heading5': _paragraph,
    'Heading6': _subparagraph,
    'Heading7': _subsubparagraph,
    'Chapter': _chapter,
    'Section': _section,
    'Subsection': _subsection,
    'Subsubsection': _subsubsection,
    'Abstract': _abstract,
    'Authors': _author,
    'BookHead1': _section,
    'BookHead2': _subsection,
    'BookHead3': _subsubsection,
    'Bookhead4': _paragraph,
}

IGNORED_STYLES = (
    'ListParagraph',
    'Subtitle',
    'NormalWeb',
    'DefaultParagraphFont',
    'TableParagraph',
    'BodyText',
    'para'
)

NEW_LINE = u'\\newline'


def render_newline_(context):
    context.write(u'%s\n' % NEW_LINE)


def render_paragraph(context, node):
    result = True
    code_style = False
    styles = list(node.styles or ())
    if len(styles) > 1:
        logger.warn("Multiple style in paragraph node, %s",
                    styles)
    style = styles[0] if styles else None

    # handle styles
    if style is None:
        result = False
    elif style in STYLES:
        style_render = STYLES[style]
        style_render(context, node)
    elif style in [u'Code', u'cCode']:
        temp_context = DefaultRendererContext()
        render_verbatim(temp_context, node)
        data = context.read()
        if data:
            result.replace(NEW_LINE, u'')
            context.write(result)
        else:
            result = False
        code_style = True
    elif style in [u'Figure']:
        context.write(u'Figure : ')
        render_children(context, node)
    elif style in [u'Tables']:
        context.write(u'\t\t')
        render_children(context, node)
    elif style not in IGNORED_STYLES:
        logger.warn('Unhandled paragraph style: %s' % style)
        result = False

    if not result:
        result = True
        render_children(context, node)

    if result and not code_style:
        context.write(u'\n\n')
    return node


@component.adapter(IParagraph)
@interface.implementer(IRenderer)
class ParagraphRenderer(object):

    __slots__ = ('node',)

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None):
        node = self.node if node is None else node
        return render_paragraph(context, node)
    __call__ = render
