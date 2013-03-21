from ...docx.paragraph import Item, List, Paragraph, Run, OrderedList, UnorderedList, Note, Newline, Hyperlink, Image
from ... import types


def baseRenderer(self):
    result = u''

    for child in self.children:
        result = result + child.render()

    return result

def paragraphRenderer(self):
    STYLES = { 'Heading1': types.Chapter,
               'Heading2': types.Section,
               'Heading3': types.SubSection,
               'Heading4': types.SubSubSection,
               'Heading5': types.Paragraph,
               'Heading6': types.SubParagraph,
               'Heading7': types.SubSubParagraph}

    result = baseRenderer(self) + u'\n'

    for style in self.styles:
        if style in STYLES.keys():
            result = STYLES[style](result)
        else:
            print('Unhandled paragraph style: %s' % style)

    return result

def runRenderer(self):
    STYLES = { 'bold': types.TextBF,
               'inserted': types.Modified,
               'italic': types.TextIT,
               'strike': types.Strikeout,
               'underline': types.Uline}

    result = baseRenderer(self)

    for style in self.styles:
        if style in STYLES.keys():
            result = STYLES[style](result)
        else:
            print('Unhandled run style: %s' % style)

    return result


def environmentRenderer( self, element, optional ):
    body = baseRenderer(self)
    return u'\\begin{%s}%s\n%s\\end{%s}\n' % ( element, optional, body, element)

def orderedListRenderer(self):
    optional = u''
    if self.format == 'decimal':
        optional = u'1'
    elif self.format == 'lowerLetter':
        optional = u'a'
    elif self.format == 'upperLetter':
        optional = u'A'
    elif self.format == 'lowerRoman':
        optional = u'i'
    elif self.format == 'upperRoman':
        optional = u'I'

    if self.start != 1:
        optional = optional + u', start=%s' % self.start

    if optional:
        optional = u'[' + optional + u']'

    return environmentRenderer(self, u'enumerate', optional)

def listRenderer(self):
    return environmentRenderer(self, u'itemize', u'')

def itemRenderer(self):
    return u'\\item %s' % baseRenderer(self)

def noteRenderer(self):
    return u'\\footnote{%s}' % baseRenderer(self)

def newlineRenderer(self):
    return u'\\newline'

def hyperlinkRenderer(self):
    result = u''
    if self.type == 'Normal':
        result = u'\\href{%s}{%s}' % (self.target, baseRenderer(self))
    elif self.type == 'YouTube':
        result = u'\\href{%s}{%s}' % (self.target, baseRenderer(self))
    elif self.type == 'Thumbnail':
        result = u'\\href{%s}{%s}' % (self.target, baseRenderer(self))
    return result

Paragraph.render = paragraphRenderer
Run.render = runRenderer
OrderedList.render = orderedListRenderer
UnorderedList.render = listRenderer
List.render = listRenderer
Item.render = itemRenderer
Note.render = noteRenderer
Newline.render = newlineRenderer
Hyperlink.render = hyperlinkRenderer
