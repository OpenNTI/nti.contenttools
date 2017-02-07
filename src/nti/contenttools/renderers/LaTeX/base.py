#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component

from nti.contenttools.renderers.interfaces import IRenderer


def render_iterable(context, iterabe):
    for node in iterabe or ():
        renderer = component.getAdapter(node,
                                        IRenderer,
                                        name=context.name)
        renderer.render(context, node)


def render_children(context, node):
    render_iterable(context, node.children or ())
    return node
