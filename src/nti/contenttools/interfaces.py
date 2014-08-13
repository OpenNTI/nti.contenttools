#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: interfaces.py 44327 2014-07-27 06:48:14Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from zope import interface

class IMathLatexEscaper(interface.Interface):
	
	def __call_(text):
		"""
		scape the specifed text
		"""
