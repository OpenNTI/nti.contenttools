#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.schema.field import ValidTextLine


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


class IRenderContext(interface.Interface):

    name = ValidTextLine(title="renderer",
                         required=True,
                         default='LaTeX')

    def write(data):
        """
        Write the specified data

        :param data Data to save
        """

    def get(name, default):
        """
        Return a property with the given name

        :param name propert name
        """

    def set(name, value):
        """
        Set property value

        :param name: Property name
        :param value: Property value
        """
