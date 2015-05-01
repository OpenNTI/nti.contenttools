#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: glossary_adapter.py 51866 2014-10-23 17:34:06Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)
from ... import types
from .run_adapter import check_child
from .run_adapter import check_element_text
from .run_adapter import check_element_tail
from .run_adapter import Run

class GlossaryTerm(types.GlossaryTerm):
	@classmethod
	def process(cls, element):
		me = cls()
		me = check_element_text(me, element)
		me = check_child(me, element)
		el = Run()
		el.add_child(me)
		el = check_element_tail(el, element)
		return el