#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

import unittest

from nti.contenttools import latex
from nti.contentfragments.interfaces import PlainTextContentFragment
from nti.contentfragments.latex import PlainTextToLatexFragmentConverter

class TestExtendedEscapeList(unittest.TestCase):
	def test_extended_escape_chars(self):
		plain_text = u"hello from plain µ"
		latex_tex  = u"hello from plain $\\mu$"
		result_tex = PlainTextToLatexFragmentConverter(plain_text, text_scaper='extended')
		self.assertEqual(latex_tex,result_tex)

		plain_text = u"check arrow ↑"
		latex_tex  = u"check arrow $\\uparrow$"
		result_tex = PlainTextToLatexFragmentConverter(plain_text, text_scaper='extended')
		self.assertEqual(latex_tex,result_tex)

		plain_text = u"hello from plain δ Τ"
		latex_tex  = u"hello from plain $\\delta$ $\\Tau$"
		result_tex = PlainTextToLatexFragmentConverter(plain_text, text_scaper='extended')
		self.assertEqual(latex_tex,result_tex)


