#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: __init__.py 44709 2014-07-29 20:53:29Z carlos.sanchez $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from epub import EPUBParser