from . import _DocxStructureElement
from . import properties as docx
from .body import Body

class Document( _DocxStructureElement ):

    def __init__( self, doc_type=u'book' ):
        self.doc_type = doc_type
        self.title = u''
        self.author = u''
        self.packages = [ 'graphicx',
                          'hyperref',
                          'ulem',
                          'ntilatexmacros',
                          'ntiassessment']

    @classmethod
    def process(cls, document, docxfile):
        me = cls()

        # Iterate over the structure of the document, process document body
        for element in document.iterchildren():
            # Process Elements in Document Body
            if element.tag == '{'+docx.nsprefixes['w']+'}body':
                me.add_child( Body.process( element, docxfile ) )
            else:
                print('Did not handle document element: %s' % element.tag)

        return me
