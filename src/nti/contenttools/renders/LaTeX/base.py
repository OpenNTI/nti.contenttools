#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

def base_renderer(self):
    result = []
    for child in self.children:
        result.append(child.render())
    return ''.join(result)

def _command_renderer(command, arg, optional=''):
    if optional is not '':
        optional = u'[%s]' % optional
    return u'\\%s%s{%s}' % (command, optional, arg)

def _environment_renderer( self, element, optional ):
    body = base_renderer(self)
    return u'\\begin{%s}%s\n%s\n\\end{%s}\n' % ( element, optional, body, element)

def _code_renderer(self):
	body = base_renderer(self)
	if len(body) > 0 : body =  u'\\begin{verbatim}\n%s\n\\end{verbatim}\n' % (body)
	return body	

