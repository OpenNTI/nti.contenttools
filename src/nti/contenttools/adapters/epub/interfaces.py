#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

from zope import interface


class IChildProcessor(interface.Interface):
    """
    Utility to process a child node
    """

    def process(child, node, element, epub=None):
        pass
