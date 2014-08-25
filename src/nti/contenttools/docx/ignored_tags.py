#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import properties as docx

IGNORED_TAGS = {
		'{'+docx.nsprefixes['w']+'}ind',
		'{'+docx.nsprefixes['w']+'}sectPr',
		'{'+docx.nsprefixes['w']+'}proofErr',
		'{'+docx.nsprefixes['w']+'}noProof',
		'{'+docx.nsprefixes['w']+'}commentReference',
		'{'+docx.nsprefixes['w']+'}commentRangeEnd',
		'{'+docx.nsprefixes['w']+'}commentRangeStart',
		'{'+docx.nsprefixes['w']+'}bookmarkEnd',
		'{'+docx.nsprefixes['w']+'}bookmarkStart',
		'{'+docx.nsprefixes['w']+'}shd',
		'{'+docx.nsprefixes['w']+'}contextualSpacing',
		'{'+docx.nsprefixes['w']+'}tabs',
		'{'+docx.nsprefixes['w']+'}highlight',
		'{'+docx.nsprefixes['w']+'}jc',
		'{'+docx.nsprefixes['w']+'}keepNext',
		'{'+docx.nsprefixes['w']+'}outlineLvl',
		'{'+docx.nsprefixes['w']+'}lastRenderedPageBreak',
		'{'+docx.nsprefixes['w']+'}shd',
		'{'+docx.nsprefixes['w']+'}spacing',
		'{'+docx.nsprefixes['w']+'}autoSpaceDE',
		'{'+docx.nsprefixes['w']+'}autoSpaceDN',
		'{'+docx.nsprefixes['w']+'}adjustRightInd',
		'{'+docx.nsprefixes['w']+'}tab',
		'{'+docx.nsprefixes['w']+'}rtl' 
}
