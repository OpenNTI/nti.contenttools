# Import NTI things
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
        curent_item = 0
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

    def __init__(self, target='', type='Normal'):
        super( Hyperlink, self ).__init__()
        self.target = target
        self.type = type

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

    def __init__(self, level='', group='', start=0, format=''):
        self.level = level
        self.group = group
        self.start = start
        self.format = format

class UnorderedList( List ):
    pass

class OrderedList( List ):

    def __init__(self):
        super(OrderedList, self).__init__(format='decimal')

class Item( DocumentStructureNode ):
    pass

