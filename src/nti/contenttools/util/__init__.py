#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .string_replacer import rename_filename
from .string_replacer import create_label


def merge_two_dicts(x, y):
	z = x.copy()
	z.update(y)
	return z