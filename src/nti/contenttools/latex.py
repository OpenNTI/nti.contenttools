#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: latex.py 44645 2014-07-29 15:15:36Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contentfragments.interfaces import ITextLatexEscaper
from nti.contenttools import unicode_to_latex

@interface.implementer(ITextLatexEscaper)
class _ExtendedTextLatexEscaper(object):
      
      __slots__ = ()
      
      def __call__(self, text):
            escaped_text = text
            for escape in _escapes:
                  escaped_text = escaped_text.replace(escape[0], escape[1])
            return escaped_text
      
_escapes = unicode_to_latex.unicode_to_latex.items()

