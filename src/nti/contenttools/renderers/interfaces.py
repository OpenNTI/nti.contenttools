#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

class IRenderContext(interface.Interface):
    """
    Renderer context
    """

class IRenderer(interface.Interface):
    """
    Marker interface for node renderers
    """

    def render(context, node, *args, **kwargs):
        """
        Render this not using the specified context
        
        :param context: A :class:`IRenderContext` object 
        :param context: A :class:`nti.contenttools.types.interfaces.INode` object to render
        """
