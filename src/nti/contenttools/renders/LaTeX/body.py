#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: views.py 44701 2014-07-29 20:30:15Z carlos.sanchez $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .base import _environment_renderer

def body_renderer(self):
    return _environment_renderer(self, 'document', '')
