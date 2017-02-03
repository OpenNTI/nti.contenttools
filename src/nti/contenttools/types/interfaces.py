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

from nti.schema.field import Bool, ValidText, ValidTextLine
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


class IImage(IDocumentStructureNode):
    path = ValidTextLine(title="Image Path",
                         required=True,
                         default=u'')
    caption = ValidTextLine(title="Image Caption",
                            required=True,
                            default=u'')
    width = Int(title="Image Width",
                required=True,
                default=0)
    height = Int(title="Image Height",
                 required=True,
                 default=0)
    equation_image = Bool(title="Equation Image Type",
                          required=True,
                          default=False)
    inline_image = Bool(title="Inline Image Type",
                        required=True,
                        default=False)
    predefined_image_path = Bool(title="Predifined Image Path",
                                 required=True,
                                 default=False)


class IDocxImage(IImage):
    """
    Docx Image Node
    """


class IVideo(IDocumentStructureNode):
    path = ValidTextLine(title="Video Path",
                         required=True,
                         default=u'')
    thumbnail = ValidTextLine(title="Video Thumbnail",
                              required=True,
                              default=u'')
    caption = ValidTextLine(title="Video",
                            required=True,
                            default=u'')
    width = Int(title="Video Width",
                required=True,
                default=0)
    height = Int(title="Video Height",
                 required=True,
                 default=0)


class IList(IDocumentStructureNode):
    level = ValidTextLine(title="Level",
                          required=True,
                          default=u'')
    group = ValidTextLine(title="Group",
                          required=True,
                          default=u'')
    start = Int(title="List Start Number",
                required=True,
                default=0)
    format = ValidTextLine(title="Format",
                           required=True,
                           default=u'')


class IUnorderedList(IList):
    """
    UnOrdered List
    """


class IOrderedList(IList):
    """
    Ordered List
    """


class IItem(IDocumentStructureNode):
    """
    Item List
    """


class IDescriptionList(IList):
    """
    Description List Node (a particular Node used of openstax)
    """


class ItemWithDesc(IItem):
    """
    Item list with some descriptions
    """


class IDT(IDocumentStructureNode):
    desc = ValidTextLine(title="Description",
                         required=False)
    type = ValidTextLine(title="Description Type",
                         required=False)

    def set_description(desc):
        """
        set description
        """

    def set_type(type_):
        """
        set_type
        """


class IDD(IDocumentStructureNode):
    """
    DD : Part of Description List Node
    """


class ITable(IDocumentStructureNode):
    number_of_col_header = Int(title="Number of Column Header",
                               required=True,
                               default=0)
    number_of_col_body = Int(title="Number of Column Body",
                             required=True,
                             default=0)
    caption = ValidTextLine(title="Table Caption",
                            required=False)
    label = ValidTextLine(title="Table Label",
                          required=False)
    border = ListOrTuple(title="TableBorder",
                         required=False)
    type_ = ValidTextLine(title="Table Type",
                          required=False)
    alignment = ValidTextLine(title="Table Alignment",
                              required=True,
                              default=u'left')

    def set_number_of_col_header(number_of_col_header):
        """
        set number of column header
        """

    def set_number_of_col_body(number_of_col_body):
        """
        set number of column body
        """

    def set_caption(caption):
        """
        set caption
        """

    def set_label(label):
        """
        set label
        """

    def set_border(border):
        """
        set border
        """

    def set_type(type_):
        """
        set type
        """

    def set_alignment(alignment):
        """
        set alignment
        """


class IRow(IDocumentStructureNode):
    number_of_col = Int(title="Number of Column",
                        required=True,
                        default=0)
    border = Bool(title="Border",
                  required=True,
                  default=False)
    type_ = ValidTextLine(title="Row Type",
                          required=False)

    def set_number_of_col(number_of_col):
        """
        set number of column
        """

    def set_border(border):
        """
        set border
        """

    def set_type(type_):
        """
        set type
        """


class ICell (IDocumentStructureNode):
    border = Bool(title="Border",
                  required=True,
                  default=False)
    is_first_cell_in_the_row = Bool(title="Check if it is the first cell on the row",
                                    required=True,
                                    default=False)
    colspan = Int(title="Column Span",
                  required=True,
                  default=1)

    def set_border(border):
        """
        set border
        """


class ITBody(IDocumentStructureNode):
    number_of_col = Int(title="Number of Column",
                        required=True,
                        default=0)
    border = Bool(title="Table Body Border",
                  required=True,
                  default=False)

    def set_number_of_col(number_of_col):
        """
        set number of column
        """

    def set_border(border):
        """
        set table body border
        """


class ITHead(IDocumentStructureNode):
    number_of_col = Int(title="Number of Table Header Column",
                        required=True,
                        default=0)
    border = Bool(title="Table Header Border",
                  required=True,
                  default=False)

    def set_number_of_col(number_of_col):
        """
        set number of table header column
        """

    def set_border(border):
        """
        set table header border
        """


class ITFoot(IDocumentStructureNode):
    number_of_col = Int(title="Number of Table Footer Column",
                        required=True,
                        default=0)

    def set_number_of_col(number_of_col):
        """
        set number of column
        """
