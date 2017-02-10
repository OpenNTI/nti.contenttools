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

from nti.contenttools.renderers.LaTeX.base import render_command
from nti.contenttools.renderers.LaTeX.base import render_verbatim
from nti.contenttools.renderers.LaTeX.base import render_children_output

from nti.contenttools.renderers.LaTeX.utils import create_label

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.types.interfaces import IParagraph


def _label_command(context, node, command):
    render_command(context, command, node)
    context.write('\n')
    # create a label from children
    value = render_children_output(node)
    context.write(create_label(command, value))
    return node


def _chapter(context, node):
    return _label_command(context, node, 'chapter')


def _section(context, node):
    return _label_command(context, node, 'section')


def _subsection(context, node):
    return _label_command(context, node, 'subsection')


def _subsubsection(context, node):
    return render_command(context, 'subsubsection', node)


def _paragraph(context, node):
    return render_command(context, 'paragraph', node)


def _subparagraph(context, node):
    return render_command(context, 'subparagraph', node)


def _subsubparagraph(context, node):
    return render_command(context, 'subsubparagraph', node)


def _abstract(context, node):
    return render_command(context, 'abstract', node)


def _author(context, node):
    return render_command(context, 'author', node)


def _footnotetext(context, node):
    return render_command(context, 'footnotetext', node)


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


def render_paragraph(out_context, node):
    result = None
    code_style = False
    for style in node.styles or ():
        if style in STYLES:
            style_render = STYLES[style]
            context = DefaultRendererContext()
            style_render(context, node)
            result = context.read()
        elif style in [u'Code', u'cCode']:
            context = DefaultRendererContext()
            render_verbatim(context, node)
            result = context.read()
            code_style = True
        elif style in [u'Figure']:
            if not result:
                result = render_children_output(node)
            result = u'Figure : %s' % result
        elif style in [u'Tables']:
            if not result:
                result = render_children_output(node)
            result = u'\t\t%s' % result
        elif style not in IGNORED_STYLES:
            logger.warn('Unhandled paragraph style: %s' % style)

    if result and not code_style:
        result = result + u'\n\n'

    if code_style:
        result = result.replace(NEW_LINE, u'')

    if result:
        out_context.write(result)
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
