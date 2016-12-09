#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: __init__.py 46417 2014-08-13 16:59:06Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .string_replacer import rename_filename
from .string_replacer import create_label
