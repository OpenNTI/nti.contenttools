#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contentfragments import interfaces as frg_interfaces
from nti.contentfragments.latex import PlainTextToLatexFragmentConverter

class _Node( object ):
    __parent__ = None
    children = ()
    
    def add_child( self, child ):
        if self.children == ():
            self.children = []
        if isinstance( child, _Node ):
            self.children.append( child )
            child.__parent__ = self

    def remove_child( self, child ):
        self.children.remove( child )
        child.__parent__ = None

    def render( self ):
        result = u''

        if not hasattr(self, 'children'):
            return self

        for child in self:
            result = result + child.render()

        return result

    def __iter__(self):
        current_item = 0
        while ( current_item < len(self.children) ):
            yield self.children[current_item]
            current_item += 1

class TextNode(_Node, frg_interfaces.PlainTextContentFragment):
    __slots__ = frg_interfaces.PlainTextContentFragment.__slots__ + ('children','__parent__')

    def __new__( cls, text ='' ):
        return super(TextNode,cls).__new__( cls, PlainTextToLatexFragmentConverter(text) )

    def __init__( self, text='' ):
        # Note: __new__ does all the actual work, because these are immutable as strings
        super(TextNode,self).__init__( self, PlainTextToLatexFragmentConverter(text) )

    def render( self ):
        return unicode( self )

class DocumentStructureNode( _Node ):
    STYLES = {}

    def __init__( self ):
        super( DocumentStructureNode, self ).__init__()
        self.styles = []

    def raw( self ):
        val = u''
        for child in self:
            if hasattr( child, 'raw' ):
                val = val + child.raw()
            else:
                val = val + child
        return val

    def addStyle( self, style ):
        self.styles.append(style)

    def removeStyle( self, style ):
        self.styles.remove(style)

class Document( DocumentStructureNode ):

    def __init__( self, doc_type=u'book' ):
        self.doc_type = doc_type
        self.title = u''
        self.author = u''
        self.packages = [ 'graphicx',
                          'hyperref',
                          'ulem',
                          'ntilatexmacros',
                          'ntiassessment']

class Body( DocumentStructureNode ):
    pass

class Chapter( DocumentStructureNode ):

    def __init__( self, suppressed=False ):
        super( Chapter, self ).__init__()
        self.suppressed = suppressed

class Section( DocumentStructureNode ):

    def __init__( self, suppressed=False ):
        super( Section, self ).__init__()
        self.suppressed = suppressed

class SubSection( DocumentStructureNode ):
    pass

class SubSubSection( DocumentStructureNode ):
    pass

class Paragraph( DocumentStructureNode ):
    pass

class Run( DocumentStructureNode ):
    pass

class Newline( DocumentStructureNode ):
    pass

class Note( DocumentStructureNode ):
    pass

class Hyperlink( DocumentStructureNode ):

    def __init__(self, target='', type_='Normal'):
        super( Hyperlink, self ).__init__()
        self.target = target
        self.type = type_

class Label( DocumentStructureNode ):

    def __init__(self, name=''):
        super( Label, self ).__init__()
        self.name = name

class Sidebar( DocumentStructureNode ):

    def __init__(self, title=''):
        super( Sidebar, self ).__init__()
        self.title = title

class BlockQuote( DocumentStructureNode ):

    def __init__(self, source=''):
        super( BlockQuote, self ).__init__()
        self.source = source

class Image( DocumentStructureNode ):

    def __init__(self, path=''):
        super( Image, self ).__init__()
        self.path = u''
        self.caption = u''
        self.width = 0
        self.height = 0

class Video( DocumentStructureNode ):

    def __init__(self, path=''):
        super( Video, self ).__init__()
        self.path = u''
        self.thumbnail = u''
        self.caption = u''
        self.width = 0
        self.height = 0

class List( DocumentStructureNode ):

    def __init__(self, level='', group='', start=0, fmt=''):
        self.level = level
        self.group = group
        self.start = start
        self.format = fmt

class UnorderedList( List ):
    pass

class OrderedList( List ):

    """
    def __init__(self):
        super(OrderedList, self).__init__(format='decimal')
    """
    pass

class Item( DocumentStructureNode ):
    pass

class Table(DocumentStructureNode):
    def __init__(self, number_of_col=0):
        self.number_of_col = number_of_col

    def set_number_of_col(self, number_of_col):
        self.number_of_col = number_of_col

class Row(DocumentStructureNode):
    def __init__(self, number_of_col=0):
        self.number_of_col = number_of_col
        
    def set_number_of_col(self, number_of_col):
        self.number_of_col = number_of_col

class Cell (DocumentStructureNode):
    pass

class TBody(DocumentStructureNode):
    def __init__(self, number_of_col=0):
        self.number_of_col = number_of_col
        
    def set_number_of_col(self, number_of_col):
        self.number_of_col = number_of_col

class Math(DocumentStructureNode):
    pass

class MRow(DocumentStructureNode):
    pass

class MSup(DocumentStructureNode):
    pass

class MSub(DocumentStructureNode):
    pass

class MSubSup(DocumentStructureNode):
    pass

class MathRun(DocumentStructureNode):
    pass

class MFenced(DocumentStructureNode):
    def __init__(self, opener=u'', close=u'', separators = u''):
        self.opener = opener
        self.close = close
        self.separators = separators

class MSpace(DocumentStructureNode):
    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height

class Mtable(DocumentStructureNode):
    def __init__(self, number_of_col=0):
        self.number_of_col = number_of_col
        
    def set_number_of_col(self, number_of_col):
        self.number_of_col = number_of_col


class Mtr(DocumentStructureNode):
    def __init__(self, number_of_col=0):
        self.number_of_col = number_of_col
        
    def set_number_of_col(self, number_of_col):
        self.number_of_col = number_of_col

class Mtd (DocumentStructureNode):
    pass

class Mfrac(DocumentStructureNode):
    pass

class Msqrt(DocumentStructureNode):
    pass

class Mroot(DocumentStructureNode):
    pass

