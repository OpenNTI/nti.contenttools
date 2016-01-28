#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: __init__.py 50380 2014-10-02 19:24:32Z carlos.sanchez $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .html import HTMLParser