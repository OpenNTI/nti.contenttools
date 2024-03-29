#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ... import types
from .run_adapter import check_child
from .run_adapter import check_element_text
from .run_adapter import check_element_tail


class Code (types.Code):

    @classmethod
    def process(cls, element):
        me = cls()
        me = check_element_text(me, element)
        me = check_child(me, element)
        me = check_element_tail(me, element)
        return me
