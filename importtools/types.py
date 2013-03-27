from lxml import etree

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

class _Container(_Node, frg_interfaces.LatexContentFragment):
    __slots__ = frg_interfaces.LatexContentFragment.__slots__ + ('children','__parent__')

class _WrappedElement(_Container):
    wrapper = None

    def __new__( cls, text, optional=''  ):
        options = ''
        if optional:
            options = '[' + optional + '] '

        return super(_WrappedElement,cls).__new__( cls, '\\' + cls.wrapper + '{' + unicode(text) + '}' + options )

    def __init__( self, text='', optional=''  ):
        # Note: __new__ does all the actual work, because these are immutable as strings
        options = ''
        if optional:
            options = '[' + optional + '] '
        super(_WrappedElement,self).__init__( self, '\\' + self.wrapper + '{' + text + '}' + options )

class DocumentClass(_WrappedElement):
    wrapper = 'documentclass'

class UsePackage(_WrappedElement):
    wrapper = 'usepackage'

class Title(_WrappedElement):
    wrapper = 'title'

class _SimpleElement( _Container ):
    element = None

    def __new__( cls, text='', optional='' ):
        if optional:
            spacer = '[' + optional + '] '
        else:
            spacer = ' '
        return super(_SimpleElement,cls).__new__( cls, '\\' + cls.element + spacer + unicode(text) )

    def __init__( self, text='', optional='' ):
        # Note: __new__ does all the actual work, because these are immutable as strings
        if optional:
            spacer = '[' + optional + '] '
        else:
            spacer = ' '
        super(_SimpleElement,self).__init__( self, '\\' + self.element + spacer + unicode(text) )

class Quad( _SimpleElement ):
    element = 'quad'

class QQuad( _SimpleElement ):
    element = 'qquad'

