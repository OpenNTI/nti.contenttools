from . import properties as docx

from ..import types
from .body import Body

class Document( types.Document ):

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
