#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)


from zope import component
from zope import interface

from nti.contenttools.interfaces import IRenderer

from nti.contenttools.types.interfaces import IRunNode

@component.adapter(IRunNode)
@interface.implementer(IRenderer)
class RunRenderer(object):

    __slots__ = ('node',)

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None, *args, **kwargs):
        node = self.node if node is None else node
    __call__ = render
