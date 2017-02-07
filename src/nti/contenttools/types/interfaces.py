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

from nti.schema.field import Int
from nti.schema.field import Bool
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

    def set_title(title):
        """
        set title
        """

    def set_label(label):
        """
        set label
        """


class ISection(IDocumentStructureNode):

    suppressed = Bool(title="Suppressed",
                      default=False,
                      required=False)

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


class ISubSubSubSection(ISection):
    """
    SubSubSubSection
    """


class ISubSubSubSubSection(ISection):
    """
    SubSubSubSubSection
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

    type = ValidTextLine(title="Table Type",
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

    type = ValidTextLine(title="Row Type",
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


class IMath(IDocumentStructureNode):

    equation_type = ValidTextLine(title="Equation Type",
                                  required=False)


class IMRow(IDocumentStructureNode):
    """
    Node for MathML element <mrow>
    """


class IMSup(IDocumentStructureNode):
    """
    Node for MathML element <msup>
    """


class IMSub(IDocumentStructureNode):
    """
    Node for MathML element <>
    """


class IMSubSup(IDocumentStructureNode):
    """
    Node for MathML element <msubsup>
    """


class IMathRun(IDocumentStructureNode):
    """
    Node covering general MathML element
    """


class IMFenced(IDocumentStructureNode):
    """
    Node for MathML element <mfence>
    """
    opener = ValidTextLine(title="Open mfence",
                           required=True,
                           default=u'')

    close = ValidTextLine(title="Close mfence",
                          required=True,
                          default=u'')

    separators = ValidTextLine(title="Separator",
                               required=True,
                               default=u'')


class IMSpace(IDocumentStructureNode):

    width = Int(title="Width",
                required=True,
                default=0)

    height = Int(title="Height",
                 required=True,
                 default=0)


class IMTable(IDocumentStructureNode):

    number_of_col = Int(title="Number of column",
                        required=True,
                        default=0)

    def set_number_of_col(number_of_col):
        """
        set number of column
        """


class IMtr(IDocumentStructureNode):

    number_of_col = Int(title="Number of column",
                        required=True,
                        default=0)

    def set_number_of_col(number_of_col):
        """
        set number of column
        """


class IMtd (IDocumentStructureNode):
    """
    Node for MathML element <mtd>
    """


class IMFrac(IDocumentStructureNode):
    """
    Node for MathML element <mfrac>
    """


class IMsqrt(IDocumentStructureNode):
    """
    Node for MathML element <msqrt>
    """


class IMRoot(IDocumentStructureNode):
    """
    Node for MathML element <mroot>
    """


class IMUnder(IDocumentStructureNode):
    """
    Node for MathML element <munder>
    """


class IMUnderover(IDocumentStructureNode):
    """
    Node for MathML element <munderover>
    """


class IMOver(IDocumentStructureNode):
    """
    Node for MathML element <mover>
    """


class IMMenclose(IDocumentStructureNode):

    notation = ListOrTuple(title="Notation",
                           required=False)


class IMMprescripts(IDocumentStructureNode):

    sub = Object(IMSub, title="subscript",
                 required=False)

    sup = Object(IMSup, title="superscript",
                 required=False)


class IMMultiscripts(IDocumentStructureNode):
    """
    To do  : double check base and prescripts type
    """
    base = Object(IDocumentStructureNode, title="base",
                  required=False)
    prescripts = Object(IMMprescripts, title="prescript",
                        required=False)


class IMText(IDocumentStructureNode):
    """
    Node for handling text in MathML element
    """


class IOMath(IDocumentStructureNode):
    """
    Main node for ooxml element <o:math>
    """


class IOMathRun(IDocumentStructureNode):
    """
    Run type node for ooxml element
    """


class IOMathFrac(IDocumentStructureNode):

    frac_type = ValidTextLine(title="Fraction Type",
                              required=False)

    def set_frac_type(frac_type):
        """
        set fraction type
        """


class IOMathNumerator(IDocumentStructureNode):
    """
    Node for ooxml element <m:num>
    """


class IOMathDenominator(IDocumentStructureNode):
    """
    Node for ooxml element <m:den>
    """


class IOMathRadical(IDocumentStructureNode):
    """
    Node for ooxml element <m:rad>
    """


class IOMathDegree(IDocumentStructureNode):
    """
    Node for ooxml element <m:deg>
    """


class IOMathBase(IDocumentStructureNode):
    """
    Node for ooxml element <m:e>
    """


class IOMathSuperscript(IDocumentStructureNode):
    """
    Node for ooxml element <m:sSup>
    """


class IOMathSup(IDocumentStructureNode):
    """
    Node for ooxml element <m:sup>
    """


class IOMathSubscript(IDocumentStructureNode):
    """
    Node for ooxml element <m:sSub>
    """


class IOMathSub(IDocumentStructureNode):
    """
    Node for ooxml element <m:sub>
    """


class IOMathSubSup(IDocumentStructureNode):
    """
    Node for ooxml element <m:sSubSup>
    """


class IOMathNary(IDocumentStructureNode):
    """
    Node for ooxml element <m:nary>
    """


class IOMathNaryPr(IDocumentStructureNode):
    """
    Node for ooxml element <m:naryPr>
    """
    chrVal = ValidTextLine(title="chrValue",
                           required=False)

    limLocVal = ValidTextLine(title="lim location value",
                              required=False)

    def set_chr_val(chrVal):
        """
        set chrVal
        """

    def set_lim_loc_val(limLocVal):
        """
        set limLocVal
        """


class IOMathDelimiter(IDocumentStructureNode):
    """
    Node for ooxml element <m:d>
    """


class IOMathDPr(IDocumentStructureNode):
    """
    Node for ooxml element <m:dPr>
    """
    begChr = ValidTextLine(title="Beginning Char",
                           required=False)

    endChr = ValidTextLine(title="End Char",
                           required=False)

    def set_beg_char(begChr):
        """
        set beginning char
        """

    def set_end_char(endChr):
        """
        set end char
        """


class IOMathLimLow(IDocumentStructureNode):
    """
    Node for ooxml element <m:limlow>
    """


class IOMathBar(IDocumentStructureNode):
    """
    Node for ooxml element <m:bar>
    """
    pos = ValidTextLine(title="Position",
                        required=False)

    def set_bar_pos(pos):
        """
        set position
        """


class IOMathAcc(IDocumentStructureNode):
    """
    Node for ooxml element  <m:acc>
    """
    accChr = ValidTextLine(title="accChr",
                           required=False)

    def set_acc_chr(accChr):
        """
        set accChr
        """


class IOMathPara(IDocumentStructureNode):
    """
    Node for ooxml element <m:OMathPara>
    """

# handling matrix for docx


class IOMathMatrix(IDocumentStructureNode):
    """
    Node for ooxml element <m:m>
    """
    begChr = ValidTextLine(title="Beginning Char",
                           required=False)

    endChr = ValidTextLine(title="End Char",
                           required=False)

    number_of_col = Int(title="Number of Column",
                        required=True,
                        default=0)

    number_of_row = Int(title="Number of Row",
                        required=True,
                        default=0)

    def set_number_of_col(number_of_col):
        """
        set number of column
        """

    def set_number_of_row(number_of_row):
        """
        set number of row
        """

    def set_beg_char(begChr):
        """
        set beginning char
        """

    def set_end_char(endChr):
        """
        set end char
        """

# handling matrix row


class IOMathMr (IDocumentStructureNode):
    """
    Node for ooxml element <m:mr>
    """

# omath: handling function apply function


class IOMathFunc(IDocumentStructureNode):
    """
    Node for ooxml element <m:func>
    """


class IOMathFName(IDocumentStructureNode):
    """
    Node for ooxml element <m:fName>
    """

# omath : handling equation-array function


class IOMathEqArr(IDocumentStructureNode):
    """
    Node for ooxml element <m:eqArr>
    """
    rowspace = Int(title="Row Space",
                   required=True,
                   default=1)

    def set_row_space(rowSpace):
        """
        set row space
        """


class IOMathSPre(IDocumentStructureNode):
    """
    Node for ooxml element <m:sPre>
    """


class IOMathBox(IDocumentStructureNode):
    """
    Node for ooxml element <m:box>
    """


class IOMathGroupChr(IDocumentStructureNode):
    """
    Node for ooxml element <m:groupChr>
    """
    pos = ValidTextLine(title="Position",
                        required=False)

    groupChr = ValidTextLine(title="group Chr",
                             required=False)

    vertJc = ValidTextLine(title="Vertical Jc",
                           required=False)

    def set_groupChr(groupChr):
        """
        set group Chr
        """

    def set_pos(pos):
        """
        set position
        """

    def set_vertJc(vertJc):
        """
        set vertical Jc
        """


class IOMathLimUpp(IDocumentStructureNode):
    """
    Node for ooxml element <m:limUpp>
    """


class IOMathBorderBox(IDocumentStructureNode):
    """
    Node for ooxml element <m:borderBox>
    """
