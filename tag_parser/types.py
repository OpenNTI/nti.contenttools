# Import NTI things
from nti.contentfragments import interfaces as frg_interfaces
from nti.contentfragments.latex import PlainTextToLatexFragmentConverter


class _Node( object ):

    parent = None
    children = ()
    
    def add_child( self, child ):
        if self.children == ():
            self.children = []
        self.children.append( child )
        child.parent = self

class _Container(_Node, frg_interfaces.LatexContentFragment):
    pass

class _WrappedElement(_Container):
    wrapper = None

    def __new__( cls, text ):
        return super(_WrappedElement,cls).__new__( cls, '\\' + cls.wrapper + '{' + text + '}' )

    def __init__( self, text=None ):
        # Note: __new__ does all the actual work, because these are immutable as strings
        super(_WrappedElement,self).__init__( self, '\\' + self.wrapper + '{' + text + '}' )

class TextNode(_Node, frg_interfaces.LatexContentFragment):

    def __new__( cls, text ='' ):
        return super(TextNode,cls).__new__( cls, PlainTextToLatexFragmentConverter(text) )

    def __init__( self, text='' ):
        # Note: __new__ does all the actual work, because these are immutable as strings
        super(TextNode,self).__init__( self, PlainTextToLatexFragmentConverter(text) )

class _SimpleElement( _Container ):
    element = None

    def __new__( cls, text=None, optional='' ):
        if optional:
            spacer = '[' + optional + '] '
        else:
            spacer = ' '
        return super(_SimpleElement,cls).__new__( cls, '\\' + cls.element + spacer + text )

    def __init__( self, text=None, optional='' ):
        # Note: __new__ does all the actual work, because these are immutable as strings
        if optional:
            spacer = '[' + optional + '] '
        else:
            spacer = ' '
        super(_SimpleElement,self).__init__( self, '\\' + self.element + spacer + text )

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
        if self.children:
            for child in self.children:
                body = body + str(child) + '\n'
            return '\\begin{' + self.element + '}' + self.optional + '\n' + body + '\\end{' + self.element + '}'
        else:
            return ''

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

