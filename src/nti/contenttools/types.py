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

        for child in self.children:
            result = result + child.render()

        return result

class TextNode(_Node, frg_interfaces.PlainTextContentFragment):
    __slots__ = frg_interfaces.PlainTextContentFragment.__slots__ + ('children','__parent__')

    def __new__( cls, text ='' ):
        return super(TextNode,cls).__new__( cls, PlainTextToLatexFragmentConverter(text) )

    def __init__( self, text='' ):
        # Note: __new__ does all the actual work, because these are immutable as strings
        super(TextNode,self).__init__( self, PlainTextToLatexFragmentConverter(text) )

    def render( self ):
        return unicode( self )
