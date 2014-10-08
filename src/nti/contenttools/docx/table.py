#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import _DocxStructureElement
from . import process_border
from . import properties as docx
from .paragraph import Paragraph

class Table( _DocxStructureElement ):

    @classmethod
    def process( cls, table, doc, rels=None ):
        me = cls()
        me.grid = []
        me.borders = {}

        if rels is None:
            rels = doc.relationships

        # Parse element and determine table properties
        for element in table.iterchildren():
            if element.tag == '{'+docx.nsprefixes['w']+'}tblGrid':
                logger.info('processing grid\n%s' % me.grid)
                me.process_grid( element )
                logger.info(me.grid)
            elif element.tag == '{'+docx.nsprefixes['w']+'}tblPr':
                me.process_properties( element, doc, rels=rels )
            elif element.tag == '{'+docx.nsprefixes['w']+'}tr':
                me.add_child( cls.Row.process(element, doc, rels=rels ) )
            else:
                logger.warn('Did not handle table element: %s' % element.tag)
        return me

    class Row( _DocxStructureElement ):

        @classmethod
        def process( cls, row, doc, rels=None ):
            me = cls()

            if rels is None:
                rels = doc.relationships

            for element in row.iterchildren():
                if element.tag == '{'+docx.nsprefixes['w']+'}tc':
                    me.add_child( cls.Cell.process( element, doc, rels=rels ) )
                elif element.tag == '{'+docx.nsprefixes['w']+'}trPr':
                    me.process_properties( element )
                elif element.tag == '{'+docx.nsprefixes['w']+'}tblPrEx':
                    pass
                else:
                    logger.warn('Did not handle table row element: %s' % element.tag)
            return me

        class Cell( _DocxStructureElement ):
            
            @classmethod
            def process( cls, cell, doc, rels=None ):
                me = cls()
                me.grid_span = 1

                if rels is None:
                    rels = doc.relationships

                for element in cell.iterchildren():
                    if element.tag == '{'+docx.nsprefixes['w']+'}p':
                        me.add_child( Paragraph.process( element, doc, rels=rels ) )
                    elif element.tag == '{'+docx.nsprefixes['w']+'}tcPr':
                        me.process_properties( element )
                    else:
                        logger.warn('Did not handle table cell element: %s' % element.tag)

                return me

            def process_properties( self, properties ):
                for element in properties.iterchildren():
                    if element.tag == '{'+docx.nsprefixes['w']+'}cellDel':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}cellIns':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}cellMerge':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}cnfStyle':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}gridSpan':
                        self.grid_span = int(element.attrib['{'+docx.nsprefixes['w']+'}val'])
                        logger.info(self.grid_span)
                    elif element.tag == '{'+docx.nsprefixes['w']+'}headers':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}hideMark':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}hMerge':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}noWrap':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}shd':
                        # Shading is not supported yet
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}tcBorders':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}tcFitText':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}tcMar':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}tcPrChange':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}tcW':
                        value = element.attrib['{'+docx.nsprefixes['w']+'}w'] 
                        units = element.attrib['{'+docx.nsprefixes['w']+'}type']
                        self.width = ( value, units )
                    elif element.tag == '{'+docx.nsprefixes['w']+'}textDirection':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}vAlign':
                        pass
                    elif element.tag == '{'+docx.nsprefixes['w']+'}vMerge':
                        pass
                    else:
                        logger.warn('Did not handle cell property element: %s' % element.tag)

        def process_properties( self, properties ):
            for element in properties.iterchildren():
                if element.tag == '{'+docx.nsprefixes['w']+'}cantSplit':
                    # We do not require this infermation
                    pass
                elif element.tag == '{'+docx.nsprefixes['w']+'}cnfStyle':
                    # We do not support conditional formating at this time
                    pass
                elif element.tag == '{'+docx.nsprefixes['w']+'}del':
                    self.addStyle('strike')
                elif element.tag == '{'+docx.nsprefixes['w']+'}divId':
                    # We do not require this information
                    pass
                elif element.tag == '{'+docx.nsprefixes['w']+'}gridAfter':
                    self.gridAfter = element.attrib['{'+docx.nsprefixes['w']+'}val']
                elif element.tag == '{'+docx.nsprefixes['w']+'}gridBefore':
                    self.gridAfter = element.attrib['{'+docx.nsprefixes['w']+'}val']
                elif element.tag == '{'+docx.nsprefixes['w']+'}hidden':
                    self.addStyle('hidden')
                elif element.tag == '{'+docx.nsprefixes['w']+'}ins':
                    self.addStyle('modified')
                elif element.tag == '{'+docx.nsprefixes['w']+'}jc':
                    # We do not support specifying table alignment at this level
                    pass
                elif element.tag == '{'+docx.nsprefixes['w']+'}tblCellSpacing':
                    value = element.attrib['{'+docx.nsprefixes['w']+'}w'] 
                    units = element.attrib['{'+docx.nsprefixes['w']+'}type']
                    self.cellSpacing = ( value, units )
                elif element.tag == '{'+docx.nsprefixes['w']+'}tblHeader':
                    self.header = True
                elif element.tag == '{'+docx.nsprefixes['w']+'}trHeight':
                    mode = 'auto'
                    if '{'+docx.nsprefixes['w']+'}hRule' in element.attrib.keys():
                        mode = element.attrib['{'+docx.nsprefixes['w']+'}hRule']
                    value = element.attrib['{'+docx.nsprefixes['w']+'}val']
                    self.height = ( mode, value )
                elif element.tag == '{'+docx.nsprefixes['w']+'}trPrChange':
                    # We do not support displaying row property changes at this time
                    pass
                elif element.tag == '{'+docx.nsprefixes['w']+'}wAfter':
                    value = element.attrib['{'+docx.nsprefixes['w']+'}w'] 
                    units = element.attrib['{'+docx.nsprefixes['w']+'}type']
                    self.widthAfter = ( value, units )
                elif element.tag == '{'+docx.nsprefixes['w']+'}wBefore':
                    value = element.attrib['{'+docx.nsprefixes['w']+'}w'] 
                    units = element.attrib['{'+docx.nsprefixes['w']+'}type']
                    self.widthBefore = ( value, units )
                else:
                    logger.warn('Did not handle row property element: %s' % element.tag)

    def process_properties( self, properties, doc, rels=None ):
        if rels is None:
            rels = doc.relationships

        for element in properties.iterchildren():
            if element.tag == '{'+docx.nsprefixes['w']+'}tblBorders':
                self.borders = process_border( element )
            elif element.tag == '{'+docx.nsprefixes['w']+'}tblCaption':
                self.caption = element.attrib['{'+docx.nsprefixes['w']+'}val'] 
            elif element.tag == '{'+docx.nsprefixes['w']+'}tblDescription':
                self.description = element.attrib['{'+docx.nsprefixes['w']+'}val'] 
            elif element.tag == '{'+docx.nsprefixes['w']+'}tblLook':
                # tblLook is not supported, hence conditional formatting is not supported
                pass
            elif element.tag == '{'+docx.nsprefixes['w']+'}tblW':
                value = element.attrib['{'+docx.nsprefixes['w']+'}w'] 
                units = element.attrib['{'+docx.nsprefixes['w']+'}type']
                self.width = ( value, units )
            else:
                logger.warn('Did not handle table property element: %s' % element.tag)

    def process_grid( self, grid ):
        for element in grid.iterchildren():
            if element.tag == '{'+docx.nsprefixes['w']+'}gridCol':
                if '{'+docx.nsprefixes['w']+'}w' in element.attrib.keys():
                    self.grid.append(element.attrib['{'+docx.nsprefixes['w']+'}w'])
                else:
                    logger.warn('Did not handle table grid property: %s' % element.tag)
            elif element.tag == '{'+docx.nsprefixes['w']+'}tblGridChange':
                pass
            else:
                logger.warn('Did not handle table grid element: %s' % element.tag)

        logger.info( self.grid )
