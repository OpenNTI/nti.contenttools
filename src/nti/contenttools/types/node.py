#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import INode
from nti.contenttools.types.interfaces import IDocumentStructureNode


@interface.implementer(INode)
class Node(object):

    __name__ = None
    __parent__ = None
    children = ()
    
    def add(self, child):
        if self.children == ():
            self.children = list(self.children or ())
        if INode.providedBy(child):
            self.children.append(child)
            child.__parent__ = self # take ownership
    add_child = add

    def remove(self, child):
        self.children.remove(child)
        child.__parent__ = None
    remove_child = remove

    def render(self, context):
        for child in self:
            child.render(context)

    def __iter__(self):
        for item in self.children or ():
            yield item
_Node = Node


@interface.implementer(IDocumentStructureNode)
class DocumentStructureNode(Node):

    STYLES = {}

    def __init__(self, styles=None):
        Node.__init__(self)
        self.styles = list(styles or ())

    def raw(self):
        val = u''
        for child in self:
            if hasattr(child, 'raw'):
                val = val + child.raw()
            else:
                val = val + child
        return val

    def add_style(self, style):
        self.styles.append(style)
    addStyle = add_style

    def remove_style(self, style):
        self.styles.remove(style)
    removeStyle = remove_style
