#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: views.py 44701 2014-07-29 20:30:15Z carlos.sanchez $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import base_renderer, _command_renderer

def chapter_renderer(self):
    if self.suppressed:
        return _command_renderer('chaptertitlesuppressed', base_renderer(self).strip() ) + u'\n'
    else:
        return _command_renderer('chapter', base_renderer(self).strip() ) + u'\n'

def section_renderer(self):
    if self.suppressed:
        return _command_renderer('sectiontitlesuppressed', base_renderer(self).strip() ) + u'\n'
    else:
        return _command_renderer('section', base_renderer(self).strip() ) + u'\n'

def subsection_renderer(self):
    return _command_renderer('subsection', base_renderer(self).strip() ) + u'\n'

def subsubsection_renderer(self):
    return _command_renderer('subsubsection', base_renderer(self).strip() ) + u'\n'
