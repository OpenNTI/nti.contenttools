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

from nti.schema.field import Bool
from nti.schema.field import Int
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

    title = ValidTextLine(title="Document title",
                          required=True,
                          default=u'')

    author = ValidTextLine(title="Document author",
                           required=False,
                           default=u'')

    packages = ListOrTuple(ValidTextLine(title='the package'),
                           title='List of packages',
                           required=False,
                           min_length=0)


class IBody(IDocumentStructureNode):
    """
    Body Element
    """


class IEPUBBody(IDocumentStructureNode):
    """
    For EPUB Document Body
    """


class IChapter(IDocumentStructureNode):
    suppressed = Bool(title="Suppressed",
                      default=False)
    title = ValidTextLine(title="Chapter Title",
                          required=True,
                          default=u'')
    label = ValidTextLine(title="Chapter label",
                          required=True,
                          default=u'')

    def set_title(self, title):
        """
        set title
        """

    def set_label(self, label):
        """
        set label
        """


class ISection(IDocumentStructureNode):
    suppressed = Bool(title="Suppressed",
                      default=False)
    title = ValidTextLine(title="Section Title",
                          required=True,
                          default=u'')
    label = ValidTextLine(title="Section Label",
                          required=True,
                          default=u'')
    data_depth = Int(title="Data depth",
                     required=False)
    section_type = ValidTextLine(title="Section type",
                                 required=False)

    def set_title(title):
        """
        set title
        """

    def set_label(label):
        """
        set label
        """


class ISubSection(ISection):

    title = ValidTextLine(title="Section Title",
                          required=True,
                          default=u'')
    label = ValidTextLine(title="Section Label",
                          required=False)


class ISubSubSection(ISection):
    """
    SubSubSection
    """


class IParagraph(IDocumentStructureNode):

    element_type = ValidTextLine(title="Element Type",
                                 required=False)


class INewline(IDocumentStructureNode):
    """
    Newline Node
    """


class INote(IDocumentStructureNode):
    """
    Note Node
    """


class Hyperlink(IDocumentStructureNode):
    target = ValidTextLine(title="Hyperlink Target",
                           required=True,
                           default=u'')
    type = ValidTextLine(title="Hyperlink Type ",
                         required=True,
                         default=u'Normal')


class IIframe(IDocumentStructureNode):
    """
    IFrame Node
    """


class ILabel(IDocumentStructureNode):
    name = ValidTextLine(title="Label Name",
                         required=True,
                         default=u'')


class ISidebar(IDocumentStructureNode):
    title = ValidTextLine(title="Sidebar Title",
                          required=False)
    label = ValidTextLine(title="Sidebar Label",
                          required=False)
    type = ValidTextLine(title="Sidebar Type",
                         required=False)


class IBlockQuote(IDocumentStructureNode):
    source = ValidTextLine(title="Block Quote Source",
                           required=True,
                           default=u'')
