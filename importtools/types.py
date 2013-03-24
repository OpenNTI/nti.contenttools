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

class Newline(_Container):

    def __new__( cls ):
        return super(Newline,cls).__new__( cls, '\\newline\n' )

    def __init__( self ):
        super(Newline,self).__init__( self, '\\newline\n' )

class href(_Container):

    def __new__( cls, url, text=None ):
        if text:
            _t = url + '}{' + text
        else:
            _t = url
        return super(href,cls).__new__( cls, '\\href{' + _t + '}' )

    def __init__( self, url, text=None ):
        # Note: __new__ does all the actual work, because these are immutable as strings
        if text:
            _t = url + '}{' + text
        else:
            _t = url
        super(href,self).__init__( self, '\\href{' + _t + '}' )

class Image(_Container):

    def __new__( cls, image_file, parms=None ):
        if parms:
            _t = '[%s]{%s}' % (parms,image_file)
        else:
            _t = '{%s}' % image_file
        return super(Image,cls).__new__( cls, '\\includegraphics' + _t  )

    def __init__( self, image_file, parms=None ):
        # Note: __new__ does all the actual work, because these are immutable as strings
        if parms:
            _t = '[%s]{%s}' % (parms,image_file)
        else:
            _t = '{%s}' % image_file
        super(Image,self).__init__( self, '\\includegraphics' + _t  )

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

class _EnvironmentElement( _Node ):
    element = None

    def __init__( self, optional='' ):
        if optional:
            self.optional = '[' + optional + ']'
        else:
            self.optional = ''

    def __str__( self ):
        body = u''
        optional = u''
        if self.optional:
            optional = u'[' + self.optional + u']'
        if self.children:
            for child in self.children:
                body = body + unicode(child) + u'\n'
            return '\\begin{' + self.element + '}' + optional + '\n' + body + '\\end{' + self.element + '}'
        else:
            return ''

