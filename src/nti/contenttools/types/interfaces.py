#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope.location.interfaces import IContained

from nti.contentfragments.interfaces import IPlainTextContentFragment

from nti.schema.field import Int
from nti.schema.field import Bool
from nti.schema.field import Dict
from nti.schema.field import Object
from nti.schema.field import Variant
from nti.schema.field import ListOrTuple
from nti.schema.field import IndexedIterable
from nti.schema.field import TextLine as ValidTextLine


class _INode(IContained):
  """
  Basic interface for nodes
  """


class INode(_INode):

  children = IndexedIterable(Object(_INode, title=u'the node'),
                             title=u'List of nodes',
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

  def __iter__():
    """
    Return an iterator object.
    """


class ITextNode(INode, IPlainTextContentFragment):
  pass


class IDocumentStructureNode(INode):

  styles = IndexedIterable(ValidTextLine(title=u'the style'),
                           title=u'List of styles',
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

  element_type = ValidTextLine(title=u"Element type",
                               required=False)


class IRealPageNumber(IDocumentStructureNode):
  pass


class IDocument(IDocumentStructureNode):

  doc_type = ValidTextLine(title=u"Document type",
                           required=True,
                           default=u'book')

  title = ValidTextLine(title=u"Document title",
                        required=True,
                        default=u'')

  author = ValidTextLine(title=u"Document author",
                         required=False,
                         default=u'')

  packages = ListOrTuple(ValidTextLine(title=u'the package'),
                         title=u'List of packages',
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

  suppressed = Bool(title=u"Suppressed",
                    default=False)

  title = Variant((Object(IDocumentStructureNode,
                          title=u"Title"),
                   ValidTextLine(title=u"Title")),
                  required=False)

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  def set_title(title):
    """
    set title
    """

  def set_label(label):
    """
    set label
    """


class IChapterCounter(IDocumentStructureNode):
  counter_number = Variant((Int(title=u"Counter Number"),
                            ValidTextLine(title=u"Counter Number")),
                           required=True,
                           default=1)


class ISection(IDocumentStructureNode):

  suppressed = Bool(title=u"Suppressed",
                    default=False,
                    required=False)

  title = Variant((Object(IDocumentStructureNode,
                          title=u"Title"),
                   ValidTextLine(title=u"Title")),
                  required=False)

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  data_depth = Int(title=u"Data depth",
                   required=False)

  section_type = ValidTextLine(title=u"Section type",
                               required=False)


class ISubSection(ISection):
  """
  SubSubSection
  """


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

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  element_type = ValidTextLine(title=u"Element Type",
                               required=False)


class INewline(IDocumentStructureNode):
  """
  Newline Node
  """


class INote(IDocumentStructureNode):
  """
  Note Node
  """


class IHyperlink(IDocumentStructureNode):

  target = Variant((Object(IDocumentStructureNode),
                    ValidTextLine()),
                   title=u"Hyperlink Target",
                   required=False)

  type = ValidTextLine(title=u"Hyperlink Type ",
                       required=True,
                       default=u'Normal')


class IIframe(IDocumentStructureNode):
  """
  IFrame Node
  """


class ILabel(IDocumentStructureNode):

  name = ValidTextLine(title=u"Label Name",
                       required=True,
                       default=u'')


class ISidebar(IDocumentStructureNode):

  title = Variant((Object(IDocumentStructureNode),
                   ValidTextLine()),
                  title=u"Title",
                  required=False)

  label = Variant((Object(IDocumentStructureNode),
                   ValidTextLine()),
                  title=u"Label",
                  required=False)

  type = ValidTextLine(title=u"Sidebar Type",
                       required=False)

  base = ValidTextLine(title=u"The Base",
                       required=False)

  options = ValidTextLine(title=u"Options",
                          required=False)


class IBlockQuote(IDocumentStructureNode):
  source = ValidTextLine(title=u"Block Quote Source",
                         required=True,
                         default=u'')


class ICenterNode(IDocumentStructureNode):
  """
  Center env node
  """


class IImage(IDocumentStructureNode):

  path = ValidTextLine(title=u"Image Path",
                       required=True,
                       default=u'')

  caption = Variant((Object(IDocumentStructureNode),
                     ValidTextLine()), title=u"Image Caption",
                    required=True,
                    default=u'')

  width = Int(title=u"Image Width",
              required=True,
              default=0)

  height = Int(title=u"Image Height",
               required=True,
               default=0)

  equation_image = Bool(title=u"Equation Image Type",
                        required=False)

  inline_image = Bool(title=u"Inline Image Type",
                      required=False)

  predefined_image_path = Bool(title=u"Predifined Image Path",
                               required=False)

  annotation = Bool(title=u"Image Annotation",
                    required=True,
                    default=True)


class IDocxImage(IImage):
  """
  Docx Image Node
  """


class IVideo(IDocumentStructureNode):

  path = ValidTextLine(title=u"Video Path",
                       required=True,
                       default=u'')

  thumbnail = ValidTextLine(title=u"Video Thumbnail",
                            required=True,
                            default=u'')

  caption = ValidTextLine(title=u"Video",
                          required=True,
                          default=u'')

  width = Int(title=u"Video Width",
              required=True,
              default=0)

  height = Int(title=u"Video Height",
               required=True,
               default=0)


class IList(IDocumentStructureNode):

  level = ValidTextLine(title=u"Level",
                        required=True,
                        default=u'')

  group = ValidTextLine(title=u"Group",
                        required=True,
                        default=u'')

  start = Int(title=u"List Start Number",
              required=True,
              default=1)

  format = ValidTextLine(title=u"Format",
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


class IItemWithDesc(IItem):
  """
  Item list with some descriptions
  """


class IDT(IDocumentStructureNode):

  desc = Object(IDocumentStructureNode, title=u"Description",
                required=False)

  type = ValidTextLine(title=u"Description Type",
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

  number_of_col_header = Int(title=u"Number of Column Header",
                             required=True,
                             default=0)

  number_of_col_body = Int(title=u"Number of Column Body",
                           required=True,
                           default=0)
  caption = Variant((Object(IDocumentStructureNode, title=u"Table Caption"),
                     ValidTextLine(title=u"Table Caption")),
                    required=False)

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  border = Bool(title=u"TableBorder",
                default=False,
                required=True)

  type = ValidTextLine(title=u"Table Type",
                       required=False)

  alignment = ValidTextLine(title=u"Table Alignment",
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

  number_of_col = Int(title=u"Number of Column",
                      required=True,
                      default=0)

  border = Bool(title=u"Border",
                required=True,
                default=False)

  type = ValidTextLine(title=u"Row Type",
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

  border = Bool(title=u"Border",
                required=True,
                default=False)

  is_first_cell_in_the_row = Bool(title=u"Check if it is the first cell on the row",
                                  required=True,
                                  default=False)

  colspan = Int(title=u"Column Span",
                required=True,
                default=1)

  def set_border(border):
    """
    set border
    """


class ITBody(IDocumentStructureNode):

  number_of_col = Int(title=u"Number of Column",
                      required=True,
                      default=0)

  border = Bool(title=u"Table Body Border",
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

  number_of_col = Int(title=u"Number of Table Header Column",
                      required=True,
                      default=0)

  border = Bool(title=u"Table Header Border",
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

  number_of_col = Int(title=u"Number of Table Footer Column",
                      required=True,
                      default=0)

  def set_number_of_col(number_of_col):
    """
    set number of column
    """


class IConceptHierarchy(IDocumentStructureNode):
  """
  Node for Concept Hierarchy
  """


class IConcept(IDocumentStructureNode):
  """
  Node for Concept
  """
  name = Variant((Object(IDocumentStructureNode,
                         title=u"Title"),
                  ValidTextLine(title=u"Title")),
                 required=True,
                 default=u'')
  label = Variant((Object(IDocumentStructureNode,
                          title=u"Title"),
                   ValidTextLine(title=u"Title")),
                  required=False)


class IMath(IDocumentStructureNode):

  equation_type = ValidTextLine(title=u"Equation Type",
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
  Node for MathML element <msub>
  """


class IMSubSup(IDocumentStructureNode):
  """
  Node for MathML element <msubsup>
  """


class IMathRun(IDocumentStructureNode):
  """
  Node covering general MathML element
  element_type value could be : 'operator', 'numeric', 'identifier'
  adapter sets the element_type value:
      if <mn> then element_type = 'numeric'
      if <mo> then element_type = 'operator'
      if <mi> then element_type = 'identifier'
  """

  element_type = ValidTextLine(title=u"Element Type",
                               required=False)


class IMFenced(IDocumentStructureNode):
  """
  Node for MathML element <mfenced>
  """

  opener = ValidTextLine(title=u"Open mfence",
                         required=True,
                         default=u'')

  close = ValidTextLine(title=u"Close mfence",
                        required=True,
                        default=u'')

  separators = ValidTextLine(title=u"Separator",
                             required=True,
                             default=u'')


class IMSpace(IDocumentStructureNode):

  width = Int(title=u"Width",
              required=True,
              default=0)

  height = Int(title=u"Height",
               required=True,
               default=0)


class IMTable(IDocumentStructureNode):

  number_of_col = Int(title=u"Number of column",
                      required=True,
                      default=0)
  frame = ValidTextLine(title=u"Frame",
                        required=False)
  rowlines = ValidTextLine(title=u"Rowlines",
                           required=False)
  align = ValidTextLine(title=u"Align",
                        required=True,
                        default=u'')

  def set_number_of_col(number_of_col):
    """
    set number of column
    """


class IMLabeledTr(IDocumentStructureNode):
  """
  Node for MathML element <mlabeledtr>
  """


class IMtr(IDocumentStructureNode):

  number_of_col = Int(title=u"Number of column",
                      required=True,
                      default=0)
  column_align = ValidTextLine(title=u"Column Align",
                               required=False)
  row_align = ValidTextLine(title=u"Row Align",
                            required=False)

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
  Node for MathML element <MFrac>
  """


class IMsqrt(IDocumentStructureNode):
  """
  Node for MathML element <msqrt>
  """


class IMRoot(IDocumentStructureNode):
  """
  Node for MathML element <MRoot>
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
  accent = Bool(title=u'Accent',
                required=False)


class IMMenclose(IDocumentStructureNode):

  notation = Variant((ListOrTuple(title=u"Notation"),
                      ValidTextLine(title=u"Notation")),
                     required=False)


class IMMprescripts(IDocumentStructureNode):

  sub = Object(IDocumentStructureNode, title=u"subscript",
               required=False)

  sup = Object(IDocumentStructureNode, title=u"superscript",
               required=False)


class IMMultiscripts(IDocumentStructureNode):

  base = ListOrTuple(title=u"Multiscripts base",
                     required=False)

  prescripts = Object(IDocumentStructureNode, title=u"prescript",
                      required=False)


class IMText(IDocumentStructureNode):
  """
  Node for handling text in MathML element
  """


class IMNone(IDocumentStructureNode):
  """
  Node for handling <none/> element
  """


class IOMath(IDocumentStructureNode):
  """
  Main node for ooxml element <o:math>
  """


class IOMathRun(IDocumentStructureNode):
  """
  Node for ooxml element <m:r>
  """


class IOMathFrac(IDocumentStructureNode):

  frac_type = ValidTextLine(title=u"Fraction Type",
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
  chrVal = ValidTextLine(title=u"chrValue",
                         required=False)

  limLocVal = ValidTextLine(title=u"lim location value",
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
  begChr = ValidTextLine(title=u"Beginning Char",
                         required=False)

  endChr = ValidTextLine(title=u"End Char",
                         required=False)

  def set_beg_char(begChr):
    """
    set beginning char
    """

  def set_end_char(endChr):
    """
    set end char
    """


class IOMathLim(IDocumentStructureNode):
  """
  Node for ooxml element <m:lim>
  """


class IOMathLimLow(IDocumentStructureNode):
  """
  Node for ooxml element <m:limlow>
  """


class IOMathBar(IDocumentStructureNode):
  """
  Node for ooxml element <m:bar>
  """
  pos = ValidTextLine(title=u"Position",
                      required=False)

  def set_bar_pos(pos):
    """
    set position
    """


class IOMathAcc(IDocumentStructureNode):
  """
  Node for ooxml element  <m:acc>
  """
  accChr = ValidTextLine(title=u"accChr",
                         required=False)

  def set_acc_chr(accChr):
    """
    set accChr
    """


class IOMathPara(IDocumentStructureNode):
  """
  Node for ooxml element <m:OMathPara>
  """

# handling matrix property


class IOMathMPr(IDocumentStructureNode):
  """
  Node for ooxml element <m:OMathMPr>
  """


class IOMathMcs(IDocumentStructureNode):
  """
  Node for ooxml element <m:OMathMcs>
  """


class IOMathMc(IDocumentStructureNode):
  """
  Node for ooxml element <m:OMathMc>
  """


class IOMathMcPr(IDocumentStructureNode):
  """
  Node for ooxml element <m:OMathMcPr>
  """

# handling matrix for docx


class IOMathMatrix(IDocumentStructureNode):
  """
  Node for ooxml element <m:m>
  """
  begChr = ValidTextLine(title=u"Beginning Char",
                         required=False)

  endChr = ValidTextLine(title=u"End Char",
                         required=False)

  number_of_col = Variant((Int(title=u"Number of Column"),
                           ValidTextLine(title=u"Number of Column")),
                          required=True,
                          default=u'0')

  number_of_row = Variant((Int(title=u"Number of Row"),
                           ValidTextLine(title=u"Number of Row")),
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


class IOMathMr(IDocumentStructureNode):
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
  rowSpace = Int(title=u"Row Space",
                 required=True,
                 default=1)
  begBorder = ValidTextLine(title=u"Beginning Char",
                            required=False)
  endBorder = ValidTextLine(title=u"End Char",
                            required=False)

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

  pos = ValidTextLine(title=u"Position",
                      required=False)

  groupChr = ValidTextLine(title=u"group Chr",
                           required=False)

  vertJc = ValidTextLine(title=u"Vertical Jc",
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


class ICodeLine(IDocumentStructureNode):
  """
  Node for inline code
  """


class ICode(IDocumentStructureNode):
  """
  Node for code
  """


class IVerbatim(IDocumentStructureNode):
  """
  Node for verbatim style
  """


class IAlternateContent(IDocumentStructureNode):
  """
  Node for alternate content
  """


class ITextBoxContent(IDocumentStructureNode):
  """
  Node for text box content
  """


class INoteInteractive(IDocumentStructureNode):
  """
  Node for note interactive
  """

  image_path = ValidTextLine(title=u"Image path",
                             required=True,
                             default=u'')

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  link = ValidTextLine(title=u"Link",
                       required=False)

  caption = ValidTextLine(title=u"Caption",
                          required=True,
                          default=u'')

  notes = ValidTextLine(title=u"Notes",
                        required=True,
                        default=u'')

  complete_image_path = ValidTextLine(title=u"Complete image path",
                                      required=True,
                                      default=u'')

  def set_image_path(image_path):
    """
    set image path
    """

  def set_label(label):
    """
    set label
    """

  def set_link(link):
    """
    set link
    """

  def set_caption(caption):
    """
    set caption
    """

  def set_notes(notes):
    """
    set notes
    """


class INoteInteractiveImage(IDocumentStructureNode):
  """
  Node for interactive image
  """

  path = ValidTextLine(title=u"path",
                       required=True,
                       default=u'')

  caption = ValidTextLine(title=u"Caption",
                          required=True,
                          default=u'')


class IFigure(IDocumentStructureNode):
  """
  Node for figure environment
  """

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  caption = Variant((Object(IDocumentStructureNode),
                     ValidTextLine()), title=u"Figure Caption",
                    required=False)

  image_id = ValidTextLine(title=u"Image id",
                           required=False)

  image_alt = Variant((Object(IDocumentStructureNode),
                       ValidTextLine()), title=u"Image Alt",
                      required=True,
                      default=u'')

  data_type = ValidTextLine(title=u"Data type",
                            required=False)

  title = Variant((Object(IDocumentStructureNode),
                   ValidTextLine()), title=u"Figure Title",
                  required=True,
                  default=u'')
  centered = Bool(title=u"Figured Centered",
                  default=True)
  floating = Bool(title=u"Floating Figure",
                  default=False)
  icon = Bool(title=u"Figure as an icon",
              default=False)
  presentation_pref = ValidTextLine(title=u"Figure Presentation Preference",
                                    required=False)

  def set_caption(caption):
    """
    set caption
    """

  def set_label(label):
    """
    set label
    """


class IGlossary(IDocumentStructureNode):
  """
  Node for glossary
  """
  title = ValidTextLine(title=u"Title",
                        required=False)

  filename = ValidTextLine(title=u"Filename",
                           required=False)

  glossary_dict = Dict(title=u"Glossarry dict",
                       required=False)

  def set_title(title):
    """
    set title
    """

  def set_filename(filename):
    """
    set filename
    """

  def set_glossary_dict(glossary_dict):
    """
    set glossary dictionary
    """


class IGlossaryList(IDocumentStructureNode):
  """
  Node for glossary list
  """


class IGlossaryItem(IDocumentStructureNode):
  """
  Node for glossary item
  """


class IGlossaryDT(IDocumentStructureNode):
  """
  Node for glossary row
  """

  desc = ValidTextLine(title=u"Description",
                       required=False)

  def set_description(desc):
    """
    set description
    """


class IGlossaryDD(IDocumentStructureNode):
  """
  Node for glossary description (stored in a cell)
  """


class IGlossaryTerm(IDocumentStructureNode):
  """
  Node for glossary term
  """


class IGlossaryEntry(IDocumentStructureNode):
  """
  Node for glossary entry (better one)
  """
  term = Variant((Object(IDocumentStructureNode),
                  ValidTextLine()),
                 title=u"Glossary Term",
                 required=True,
                 default=u'')

  definition = Variant((Object(IDocumentStructureNode),
                        ValidTextLine()),
                       title=u"Glossary Definition",
                       required=True,
                       default=u'')
  key_term = Variant((Object(IDocumentStructureNode),
                      ValidTextLine()),
                     title=u"Glossary key",
                     required=False,
                     default=u'')


class ISolution (IDocumentStructureNode):
  """
  Node for exercise's solution
  This is mostly used when parsing openstax epub to latex.
  """

  solution = ValidTextLine(title=u"Solution",
                           required=False)

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  problem_type = ValidTextLine(title=u"Problem Type",
                               required=False)

  def set_solution(solution):
    """
    set solution
    """

  def set_label(label):
    """
    set label
    """

  def set_problem_type(problem_type):
    """
    set problem type
    """


class IProblem(IDocumentStructureNode):
  """
  Node for exercise's solution
  This is mostly used when parsing openstax epub to latex.
  """

  question = Variant((Object(IDocumentStructureNode),
                      ListOrTuple()),
                     title=u"Question",
                     required=False)

  solution = Variant((Object(IDocumentStructureNode),
                      ListOrTuple(),
                      ValidTextLine()),
                     title=u"Solution",
                     required=False)

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  problem_type = ValidTextLine(title=u"Problem Type",
                               required=False)

  def set_question(question):
    """
    set question
    """

  def set_solution(solution):
    """
    set solution
    """

  def set_label(label):
    """
    set label
    """

  def set_problem_type(problem_type):
    """
    set problem type
    """


class IExercise(IDocumentStructureNode):
  """
  Node for exercise which consists of problem and solution.
  This is mostly used when parsing openstax epub to latex.
  """

  problem = Variant((Object(IDocumentStructureNode),
                     ListOrTuple(),
                     ValidTextLine()),
                    title=u"Problem",
                    required=False)

  solution = Variant((Object(IDocumentStructureNode),
                      ListOrTuple(),
                      ValidTextLine()),
                     title=u"Solution",
                     required=False)

  def set_problem(problem):
    """
    set problem
    """

  def set_solution(solution):
    """
    set solution
    """

  def set_label(label):
    """
    set label
    """


class IMultipleChoices(IDocumentStructureNode):
  """
  Node for multiple choices question
  This is mostly used when parsing openstax epub to latex.
  """

  solution = Object(IDocumentStructureNode,
                    required=False)

  choices = Object(IDocumentStructureNode,
                   required=False)

  def set_solution(solution):
    """
    set solution
    """

  def set_choices(choices):
    """
    set choices
    """


class IChapterExercise(IDocumentStructureNode):
  """
  Node for chapter exercise
  This is mostly used when parsing openstax epub to latex.
  """


class IExerciseSection(IDocumentStructureNode):
  """
  Node for exercise section
  This is mostly used when parsing openstax epub to latex.
  """


class IExerciseElement(IDocumentStructureNode):
  """
  Node for exercise element
  This is mostly used when parsing openstax epub to latex.
  """


class IExerciseDiv(IDocumentStructureNode):
  """
  Node for exercise div
  This is mostly used when parsing openstax epub to latex.
  """


class IExample(IDocumentStructureNode):
  """
  Node for exercise example
  This is mostly used when parsing openstax epub to latex.
  """


class IProblemExercise(IDocumentStructureNode):
  """
  Node for exercise problem
  This is mostly used when parsing openstax epub to latex.
  """
  problem_type = ValidTextLine(title=u"Problem type",
                               required=False)

  title = Variant((Object(IDocumentStructureNode,
                          title=u"Title"),
                   ValidTextLine(title=u"Title")),
                  required=False)

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)


class IExerciseCheck(IDocumentStructureNode):
  """
  Node for exercise check
  This is mostly used when parsing openstax epub to latex.
  """
  title = ValidTextLine(title=u"Title",
                        required=False)

  solution = Object(ISolution, title=u"Solution",
                    required=False)

  def set_title(title):
    """
    set title
    """

  def set_solution(solution):
    """
    set solution
    """


class IEndOfChapterSolution(IDocumentStructureNode):
  """
  Node for end of chapter solution
  This is mostly used when parsing openstax epub to latex.
  """

  title = ValidTextLine(title=u"Title",
                        required=False)

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  body = Object(IDocumentStructureNode,
                title=u"Chapter Solution Body",
                required=False)


class IOpenstaxNoteBody(IDocumentStructureNode):
  """
  Node for openstax note body
  """


class IOpenstaxNote(IDocumentStructureNode):
  """
  Node for openstax note
  This is mostly used when parsing openstax epub to latex.
  """
  title = Variant((Object(IDocumentStructureNode,
                          title=u"Title"),
                   ValidTextLine(title=u"Title")),
                  required=False)

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  body = Object(IDocumentStructureNode,
                title=u"Openstax Note Body",
                required=False)


class IOpenstaxExampleNote(IOpenstaxNote):
  """
  Node for openstax note
  """


class IEquationImage(IDocumentStructureNode):
  """
  Node for equation image
  """

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  text = Variant((Object(IDocumentStructureNode),
                  ValidTextLine()),
                 title=u"Label",
                 required=False)

  image = Object(IDocumentStructureNode,
                 title=u"Image",
                 required=False)


class IOpenstaxAttributions(IDocumentStructureNode):
  """
  Node for openstax attribution
  """


class IOpenstaxTitle(IDocumentStructureNode):
  """
  Node for openstax title
  """


class ICNXContent(IDocumentStructureNode):
  """
  Node for CNX Content
  """
  modules = ListOrTuple(title=u"Modules",
                        required=False)

  subcollections = ListOrTuple(title=u"Sub Collection",
                               required=False)


class ICNXCollection(IDocumentStructureNode):
  """
  Node for cnx collection
  """
  metadata = Dict(title=u"Metadata",
                  required=False)

  content = Object(ICNXContent, title=u"Content",
                   required=False)


class ICNXSubcollection(IDocumentStructureNode):
  """
  Node for cnx sub collection
  """
  title = ValidTextLine(title=u"Title",
                        required=False)

  content = Object(ICNXContent, title=u"Content",
                   required=False)


class ICNXModule(IDocumentStructureNode):
  """
  Node for cnx module
  """
  document = ValidTextLine(title=u"Document",
                           required=False)

  title = ValidTextLine(title=u"Title",
                        required=False)


class ICNXHTMLBody(IDocumentStructureNode):
  """
  Node for cnx html body
  """


class ICNXGlossary(IDocumentStructureNode):
  """
  Node for cnx glossary
  """


class ICNXProblemSolution(IDocumentStructureNode):
  """
  Node for cnx problem solution
  """

  title = Variant((Object(INode,
                          title=u"Title"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)


class IGlossaryDefinition(IDocumentStructureNode):
  """
  Node for glossary definition
  """
  term = Object(IDocumentStructureNode,
                title=u"Term",
                required=False)

  meaning = Object(IDocumentStructureNode,
                   title=u"Meaning",
                   required=False)


class IFootnoteText(IDocumentStructureNode):
  """
  Node for footnote text.
  """

  text = Variant((Object(IDocumentStructureNode,
                         title=u"Text"),
                  ValidTextLine(title=u"Text")),
                 required=False)

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)

  num = Variant((ValidTextLine(), Int()),
                title=u"Num",
                required=False)


class IFootnoteMark(IDocumentStructureNode):
  """
  Node for footnote text.
  """

  text = Variant((Object(IDocumentStructureNode,
                         title=u"Text"),
                  ValidTextLine(title=u"Text")),
                 required=False)

  num = Variant((ValidTextLine(), Int()),
                title=u"Num",
                required=False)


class IFootnote(IDocumentStructureNode):
  """
  Node for footnote
  """
  text = Variant((Object(IDocumentStructureNode,
                         title=u"Text"),
                  ValidTextLine(title=u"Text")),
                 required=False)

  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)


class IPreTag(IDocumentStructureNode):
  """
  Node for PreTag
  """


class IDocxTable(IDocumentStructureNode):
  """
  Node for Docx Table
  """
  borders = Dict(title=u"Table Border",
                 required=False)

  grid = Int(title=u"Table Grid",
             required=False)

  alignment = ValidTextLine(title=u"Alignment",
                            required=False)


class IDocxTRow(IDocumentStructureNode):
  """
  Node for Docx Table Row
  """


class IDocxTCell(IDocumentStructureNode):
  """
  Node for Docx Table Cell
  """
  grid_span = Int(title=u"Grid Span",
                  required=True,
                  default=0)


class INaqSymmath(IDocumentStructureNode):
  """
  Node for NaqSymmathPart
  """
  label = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)


class INaqSymmathPart(IDocumentStructureNode):
  """
  Node for NaqSymmathPart
  """
  text = Variant((Object(IDocumentStructureNode,
                         title=u"Text"),
                  ValidTextLine(title=u"Text")),
                 required=False)
  solution = Variant((Object(IDocumentStructureNode,
                             title=u"Label"),
                      ValidTextLine(title=u"Label")),
                     required=False)
  explanation = Variant((Object(IDocumentStructureNode,
                                title=u"Label"),
                         ValidTextLine(title=u"Label")),
                        required=False)


class INaqSymmathPartSolution(IDocumentStructureNode):
  """
  Node for NaqSymmathPartSolution
  """


class INaqSymmathPartSolutionValue(IDocumentStructureNode):
  """
  Node for NaqSymmathPartSolutionValue
  """
  option = Variant((Object(IDocumentStructureNode,
                           title=u"Text"),
                    ValidTextLine(title=u"Text")),
                   required=False)

  value = Variant((Object(IDocumentStructureNode,
                          title=u"Label"),
                   ValidTextLine(title=u"Label")),
                  required=False)


class INaqSymmathPartSolutionExplanation(IDocumentStructureNode):
  """
  Node for NaqSymmathPartSolutionExplanation
  """
