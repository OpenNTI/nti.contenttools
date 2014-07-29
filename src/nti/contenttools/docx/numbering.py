#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import properties as docx

class _Level( object ):
    ignored = [ '{'+docx.nsprefixes['w']+'}lvlText',
                '{'+docx.nsprefixes['w']+'}lvlJc',
                '{'+docx.nsprefixes['w']+'}pPr',
                '{'+docx.nsprefixes['w']+'}pStyle',
                '{'+docx.nsprefixes['w']+'}rPr',
                '{'+docx.nsprefixes['w']+'}tentative',
                '{'+docx.nsprefixes['w']+'}tplc' ]

    def __init__( self, ilvl='0', start='1', format='Bullets' ):
        self.ilvl = ilvl
        self.start = start
        self.format = format

    @classmethod
    def process_element( cls, element ):
        _t = cls()

        for sub_element in element.iterchildren():
            if sub_element.tag == '{'+docx.nsprefixes['w']+'}start':
                _t.start = sub_element.attrib['{'+docx.nsprefixes['w']+'}val']
            elif sub_element.tag == '{'+docx.nsprefixes['w']+'}numFmt':
                _t.format = sub_element.attrib['{'+docx.nsprefixes['w']+'}val']
            elif sub_element.tag in cls.ignored:
                pass # We are not processing any tags/attribures in this list
            else:
                print( 'Did not handle level element: %s' % sub_element.tag )

        for attrib in element.attrib:
            if attrib == '{'+docx.nsprefixes['w']+'}ilvl':
                _t.ilvl = element.attrib[attrib]
            elif attrib in cls.ignored:
                pass # We are not processing any tags/attribures in this list
            else:
                print( 'Did not handle level attribute: %s' % attrib )

        return _t


class AbstractNumbering( object ):
    ignored = [ '{'+docx.nsprefixes['w']+'}multiLevelType',
                '{'+docx.nsprefixes['w']+'}nsid',
                '{'+docx.nsprefixes['w']+'}tmpl' ]
    
    def __init__( self, id='' ):
        self.id = id
        self.levels = {}

    @classmethod
    def process_element( cls, element ):
        _t = cls()

        for sub_element in element.iterchildren():
            if sub_element.tag == '{'+docx.nsprefixes['w']+'}lvl':
                l = _Level.process_element( sub_element )
                _t.levels[l.ilvl] = l
            elif sub_element.tag in cls.ignored:
                pass # We are not processing any tags/attribures in this list
            else:
                print( 'Did not handle abstract numbering element: %s' % sub_element.tag )

        for attrib in element.attrib:
            if attrib == '{'+docx.nsprefixes['w']+'}abstractNumId':
                _t.id = element.attrib[attrib]
            elif attrib in cls.ignored:
                pass # We are not processing any tags/attribures in this list
            else:
                print( 'Did not handle abstract numbering attribute: %s' % attrib )

        return _t

class Numbering( object ):

    def __init__( self, id='0', abstract_num_id='0' ):
        self.id = id
        self.abstract_num_id = abstract_num_id
        self.levels = {}

    @classmethod
    def process_element( cls, element ):
        _t = cls()

        for sub_element in element.iterchildren():
            if sub_element.tag == '{'+docx.nsprefixes['w']+'}abstractNumId':
                _t.abstract_num_id = sub_element.attrib['{'+docx.nsprefixes['w']+'}val']
            else:
                print( 'Did not handle numbering element: %s' % sub_element.tag )

        for attrib in element.attrib:
            if attrib == '{'+docx.nsprefixes['w']+'}numId':
                _t.id = element.attrib[attrib]
            else:
                print( 'Did not handle numbering attribute: %s' % attrib )

        return _t
    

def process_numbering( numbering ):
    a = {}
    n = {}

    for element in numbering.iterchildren():
        if element.tag == '{'+docx.nsprefixes['w']+'}abstractNum':
            _t = AbstractNumbering.process_element( element )
            a[_t.id] = _t
        elif element.tag == '{'+docx.nsprefixes['w']+'}num':
            _t = Numbering.process_element( element )
            n[_t.id] = _t
        else:
            print('Unhandled numbering tag: %s' % element.tag)

    for entry in n:
        n[entry].levels = a[n[entry].abstract_num_id].levels

    return a, n
