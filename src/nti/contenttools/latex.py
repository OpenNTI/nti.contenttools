#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contentfragments.interfaces import ITextLatexEscaper

_escapes = []

@interface.implementer(ITextLatexEscaper)
class _ExtendedTextLatexEscaper(object):

	__slots__ = ()

	def __call__(self, text):
		escaped_text = text
		for escape in _escapes:
			escaped_text = escaped_text.replace(escape[0], escape[1])
		return escaped_text
