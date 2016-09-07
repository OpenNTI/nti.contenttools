#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: __init__.py 81889 2016-01-28 16:40:10Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools.mathcounts_parser.adapters.run_adapter import adapt
