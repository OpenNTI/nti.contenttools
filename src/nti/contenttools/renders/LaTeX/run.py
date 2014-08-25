#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer, _command_renderer

def _textbf( arg ):
    return _command_renderer( 'textbf', arg )

def _modified( arg ):
    return _command_renderer( 'modified', arg )

def _textit( arg ):
    return _command_renderer( 'textit', arg )

def _strikeout( arg ):
    return _command_renderer( 'strikeout', arg )

def _subscript( arg ):
    return _command_renderer( 'textsubscript', arg )

def _uline( arg ):
    return _command_renderer( 'uline', arg )

def _superscript(arg):
    return _command_renderer('textsuperscript', arg)

def run_renderer(self):
    STYLES = { 'bold': _textbf,
               'inserted': _modified,
               'italic': _textit,
               'strike': _strikeout,
               'sub': _subscript,
               'underline': _uline,
               'sup': _superscript}

    result = base_renderer(self)

    for style in self.styles:
        if style in STYLES.keys():
            result = STYLES[style](result)
        else:
            print('Unhandled run style: %s' % style)

    return result
