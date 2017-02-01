#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.schema.field import Object
from nti.schema.field import UniqueIterable

class IRenderContext(interface.Interface):
    """
    Renderer context
    """

class _INode(interface.Interface):
    """
    Basic interface for nodes
    """

class INode(_INode):

    children = UniqueIterable(Object(_INode, title='the node'),
                              title='List of nodes')

    def add(node):
        """
        add a ndoe
        """

    def remove(node):
        """
        remove a node
        """
        
    def render(context):
        """
        Render this not using the specified context
        
        :param context: A :class:`IRenderContext` object 
        """

class IRunNode(INode):
    """
    A run node
    """

class IRenderer(interface.Interface):
    """
    Marker interface for node renderers
    """

    def render(context, node, *args, **kwargs):
        """
        Render this not using the specified context
        
        :param context: A :class:`IRenderContext` object 
        :param context: A :class:`INode` object to render
        """
