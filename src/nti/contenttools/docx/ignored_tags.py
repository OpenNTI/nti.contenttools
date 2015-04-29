#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import properties as docx

doc_main_prefix = docx.nsprefixes['w']

IGNORED_TAGS = {
		'{%s}ind' %(doc_main_prefix),
		'{%s}sectPr' %(doc_main_prefix),
		'{%s}proofErr' %(doc_main_prefix),
		'{%s}noProof' %(doc_main_prefix),
		'{%s}commentReference' %(doc_main_prefix),
		'{%s}commentRangeEnd' %(doc_main_prefix),
		'{%s}commentRangeStart' %(doc_main_prefix),
		'{%s}bookmarkEnd' %(doc_main_prefix),
		'{%s}bookmarkStart' %(doc_main_prefix),
		'{%s}shd' %(doc_main_prefix),
		'{%s}contextualSpacing' %(doc_main_prefix),
		'{%s}tabs' %(doc_main_prefix),
		'{%s}highlight' %(doc_main_prefix),
		'{%s}jc' %(doc_main_prefix),
		'{%s}keepNext' %(doc_main_prefix),
		'{%s}outlineLvl' %(doc_main_prefix),
		'{%s}lastRenderedPageBreak' %(doc_main_prefix),
		'{%s}shd' %(doc_main_prefix),
		'{%s}spacing' %(doc_main_prefix),
		'{%s}autoSpaceDE' %(doc_main_prefix),
		'{%s}autoSpaceDN' %(doc_main_prefix),
		'{%s}adjustRightInd' %(doc_main_prefix),
		#'{%s}tab' %(doc_main_prefix),
		'{%s}rtl' %(doc_main_prefix) 
}
