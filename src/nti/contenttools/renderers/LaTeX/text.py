#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: text.py 107708 2017-03-01 08:30:02Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.types.interfaces import ITextNode

@component.adapter(ITextNode)
@interface.implementer(IRenderer)
class TextNodeRenderer(object):

    __slots__ = ('node',)

    def __init__(self, node):
        self.node = node

    def render(self, context, node=None, *args, **kwargs):
        node = self.node if node is None else node
        context.write(node)
        return node
        
    __call__ = render