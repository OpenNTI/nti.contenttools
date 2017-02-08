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

from nti.schema.field import SchemaConfigured

from nti.schema.fieldproperty import createFieldProperties


class NodeMixin(object):

    __name__ = None
    __parent__ = None

    children = ()

    def __iter__(self):
        for item in self.children or ():
            yield item
_Node = NodeMixin


@interface.implementer(INode)
class Node(SchemaConfigured, NodeMixin):
    createFieldProperties(INode)

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self.children = self.children or list()

    def add(self, child):
        if INode.providedBy(child):
            self.children.append(child)
            child.__parent__ = self  # take ownership
    add_child = add

    def remove(self, child):
        self.children.remove(child)
        child.__parent__ = None
    remove_child = remove

    def render(self, context):
        for child in self:
            child.render(context)


@interface.implementer(IDocumentStructureNode)
class DocumentStructureNode(Node):
    createFieldProperties(IDocumentStructureNode)

    STYLES = {}

    def __init__(self, *args, **kwargs):
        super(DocumentStructureNode, self).__init__(*args, **kwargs)
        self.styles = self.styles or list()

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
