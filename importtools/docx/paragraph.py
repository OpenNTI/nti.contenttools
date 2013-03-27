import os
import urllib
import urlparse

from . import _DocxStructureElement
from . import process_border
from . import properties as docx
from ..types import _Node
from ..types import TextNode

IGNORED_TAGS = [ '{'+docx.nsprefixes['w']+'}ind',
		 '{'+docx.nsprefixes['w']+'}sectPr',
		 '{'+docx.nsprefixes['w']+'}proofErr',
		 '{'+docx.nsprefixes['w']+'}noProof',
		 '{'+docx.nsprefixes['w']+'}commentReference',
		 '{'+docx.nsprefixes['w']+'}commentRangeEnd',
		 '{'+docx.nsprefixes['w']+'}commentRangeStart',
		 '{'+docx.nsprefixes['w']+'}bookmarkEnd',
		 '{'+docx.nsprefixes['w']+'}bookmarkStart',
		 '{'+docx.nsprefixes['w']+'}shd',
		 '{'+docx.nsprefixes['w']+'}contextualSpacing',
		 '{'+docx.nsprefixes['w']+'}tabs',
		 '{'+docx.nsprefixes['w']+'}highlight',
		 '{'+docx.nsprefixes['w']+'}jc',
		 '{'+docx.nsprefixes['w']+'}keepNext',
		 '{'+docx.nsprefixes['w']+'}outlineLvl',
		 '{'+docx.nsprefixes['w']+'}lastRenderedPageBreak']

class Paragraph( _DocxStructureElement ):

    @classmethod
    def process(cls, paragraph, doc, rels=None ):
	'''Processes the text of a given paragraph into insets and text.'''
	
	if rels is None:
            rels = doc.relationships

	me = cls()
        me.numbering = None
	fields = []
	# Scan the elements in the paragraph and extract information
	for element in paragraph.iterchildren():

            # Process Text Runs
            if element.tag == '{'+docx.nsprefixes['w']+'}r':
                me.add_child(Run.process(element, doc, fields = fields, rels = rels))
                pass
            # Process 'Deleted' Text Runs
            elif element.tag == '{'+docx.nsprefixes['w']+'}del':
                me.add_child(Del.process(element, doc, fields = fields, rels = rels))
            # Process 'Inserted' Text Runs
            elif element.tag == '{'+docx.nsprefixes['w']+'}ins':
                me.add_child(Ins.process(element, doc, fields = fields, rels = rels))
            # Look for hyperlinks
            elif (element.tag == '{'+docx.nsprefixes['w']+'}hyperlink'):
                me.add_child(Hyperlink.process(element, doc, rels = rels))
            # Paragraph Properties
            elif element.tag == '{'+docx.nsprefixes['w']+'}pPr':
                me.process_properties( element, doc, rels=rels )
            # Skip elements in IGNORED_TAGS
            elif element.tag in IGNORED_TAGS:
                pass

            # We did not handle the element
            else:
                print('Did not handle paragraph element: %s' % element.tag)

	# Check to see if we found the document title
	if 'Title' in me.styles:
            me.removeStyle('Title')
            doc.title = str(me).strip()
            me = None
	else:
            # Check for NTI Tags
            s,v = doc.tagparser.parse_line( me.raw() )
            if s != 'IDLE':
                me = None
            if v:
                me = v

	if me is not None and hasattr(me, 'numbering') and me.numbering is not None:
            item = Item()
            item.add_child(me)
            me.numbering.add_child( item )
            me = me.numbering

	return me

    def process_properties( self, properties, doc, rels=None ):
        for element in properties.iterchildren():
            # Look for Paragraph Styles
            if element.tag == '{'+docx.nsprefixes['w']+'}pStyle':
                self.addStyle(element.attrib['{'+docx.nsprefixes['w']+'}val'])
            # We don't care about the paragraph mark character in LaTeX so ignore formattingi it.
            elif element.tag == '{'+docx.nsprefixes['w']+'}rPr':
                pass
            # Look for numbering levels
            elif (element.tag == '{'+docx.nsprefixes['w']+'}numPr'):
                print('processing numbering')
                self.numbering = process_numbering( element, doc )
            # Skip elements in IGNORED_TAGS
            elif element.tag in IGNORED_TAGS:
                pass
            else:
                print('Unhandled paragraph property: %s' % element.tag)


class Run( _DocxStructureElement ):

    @classmethod
    def process( cls, textrun, doc, fields = [], rels=None ):
	'''Process a paragraph textrun, parse for character styles'''

	if rels is None:
            rels = doc.relationships

	me = cls()
	for element in textrun.iterchildren():

            # Look for run properties
            if element.tag == '{'+docx.nsprefixes['w']+'}rPr':
                me.process_properties( element, doc, rels=rels )
            # Find run text
            elif (element.tag == '{'+docx.nsprefixes['w']+'}t'): 
                # If not character style, append to the end of the paragraph
                if element.text:
                    me.add_child( TextNode(element.text) )
            elif element.tag == '{'+docx.nsprefixes['w']+'}drawing':
                me.add_child( Image.process(element, doc, rels=rels ) )
                pass
            # Find 'deleted' text
            elif element.tag == '{'+docx.nsprefixes['w']+'}delText':
                me.addStyle('strike')
                if element.text:
                    me.add_child( TextNode(element.text) )
            # Look for hyperlinks
            elif (element.tag == '{'+docx.nsprefixes['w']+'}hyperlink'):
                 me.add_child( Hyperlink.process(element, doc, rels = rels) )
            # Look for complex fields
            elif (element.tag == '{'+docx.nsprefixes['w']+'}fldChar'):
                type = element.attrib['{'+docx.nsprefixes['w']+'}fldCharType']
                if 'begin' in type:
                    # Push the element onto the field stack
                    fields.append(element)
                elif 'end' in type:
                    elems = []
                    # Pop the element off of the field stack
                    while fields:
                        if not isinstance( fields[len(fields)-1], Run ) \
                                and  '{'+docx.nsprefixes['w']+'}fldChar' in fields[len(fields)-1].tag:
                            if 'begin' in fields[len(fields)-1].attrib['{'+docx.nsprefixes['w']+'}fldCharType']:
                                # We have found the begining of the field so pop it off and
                                # stop searching
                                fields.pop()
                                break;
                            else:
                                fields.pop()
                        else:
                            elems.append(fields.pop())
                            me.add_child( processComplexField( elems, doc, rels = rels ) )
                elif 'separate' in type:
                    # This node was used to separate the field "command" from the result. It does not seem
                    # to make sense with how we are processing the document so it is being ignored.
                    pass

            # Look for field codes
            elif (element.tag == '{'+docx.nsprefixes['w']+'}instrText'):
                fields.append(element)

            # Look for footnotes
            elif (element.tag == '{'+docx.nsprefixes['w']+'}footnoteReference'):
                me.add_child( Note.process(element, doc) )
                pass
            # Look for endnotes
            elif (element.tag == '{'+docx.nsprefixes['w']+'}endnoteReference'):
                me.add_child( Note.process(element, doc) )
                pass
            # Look for carrage returns
            elif (element.tag == '{'+docx.nsprefixes['w']+'}br'):
                me.add_child( Newline() )
            # Look for other runs embedded in this run, process recursively
            elif (element.tag == '{'+docx.nsprefixes['w']+'}r'):
                me.add_child( cls.process(element, doc, fields = fields, rels = rels) )

            # Skip elements in IGNORED_TAGS
            elif element.tag in IGNORED_TAGS:
                pass

            # We did not handle the element
            else:
                print('Did not handle run element: %s' % element.tag)

	# Remove styles handled in other manners:
        if 'Hyperlink' in me.styles:
            me.removeStyle('Hyperlink')
        elif 'FootnoteReference' in me.styles:
            me.removeStyle('FootnoteReference')
        elif 'FootnoteText' in me.styles:
            me.removeStyle('FootnoteText')

	if fields:
            fields.append( me )
            return cls()
	else:
            return me


    def process_properties( self, properties, doc, rels=None ):
        for element in properties.iterchildren():
            if element.tag == '{'+docx.nsprefixes['w']+'}rStyle':
                self.addStyle(element.attrib['{'+docx.nsprefixes['w']+'}val'])
            elif element.tag == '{'+docx.nsprefixes['w']+'}b':
                self.addStyle('bold')
            # Ignore bold complex script specification
            elif element.tag == '{'+docx.nsprefixes['w']+'}bCs':
                pass
            # Ignore run content color specification
            elif element.tag == '{'+docx.nsprefixes['w']+'}color':
                pass
            elif element.tag == '{'+docx.nsprefixes['w']+'}i':
                self.addStyle('italic')
            # Ignore italic  complex script specification
            elif element.tag == '{'+docx.nsprefixes['w']+'}iCs':
                pass
            elif element.tag == '{'+docx.nsprefixes['w']+'}strike':
                self.addStyle('strike')
            elif element.tag == '{'+docx.nsprefixes['w']+'}u':
                self.addStyle('underline')
            # Ignore run level font specifications
            elif element.tag == '{'+docx.nsprefixes['w']+'}rFonts':
                pass
            # Ignore run level font size specifications
            elif element.tag == '{'+docx.nsprefixes['w']+'}sz':
                pass
            # Ignore run level complex script font size specifications
            elif element.tag == '{'+docx.nsprefixes['w']+'}szCs':
                pass
            # Skip elements in IGNORED_TAGS
            elif element.tag in IGNORED_TAGS:
                pass
            else:
                print('Unhandled run property: %s' % element.tag)


class Del( Run ):
    pass


class Ins( Run ):

    @classmethod
    def process( cls, element, doc, fields=None, rels=None ):
	me = super( Ins, cls ).process( element, doc, fields, rels )
        me.addStyle('inserted')
	return me


class Newline( _DocxStructureElement ):
    pass


class List( _DocxStructureElement ):
    level = ''
    group = ''
    start = 0


class UnorderedList( List ):
    pass


class OrderedList( List ):
    format = 'decimal'

class Item( _DocxStructureElement ):
    pass

def process_numbering( element, doc ):
	numId = ''
	ilvl = 0
	for sub_element in element.iterchildren():
		if (sub_element.tag == '{'+docx.nsprefixes['w']+'}numId'):
			numId = sub_element.attrib['{'+docx.nsprefixes['w']+'}val']
		elif (sub_element.tag == '{'+docx.nsprefixes['w']+'}ilvl'):
			ilvl = int(sub_element.attrib['{'+docx.nsprefixes['w']+'}val'])

	if numId in doc.numbering_collection:
		if ilvl < len(doc.numbering_collection[numId]):
			doc.numbering_collection[numId][ilvl].append( _Node() )
			if ilvl > 0:
				doc.numbering_collection[numId][ilvl-1][-1].add_child(doc.numbering_collection[numId][ilvl][-1])
		else:
			doc.numbering_collection[numId].append([])
			doc.numbering_collection[numId][ilvl].append( _Node() )
			if ilvl > 0:
				doc.numbering_collection[numId][ilvl-1][-1].add_child(doc.numbering_collection[numId][ilvl][-1])
	else:
		doc.numbering_collection[numId] = []
		doc.numbering_collection[numId].append( [] )
		doc.numbering_collection[numId][ilvl].append( _Node() )

	fmt_list = [ 'decimal', 'lowerLetter', 'upperLetter', 'lowerRoman', 'upperRoman' ]
	if numId in doc.numbering:
		numbering = doc.numbering[numId]
		if numbering.levels[str(ilvl)].format in fmt_list:
			el = OrderedList()
			el.format = numbering.levels[str(ilvl)].format
		else:
			el = UnorderedList()
	else:
		el = UnorderedList()

	if ilvl > 0:
		el.start = len(doc.numbering_collection[numId][ilvl][-1].__parent__.children)
	else:
		el.start = len(doc.numbering_collection[numId][ilvl])
	el.group = numId
	el.level = str(ilvl)

	return el


class Note( _DocxStructureElement ):
    notes = None
    rels = None
    type = ''

    @classmethod
    def process(cls, note, doc):
        rels = None
        
        # Retrieve the endnote Id Number
        id = note.attrib['{'+docx.nsprefixes['w']+'}id']

        me = cls()
        if (note.tag == '{'+docx.nsprefixes['w']+'}footnoteReference'):
            me.notes = doc.footnotes
            me.rels = doc.footnote_relationships
            me.type = 'footnote'
        elif (note.tag == '{'+docx.nsprefixes['w']+'}endnoteReference'):
            me.notes = doc.endnotes
            me.rels = doc.endnote_relationships
            me.type = 'endnote'
        
        # Retrieve the endnote text
        for note in me.notes.iterchildren():
            if note.attrib['{'+docx.nsprefixes['w']+'}id'] == id:
                for element in note.iterchildren():
                    # Process paragraphs found in the note
                    if element.tag == '{'+docx.nsprefixes['w']+'}p':
                        me.add_child(Paragraph.process(element, doc, rels = me.rels))

        return me


class Hyperlink( _DocxStructureElement ):
    target = ''
    type = ''

    @classmethod
    def process(cls, node, doc, rels=None ):
        '''Process a hyperlink element'''

        if rels is None:
            rels = doc.relationships

        me = cls()
        rId = node.attrib['{'+docx.nsprefixes['r']+'}id']
        rel_type, me.target = relationshipProperties(rId, doc, rels)
        for element in node.iterchildren():
            # Look for footnotes
            if (element.tag == '{'+docx.nsprefixes['w']+'}footnoteReference'):
                me.add_child(Note.process(element, doc))
            # Look for endnotes
            elif (element.tag == '{'+docx.nsprefixes['w']+'}endnoteReference'):
                me.add_child(Note.process(element, doc))
            # Look for embedded runs
            if (element.tag == '{'+docx.nsprefixes['w']+'}r'):
                me.add_child(Run.process(element, doc, rels = rels))

        return me

    def process_target(self):
        text = self.raw()

        if 'YouTube Video' in text:
            scheme = ''
            netloc = 'www.youtube.com'
            path = '/embed'
            query = { 'html5': '1', 'rel': '0' }
            parsed_url = urlparse.urlsplit( self.target )

            if len(parsed_url.path.split('/')) > 2:
                # Then assume that we were passed a more complete URL
                path = parsed_url.path
            else:
                # Assume we were given a 'shortened' URL.
                path = path + parsed_url.path

            # Add any query args to ours
            query.update( urlparse.parse_qsl(parsed_url.query) )
            self.target = urlparse.urlunsplit( (scheme, netloc, path, urllib.urlencode(query), '') )
            self.type = 'YouTube'
        elif 'Thumbnail' in text:
            self.type = 'Thumbnail'
        else:
            self.type = 'Normal'


class Image( _DocxStructureElement ):
    target = ''
    type = ''
    height = 0
    width = 0

    @classmethod
    def process( cls, image, doc, rels=None ):
        me = cls()
	# Iterate through the image properties and process
	for element in image.iter():
		# Search for Image Properties, contained in blipFill
		if element.tag == '{'+docx.nsprefixes['pic']+'}blipFill':
                    me.process_properties( element, doc, rels )
		elif element.tag == '{'+docx.nsprefixes['wp']+'}inline':
                    me.process_properties( element, doc, rels )
			
        return me

    def process_properties( self, properties, doc, rels=None ):
        # Retrieve the Image rId and filename
        for element in properties.iter():
            if element.tag == '{'+docx.nsprefixes['a']+'}blip':
                id = element.attrib['{'+docx.nsprefixes['r']+'}embed']
                self.type, self.target = relationshipProperties(id, doc, rels)
                doc.image_list.append(os.path.basename(self.target))
            elif element.tag == '{'+docx.nsprefixes['a']+'}ext':
                # Convert EMU to inches. 1 inch = 914400 EMU
                if 'cy' in element.attrib:
                    self.height = (float(element.attrib['cy']) / 914400)
                if 'cx' in element.attrib:
                    self.width = (float(element.attrib['cx']) / 914400)

        # Set the image path
        self.path = os.path.join( doc.image_dir , os.path.splitext( os.path.basename(self.target) )[0] )


def processField( field, doc, result, rels=None ):
    if rels is None:
        rels = doc.relationships

    _t = None
    field_code = field.split()
    if field_code and field_code[0] == 'HYPERLINK':
        _t = Hyperlink()
        _t.add_child(result)
        _t.target = field_code[len(field_code)-1].replace('"','')
        _t.process_target()
    else:
        _t = Run()
        print( 'Unhandled field: %s. Field body: %s' % ( field, str(result) ) )
    return _t

def processComplexField( elements, doc, rels=None ):
    if rels is None:
        rels = doc.relationships

    field = ''
    result = Run()
    for element in elements:
        if isinstance( element, Run ):
            result.add_child( element )
        elif element.tag == '{'+docx.nsprefixes['w']+'}instrText':
            field = field + TextNode( element.text )
    return processField( field, doc, result )

def relationshipProperties( rId, doc, rels=None ):
    '''Parse the document relationships to retrieve the type and target for a 
    specified document element.'''

    if rels is None:
        rels = doc.relationships

    # Search through rels to retrieve relationship properties
    for relationship in rels.iter():
        try:
            if relationship.attrib['Id'] == rId:
                return relationship.attrib['Type'], relationship.attrib['Target']
        except:
            pass

