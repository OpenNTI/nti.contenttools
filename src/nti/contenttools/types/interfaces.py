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

from dolmen.builtins.interfaces import IIterable

from nti.schema.field import Object
from nti.schema.field import ListOrTuple
from nti.schema.field import ValidTextLine
from nti.schema.field import IndexedIterable


class _INode(interface.Interface):
    """
    Basic interface for nodes
    """


class INode(_INode, IIterable, IContained):

    children = IndexedIterable(Object(_INode, title='the node'),
                               title='List of nodes',
                               required=False,
                               min_length=0)

    def add(node):
        """
        add a node
        """

    def remove(node):
        """
        remove a node
        """

    def render(context):
        """
        Render this node using the specified context

        :param context: A :class:`nti.contenttools.interfaces.IRenderContext` object 
        """


class IDocumentStructureNode(INode):

    styles = ListOrTuple(ValidTextLine(title='the style'),
                         title='List of styles',
                         required=False,
                         min_length=0)

    def add_style(style):
        """
        add a style
        """
    addStyle = add_style

    def remove_style(node):
        """
        remove a style
        """
    removeStyle = remove_style


class IRunNode(IDocumentStructureNode):

    element_type = ValidTextLine(title="Element type",
                                 required=False)


class IDocument(IDocumentStructureNode):

    doc_type = ValidTextLine(title="Document type",
                             required=True,
                             default=u'book')

    title = ValidTextLine(title="Document type",
                          required=True,
                          default=u'')

    author = ValidTextLine(title="Document author",
                           required=False,
                           default=u'')

    packages = ListOrTuple(ValidTextLine(title='the package'),
                           title='List of packages',
                           required=False,
                           min_length=0)
