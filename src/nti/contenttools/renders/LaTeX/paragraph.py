from .base import base_renderer, _command_renderer

def _chapter( arg ):
    return _command_renderer( 'chapter', arg )

def _section( arg ):
    return _command_renderer( 'section', arg )

def _subsection( arg ):
    return _command_renderer( 'subsection', arg )

def _subsubsection( arg ):
    return _command_renderer( 'subsubsection', arg )

def _paragraph( arg ):
    return _command_renderer( 'paragraph', arg )

def _subparagraph( arg ):
    return _command_renderer( 'subparagraph', arg )

def _subsubparagraph( arg ):
    return _command_renderer( 'subsubparagraph', arg )

def paragraph_renderer(self):
    STYLES = { 'Heading1': _chapter,
               'Heading2': _section,
               'Heading3': _subsection,
               'Heading4': _subsubsection,
               'Heading5': _paragraph,
               'Heading6': _subparagraph,
               'Heading7': _subsubparagraph}

    result = base_renderer(self)

    for style in self.styles:
        if style in STYLES.keys():
            result = STYLES[style](result)
        else:
            print('Unhandled paragraph style: %s' % style)

    if result:
        result = result + u'\n\n'

    return result

def newline_renderer(self):
    return u'\\newline '

