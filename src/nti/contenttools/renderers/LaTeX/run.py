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

from nti.contenttools.renderers.LaTeX.base import render_children
from nti.contenttools.renderers.LaTeX.base import render_children_output

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import IRunNode


def render_run_command(command, base):
    return u'\\%s{%s}' % (command, base)


def _textbf(base):
    return render_run_command('textbf', base)


def _modified(base):
    return render_run_command('modified', base)


def _textit(base):
    return render_run_command('textit', base)


def _strikeout(base):
    return render_run_command('strikeout', base)


def _subscript(base):
    return render_run_command('textsubscript', base)


def _uline(base):
    return render_run_command('uline', base)


def _superscript(base):
    return render_run_command('textsuperscript', base)


def render_run_node(context, node):
    STYLES = {'bold': _textbf,
              'inserted': _modified,
              'italic': _textit,
              'strike': _strikeout,
              'sub': _subscript,
              'underline': _uline,
              'sup': _superscript,
              'subscript': _subscript,
              'superscript': _superscript}

    IGNORED_STYLE = [
        u'apple-converted-space', u'HTMLDefinition', u'cnxn-target', u'normal']

    if node.styles:
        base = render_children_output(node)
        for style in node.styles:
            if style in STYLES.keys():
                base = STYLES[style](base)
            elif style in IGNORED_STYLE:
                pass
            else:
                logger.info('Unhandled run style: %s' % style)
        context.write(base)
    else:
        render_children(context, node)

    return node


@component.adapter(IRunNode)
@interface.implementer(IRenderer)
class RunRenderer(object):

    __slots__ = ('node',)

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None, *args, **kwargs):
        node = self.node if node is None else node
        return render_run_node(context, node)
    __call__ = render
