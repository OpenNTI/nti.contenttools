#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.location.interfaces import IContained

from nti.contenttools.types.interfaces import INode


@interface.implementer(INode, IContained)
class Node(object):

    __name__ = None
    __parent__ = None

    children = ()

    def add(self, child):
        if self.children == ():
            self.children = []
        if isinstance(child, Node):
            self.children.append(child)
            child.__parent__ = self
    add_child = add

    def remove(self, child):
        self.children.remove(child)
        child.__parent__ = None
    remove_child = remove

    def render(self, context=None):
        result = u''

        if not hasattr(self, 'children'):
            return self

        for child in self:
            result = result + child.render()

        return result

    def __iter__(self):
        current_item = 0
        while (current_item < len(self.children)):
            yield self.children[current_item]
            current_item += 1
_Node = Node


class DocumentStructureNode(Node):

    STYLES = {}

    def __init__(self):
        super(DocumentStructureNode, self).__init__()
        self.styles = []

    def raw(self):
        val = u''
        for child in self:
            if hasattr(child, 'raw'):
                val = val + child.raw()
            else:
                val = val + child
        return val

    def addStyle(self, style):
        self.styles.append(style)

    def removeStyle(self, style):
        self.styles.remove(style)
