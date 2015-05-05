#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer, _command_renderer
from ... import types

"""
def chapter_renderer(self):
    if self.suppressed:
        return _command_renderer('chaptertitlesuppressed', base_renderer(self).strip() ) + u'\n'
    else:
        return _command_renderer('chapter', base_renderer(self).strip() ) + u'\n'
"""

"""
def section_renderer(self):
    if self.suppressed:
        return _command_renderer('sectiontitlesuppressed', base_renderer(self).strip() ) + u'\n'
    else:
        return _command_renderer('section', base_renderer(self).strip() ) + u'\n'
"""

def subsection_renderer(self):
    title = None
    if self.title is not None:
        if isinstance(self.title, str) or isinstance(self.title, unicode):
            title = self.title
        else : title = self.title.render().strip()
    
    label = None
    if isinstance(self.label, str):
        label = u'\\label{%s}' % (self.label)
    elif self.label is not None:
        label = self.label.render()

    if title is None or label is None:
        return _command_renderer('subsection', base_renderer(self).strip() ) + u'\n'
    else:
        return u'\\subsection{%s}\n%s\n%s' %(title, label, base_renderer(self))

    

def subsubsection_renderer(self):
    return _command_renderer('subsubsection', base_renderer(self).strip() ) + u'\n'

def subsubsubsection_renderer(self):
    return _command_renderer('subsubsubsection', base_renderer(self).strip() ) + u'\n'

def subsubsubsubsection_renderer(self):
    return _command_renderer('subsubsubsubsection', base_renderer(self).strip() ) + u'\n'

def chapter_renderer(self):
    
    if self.title is None:
        title = u''
    else:
        title = self.title

    label = u''
    if isinstance(self.label, str):
        label = u'\\label{%s}' % (self.label)
    elif self.label is not None:
        label = self.label.render()

    if self.suppressed:
        return u'\\chaptertitlesuppressed{%s%s}%s' %(title, label, base_renderer(self))
    else:
        return u'\\chapter{%s%s}%s' %(title, label, base_renderer(self))

def section_renderer(self):
    title = u''
    if isinstance (self.title, str): title = self.title 
    elif self.title is not None  : title = self.title.render().strip()

    label = u''
    if isinstance(self.label, str): label = u'\\label{%s}' % (self.label)
    elif self.label is not None:label = self.label.render().strip()
        
    if self.suppressed:
        return u'\\sectiontitlesuppressed{%s}\n%s\n%s' %(title, label, base_renderer(self))
    else:
        return u'\\section{%s}\n%s\n%s' %(title, label, base_renderer(self))
