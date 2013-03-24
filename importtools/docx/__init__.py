from . import properties as docx

from ..types import _Node
from ..types import *

# These classes encapsulate WordprocessingML structures
class _DocxStructureElement( _Node ):
    STYLES = {}

    def __init__( self ):
        super( _DocxStructureElement, self ).__init__()
        self.styles = []

    def __str__( self ):
        val = u''
        for child in self.children:
            if isinstance( child, _DocxStructureElement ):
                val = val + child.__str__()
            else:
                val = val + child


        for style in self.styles:
            if val:
                if style in self.__class__.STYLES:
                    val = self.__class__.STYLES[style](val)
                else:
                    print('Unhandled style: %s' % style)

        return val

    def raw( self ):
        val = u''
        for child in self.children:
            if isinstance( child, _DocxStructureElement ):
                val = val + child.raw()
            else:
                val = val + child
        return val

    def addStyle( self, style ):
        self.styles.append(style)

    def removeStyle( self, style ):
        self.styles.remove(style)


def process_border( border ):

    def process_attributes( attributes ):
        attribs = {}
        if '{'+docx.nsprefixes['w']+'}color' in attributes.keys():
            attribs['color'] = attributes['{'+docx.nsprefixes['w']+'}color'] or None
        if '{'+docx.nsprefixes['w']+'}frame' in attributes.keys():
            attribs['frame'] = attributes['{'+docx.nsprefixes['w']+'}frame']
        if '{'+docx.nsprefixes['w']+'}shadow' in attributes.keys():
            attribs['shadow'] = attributes['{'+docx.nsprefixes['w']+'}shadow'] or None
        if '{'+docx.nsprefixes['w']+'}space' in attributes.keys():
            attribs['space'] = attributes['{'+docx.nsprefixes['w']+'}space'] or None
        if '{'+docx.nsprefixes['w']+'}sz' in attributes.keys():
            attribs['sz'] = attributes['{'+docx.nsprefixes['w']+'}sz'] or None
        if '{'+docx.nsprefixes['w']+'}themeColor' in attributes.keys():
            attribs['themeColor'] = attributes['{'+docx.nsprefixes['w']+'}themeColor'] or None
        if '{'+docx.nsprefixes['w']+'}themeShade' in attributes.keys():
            attribs['themeShade'] = attributes['{'+docx.nsprefixes['w']+'}themeShade'] or None
        if '{'+docx.nsprefixes['w']+'}themeTint' in attributes.keys():
            attribs['themeTint'] = attributes['{'+docx.nsprefixes['w']+'}themeTint'] or None
        if '{'+docx.nsprefixes['w']+'}val' in attributes.keys():
            attribs['val'] = attributes['{'+docx.nsprefixes['w']+'}val'] or None
        return attribs

    borders = {}
    for element in border.iterchildren():
        if element.tag == '{'+docx.nsprefixes['w']+'}bottom':
            borders['bottom'] = process_attributes( element.attrib )
        elif element.tag == '{'+docx.nsprefixes['w']+'}end':
            borders['end'] = process_attributes( element.attrib )
        elif element.tag == '{'+docx.nsprefixes['w']+'}insideH':
            borders['insideH'] = process_attributes( element.attrib )
        elif element.tag == '{'+docx.nsprefixes['w']+'}insideV':
            borders['insideV'] = process_attributes( element.attrib )
        elif element.tag == '{'+docx.nsprefixes['w']+'}start':
            borders['start'] = process_attributes( element.attrib )
        elif element.tag == '{'+docx.nsprefixes['w']+'}top':
            borders['top'] = process_attributes( element.attrib )
        elif element.tag == '{'+docx.nsprefixes['w']+'}left':
            borders['left'] = process_attributes( element.attrib )
        elif element.tag == '{'+docx.nsprefixes['w']+'}right':
            borders['right'] = process_attributes( element.attrib )
        else:
            print(element.tag)

    return borders
