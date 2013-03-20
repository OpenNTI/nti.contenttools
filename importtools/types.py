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

class TextNode(_Node, frg_interfaces.PlainTextContentFragment):
    __slots__ = frg_interfaces.PlainTextContentFragment.__slots__ + ('children','__parent__')

    def __new__( cls, text ='' ):
        return super(TextNode,cls).__new__( cls, PlainTextToLatexFragmentConverter(text) )

    def __init__( self, text='' ):
        # Note: __new__ does all the actual work, because these are immutable as strings
        super(TextNode,self).__init__( self, PlainTextToLatexFragmentConverter(text) )

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

class Footnote(_WrappedElement):
    wrapper = 'footnote'

class Chapter(_WrappedElement):
    wrapper = 'chapter'

class Section(_WrappedElement):
    wrapper = 'section'

class SubSection(_WrappedElement):
    wrapper = 'subsection'

class SubSubSection(_WrappedElement):
    wrapper = 'subsubsection'

class Paragraph(_WrappedElement):
    wrapper = 'paragraph'

class SubParagraph(_WrappedElement):
    wrapper = 'subparagraph'

class SubSubParagraph(_WrappedElement):
    wrapper = 'subsubparagraph'

class Label(_WrappedElement):
    wrapper = 'label'

class Title(_WrappedElement):
    wrapper = 'title'

class Author(_WrappedElement):
    wrapper = 'author'

class Modified(_WrappedElement):
    wrapper = 'modified'

class Strikeout(_WrappedElement):
    wrapper = 'sout'

class TextIT(_WrappedElement):
    wrapper = 'textit'

class TextBF(_WrappedElement):
    wrapper = 'textbf'

class Uline(_WrappedElement):
    wrapper = 'uline'

class NTIIncludeVideo(_WrappedElement):
    wrapper = 'ntiincludevideo'

class NTIImageHref(_WrappedElement):
    wrapper = 'ntiimagehref'

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

class Item( _SimpleElement ):
    element = 'item'

class NAQChoice( _SimpleElement ):
    element = 'naqchoice'

class NAQSolution( _SimpleElement ):
    element = 'naqsolution'

class NAQHint( _SimpleElement ):
    element = 'naqhint'

class _EnvironmentElement( _Node ):
    element = None

    def __init__( self, optional='' ):
        if optional:
            self.optional = '[' + optional + ']'
        else:
            self.optional = ''

    def __str__( self ):
        body = ''
        optional = ''
        if self.optional:
            optional = '[' + self.optional + ']'
        if self.children:
            for child in self.children:
                body = body + unicode(child) + '\n'
            return '\\begin{' + self.element + '}' + optional + '\n' + body + '\\end{' + self.element + '}'
        else:
            return ''

class Document( _EnvironmentElement ):
    element = 'document'

class NAQChoices( _EnvironmentElement ):
    element = 'naqchoices'

class NAQSolutions( _EnvironmentElement ):
    element = 'naqsolutions'

class NAQHints( _EnvironmentElement ):
    element = 'naqhints'

class NAQMultipleChoicePart( _EnvironmentElement ):
    element = 'naqmultiplechoicepart'

class NAQMultipleChoiceMultipleAnswerPart( _EnvironmentElement ):
    element = 'naqmultiplechoicemultipleanswerpart'

class NAQFreeResponsePart( _EnvironmentElement ):
    element = 'naqfreeresponsepart'

class NAQuestion( _EnvironmentElement ):
    element = 'naquestion'

class _List( _EnvironmentElement ):
    level = ''
    group = ''
    start = 0

class Enumerate( _List ):
    element = 'enumerate'
    format = 'decimal'

    def __str__( self ):
        if self.format == 'decimal':
            self.optional = '1'
        elif self.format == 'lowerLetter':
            self.optional = 'a'
        elif self.format == 'upperLetter':
            self.optional = 'A'
        elif self.format == 'lowerRoman':
            self.optional = 'i'
        elif self.format == 'upperRoman':
            self.optional = 'I'

        if self.start != 1:
            self.optional = self.optional + ', start=%s' % self.start

        return super( Enumerate, self ).__str__()

class Itemize( _List ):
    element = 'itemize'

