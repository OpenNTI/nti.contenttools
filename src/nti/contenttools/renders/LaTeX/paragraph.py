#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer, _command_renderer

def _chapter( arg ):
    return _command_renderer( 'chapter', arg )

def _section( arg ):
    return _command_renderer( 'section', arg )

def _subsection( arg ):
    return _command_renderer( 'subsection', arg )

def _subsubsection( arg ):
    return _command_renderer( 'subsubsection', arg )

def _paragraph( arg ):
    return _command_renderer( 'paragraph', arg )

def _subparagraph( arg ):
    return _command_renderer( 'subparagraph', arg )

def _subsubparagraph( arg ):
    return _command_renderer( 'subsubparagraph', arg )

def _abstract( arg ):
    return _command_renderer( 'abstract', arg )

def _author( arg ):
    return _command_renderer( 'author', arg )


def paragraph_renderer(self):
    STYLES = { 'Heading1': _chapter,
               'Heading2': _section,
               'Heading3': _subsection,
               'Heading4': _subsubsection,
               'Heading5': _paragraph,
               'Heading6': _subparagraph,
               'Heading7': _subsubparagraph,
               'Section': _section,
               'Subsection': _subsection,
               'Abstract' : _abstract,
               'Authors': _author}

    IGNORED_STYLES = ['ListParagraph', 'Subtitle', 'NormalWeb', 'DefaultParagraphFont', 'TableParagraph', 'BodyText']

    result = base_renderer(self)

    for style in self.styles:
        if style in STYLES.keys():
            result = STYLES[style](result)
        elif style in IGNORED_STYLES:
            pass
        else:
            logger.warn('Unhandled paragraph style: %s' % style)

    if result:
        result = result + u'\n\n'


    return result

def newline_renderer(self):
    return u'\\newline '

