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


def subsection_renderer(self):
    title = get_title(self.title)
    label = get_label(self.label)    
    return u'\\subsection{%s}\n%s\n%s' %(title, label, base_renderer(self))

def subsubsection_renderer(self):
    title = get_title(self.title)
    label = get_label(self.label)
    return u'\\subsubsection{%s}\n%s\n%s' %(title, label, base_renderer(self))

def subsubsubsection_renderer(self):
    return _command_renderer('subsubsubsection', base_renderer(self).strip() ) + u'\n'

def subsubsubsubsection_renderer(self):
    return _command_renderer('subsubsubsubsection', base_renderer(self).strip() ) + u'\n'

def chapter_renderer(self):
    title = get_title(self.title)
    label = get_label(self.label)
    if self.suppressed:
        return u'\\chaptertitlesuppressed{%s%s}%s' %(title, label, base_renderer(self))
    else:
        return u'\\chapter{%s%s}%s' %(title, label, base_renderer(self))

def section_renderer(self):
    title = get_title(self.title)
    label = get_label(self.label)
    if self.suppressed:
        return u'\\sectiontitlesuppressed{%s}\n%s\n%s' %(title, label, base_renderer(self))
    else:
        return u'\\section{%s}\n%s\n%s' %(title, label, base_renderer(self))

def get_title(node_title):
    title = u''
    if isinstance (node_title, str) or isinstance(node_title, unicode): title = node_title
    elif node_title is not None  : title = node_title.render().strip()
    return title

def get_label(node_label):
    label = u''
    if isinstance(node_label, str): label = u'\\label{%s}' % (node_label)
    elif node_label is not None:label = node_label.render().strip()
    return label
