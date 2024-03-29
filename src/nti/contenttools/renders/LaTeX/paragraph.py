#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer, _command_renderer
from .code_line import verbatim_code_renderer, _code_listings_renderer

from nti.contenttools.util  import create_label

def _chapter( arg ):
    chapter_command = _command_renderer( 'chapter', arg )
    chapter_command = u'%s\n%s' %(chapter_command, create_label('chapter', arg))
    return chapter_command

def _section( arg ):
    section_command = _command_renderer( 'section', arg )
    section_command = u'%s\n%s' %(section_command, create_label('section', arg))
    return section_command

def _subsection( arg ):
    subsection_command = _command_renderer( 'subsection', arg )
    subsection_command = u'%s\n%s' %(subsection_command, create_label('subsection', arg))
    return subsection_command

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

def _footnotetext(arg):
    return _command_renderer ('footnotetext', arg)


def paragraph_renderer(self):
    STYLES = { 'Heading1': _chapter,
               'Heading2': _section,
               'Heading3': _subsection,
               'Heading4': _subsubsection,
               'Heading5': _paragraph,
               'Heading6': _subparagraph,
               'Heading7': _subsubparagraph,
               'Chapter' : _chapter,
               'Section': _section,
               'Subsection': _subsection,
               'Subsubsection': _subsubsection,
               'Abstract' : _abstract,
               'Authors': _author,
               'BookHead1' : _section,
               'BookHead2' : _subsection,
               'BookHead3' : _subsubsection,
               'Bookhead4' : _paragraph,
               }

    IGNORED_STYLES = ['ListParagraph', 'Subtitle', 'NormalWeb', 'DefaultParagraphFont', 'TableParagraph', 'BodyText', 'para']

    result = base_renderer(self)
    code_style = False
    for style in self.styles:
        if style in STYLES.keys():
            result = STYLES[style](result)
        elif style in IGNORED_STYLES:
            pass
        elif style in [u'Code', u'cCode']:
            result = verbatim_code_renderer(self)
            code_style = True
        elif style in [u'Figure']:
            result = u'Figure : %s' %result
        elif style in [u'Tables'] :
            result = u'\t\t%s' %result
        else:
            logger.warn('Unhandled paragraph style: %s' % style)

    if result and not code_style : 
        result = result + u'\n\n'

    if code_style:
        result = result.replace(u'\\newline', u'')

    return result

def newline_renderer(self):
    return u'\\newline\n'

