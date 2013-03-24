from . import _DocxStructureElement
from . import properties as docx
from .paragraph import Paragraph
from .paragraph import List
from .table import Table
#from ..types import _Node
#from ..types import TextNode



class Body( _DocxStructureElement ):

    @classmethod
    def process(cls, body, doc, rels=None ):
	"""Process the content of a WordprocessingML body tag."""

	if rels is None:
            rels = doc.relationships

	me = cls()
	for element in body.iterchildren():

            # P (paragraph) Elements
            if element.tag == '{'+docx.nsprefixes['w']+'}p':
                me.add_child( Paragraph.process(element, doc, rels = rels) )

            # T (table) Elements
            elif element.tag == '{'+docx.nsprefixes['w']+'}tbl':
                me.add_child( Table.process(element, doc, rels = rels) )

            else:
                print('Did not handle body element: %s' % element.tag)

	me.children = _consolidate_lists( me.children )

	return me

def _consolidate_lists( list = [] ):
    new_list = []
    for i in range(len(list)):
        if isinstance(list[i], List) and (i + 1 < len(list)) and isinstance(list[i+1], List) and list[i].group == list[i+1].group:
            if list[i].level == list[i+1].level:
                for child in list[i+1].children:
                    list[i].add_child( child )
                    list[i+1] = list[i]
            elif list[i].level < list[i+1].level:
                list[i].add_child( list[i+1] )
                list[i+1] = list[i]
            else:
                list[i].children = _consolidate_lists( list[i].children )
                new_list.append( list[i] )
        else:
            if isinstance(list[i], List):
                list[i].children = _consolidate_lists( list[i].children )
            new_list.append( list[i] )
    return new_list
	
