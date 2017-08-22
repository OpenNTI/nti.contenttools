#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: interfaces.py 113521 2017-05-24 14:27:07Z carlos.sanchez $
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface


class IChildProcessor(interface.Interface):
    """
    Utility to process a child node
    """

    def process(child, node, element, epub=None):
        pass
