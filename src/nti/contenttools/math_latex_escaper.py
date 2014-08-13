#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: math_latex_escaper.py 44645 2014-07-29 15:15:36Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface
from .interfaces import IMathLatexEscaper

_escapes_math_tex = [(u'$', u'\\$'),
			(u'%', u'\\%'),
			(u'\xa2', u'$\\prime$'),  # \uf0
			(u'\xad', u''),
			(u'\xb5', u'$\\mu$'),
			(u'\xbd', u'$\\frac{1}{2}$'),
			(u'\xd7', u'$\\times$'),
			(u'\xf7', u'$\\div$'),
			(u'\u0391', u'$\\Alpha$'),
			(u'\u0392', u'$\\Beta$'),
			(u'\u0393', u'$\\Gamma$'),
			(u'\u0394', u'$\\Delta$'),
			(u'\u0395', u'$\\Epsilon$'),
			(u'\u0396', u'$\\Zeta$'),
			(u'\u0397', u'$\\Eta$'),
			(u'\u0398', u'$\\Theta$'),
			(u'\u0399', u'$\\Iota$'),
			(u'\u039a', u'$\\Kappa$'),
			(u'\u039b', u'$\\Lamda$'),
			(u'\u039c', u'$\\Mu$'),
			(u'\u039d', u'$\\Nu$'),
			(u'\u039e', u'$\\Xi$'),
			(u'\u039f', u'$\\Omicron$'),
			(u'\u03a0', u'$\\Pi$'),
			(u'\u03a1', u'$\\Rho$'),
			(u'\u03a3', u'$\\Sigma$'),
			(u'\u03a4', u'$\\Tau$'),
			(u'\u03a5', u'$\\Upsilon$'),
			(u'\u03a6', u'$\\Phi$'),
			(u'\u03a7', u'$\\Chi$'),
			(u'\u03a8', u'$\\Psi$'),
			(u'\u03a9', u'$\\Omega$'),
			(u'\u03b1', u'$\\alpha$'),
			(u'\u03b2', u'$\\beta$'),
			(u'\u03b3', u'$\\gamma$'),
			(u'\u03b4', u'$\\delta$'),
			(u'\u03b5', u'$\\epsilon$'),
			(u'\u03b6', u'$\\zeta$'),
			(u'\u03b7', u'$\\eta$'),
			(u'\u03b8', u'$\\theta$'),
			(u'\u03b9', u'$\\iota$'),
			(u'\u03ba', u'$\\kappa$'),
			(u'\u03bb', u'$\\lamda$'),
			(u'\u03bc', u'$\\mu$'),
			(u'\u03bd', u'$\\nu$'),
			(u'\u03be', u'$\\xi$'),
			(u'\u03bf', u'$\\omicron$'),
			(u'\u03c0', u'$\\pi$'),
			(u'\u03c1', u'$\\rho$'),
			(u'\u03c2', u'$\\sigma$'),
			(u'\u03c3', u'$\\sigma$'),
			(u'\u03c4', u'$\\tau$'),
			(u'\u03c5', u'$\\upsilon$'),
			(u'\u03c6', u'$\\phi$'),
			(u'\u03c7', u'$\\chi$'),
			(u'\u03c8', u'$\\psi$'),
			(u'\u03c9', u'$\\omega$'),
			(u'\u2013', u'-'),
			(u'\u2014', u'---'),
			(u'\u2019', u"'"),
			(u'\u201c', u'``'),
			(u'\u201d', u"''"),
			(u'\u2022', u'*'),
			(u'\u20ac', u'\\euro '),
			(u'\u2190', u'$\\leftarrow$'),
			(u'\u2191', u'$\\uparrow$'),
			(u'\u2192', u'$\\rightarrow$'),
			(u'\u2193', u'$\\downarrow$'),
			(u'\u2194', u'$\\leftrightarrow$'),
			(u'\u2195', u'$\\updownarrow$'),
			(u'\u2196', u'$\\nwarrow$'),
			(u'\u2197', u'$\\nearrow$'),
			(u'\u2198', u'$\\searrow$'),
			(u'\u2199', u'$\\swarrow$'),
			(u'\u21a9', u'$\\hookleftarrow$'),
			(u'\u21aa', u'$\\hookrightarrow$'),
			(u'\u21d0', u'$\\Leftarrow$'),
			(u'\u21d1', u'$\\Uparrow$'),
			(u'\u21d2', u'$\\Rightarrow$'),
			(u'\u21d3', u'$\\Downarrow$'),
			(u'\u21d4', u'$\\Leftrightarrow$'),
			(u'\u21d5', u'$\\UpDownarrow$'),
			(u'\u2208', u'$\\in$'),
			(u'\u220b', u'$\\ni$'),
			(u'\u2205', u'$\\$'),
			(u'\u2212', u'-'),
			(u'\u2212', u'-'),
			(u'\u221a', u'$\\surd$'),
			(u'\u221e', u'$\\infty$'),
			(u'\u2248', u'$\\approx$'),
			(u'\u2248', u'$\\approx$'),
			(u'\u2260', u'$\\neq$'),
			(u'\u2264', u'$\\le$'),
			(u'\u2265', u'$\\ge$'),
			(u'\u226a', u'$\\ll$'),
			(u'\u226b', u'$\\gg$'),
			(u'\u2282', u'$\\subset$'),
			(u'\u2283', u'$\\supset$'),
			(u'\u2229', u'$\\intersection$'),
			(u'\uf020', u' '),
			(u'\uf02c', u' '),
			(u'\uf02e', u'.'),
			(u'\uf02f', u'/'),
			(u'\uf032', u'$\\prime$'),
			(u'\uf044', u'$\\triangle$'),
			(u'\uf06c', u' '),
			(u'\uf0d0', u'$\\angle$'),
			(u'. . .', u'\\ldots '),
			(u'\u2026', u'\\ldots '),
			(u'\u22ee', u'\\vdots '),
			(u'\u22ef', u'\\cdots '),
			(u'\u22f2', u'\\ddots '),
			(u'\u00A7', u'\\S')]

def _escape_tex(text):
	escaped_text = text
	for escape in _escapes_math_tex:
		escaped_text = escaped_text.replace(_escapes_math_tex[0], _escapes_math_tex[1])
	return escaped_text

@interface.implementer(IMathLatexEscaper)
class _DefaultTextLatexEscaper(object):
	
	__slots__ = ()
	
	def __call__(self, text):
		return _escape_tex(text)
