#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

def base_renderer(self):
	return list_renderer(self.children)

def _command_renderer(command, arg, optional=''):
    if optional is not '':
        optional = u'[%s]' % optional
    return u'\\%s%s{%s}' % (command, optional, arg)

def _environment_renderer( self, element, optional ):
    body = base_renderer(self)
    return u'\\begin{%s}%s\n%s\n\\end{%s}\n' % ( element, optional, body, element)

def list_renderer(content_list):
	result = []
	result_append = result.append
	for item in content_list:
		result_append(item.render())
	return u''.join(result)