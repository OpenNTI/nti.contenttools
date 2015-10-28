#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: epub_reader.py 71400 2015-08-24 03:32:32Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import shutil
import subprocess

from argparse import ArgumentParser
from lxml import etree, html
from lxml.html import html5parser, XHTMLParser
from tempfile import mkdtemp
from zipfile import ZipFile

from .. import scoped_registry
from .. import types

class EPUBReader( object ):
    """Class to open and read EPUB documents."""

    def __init__(self, file):
        def _get_rootfile(container):
            rootfilename = ''
            for child in container:
                if child.tag == '{urn:oasis:names:tc:opendocument:xmlns:container}rootfiles':
                    for rootfile in child:
                        if rootfile.attrib['media-type'] == 'application/oebps-package+xml':
                            rootfilename = rootfile.attrib['full-path']
                            break;
            return rootfilename

        def _extract_manifest( manifest ):
            result = {}
            for item in manifest:
                if hasattr(item, 'tag') and item.tag == '{http://www.idpf.org/2007/opf}item':
                    result[item.attrib['id']] = { 'href': item.attrib['href'],
                                              'media-type': item.attrib['media-type'] }
            return result

        def _extract_metadata( metadata ):
            result = {}
            for element in metadata:
                if element.tag == '{http://purl.org/dc/elements/1.1/}title':
                    result['title'] = element.text
                elif element.tag == '{http://purl.org/dc/elements/1.1/}creator':
                    result['creator'] = element.text
                elif element.tag == '{http://purl.org/dc/elements/1.1/}publisher':
                    result['publisher'] = element.text
                elif element.tag == '{http://purl.org/dc/elements/1.1/}format':
                    result['formate'] = element.text
                elif element.tag == '{http://purl.org/dc/elements/1.1/}date':
                    result['date'] = element.text
                elif element.tag == '{http://purl.org/dc/elements/1.1/}subject':
                    result['subject'] = element.text
                elif element.tag == '{http://purl.org/dc/elements/1.1/}description':
                    result['description'] = element.text
                elif element.tag == '{http://purl.org/dc/elements/1.1/}rights':
                    result['rights'] = element.text
                elif element.tag == '{http://purl.org/dc/elements/1.1/}language':
                    result['language'] = element.text
                elif element.tag == '{http://purl.org/dc/elements/1.1/}identifier':
                    result['identifier'] = element.text
                elif element.tag == '{http://www.idpf.org/2007/opf}meta':
                    result['meta'] = element.text
                else:
                    print('Unknown element: %s' % element.tag)
            return result

        def _extract_spine( spine ):
            result = []
            for itemref in spine:
                result.append(itemref.attrib['idref'])
            return result

        self.zipfile = ZipFile( file )
        scoped_registry.zipfile = self.zipfile
        self.metadata = {}
        self.manifest = {}
        self.spine = []
        self.audio_list = []
        self.image_list = []
        self.video_list = []

        container = etree.fromstring(self.zipfile.read(u'META-INF/container.xml'))
        rootfile = etree.fromstring(self.zipfile.read(_get_rootfile( container )))
        self.content_path = os.path.dirname(_get_rootfile( container ))
        scoped_registry.content_path = self.content_path

        for element in rootfile:
            logger.info(element)
            if element.tag == '{http://www.idpf.org/2007/opf}metadata':
                self.metadata = _extract_metadata(element)
            elif element.tag == '{http://www.idpf.org/2007/opf}manifest':
                self.manifest = _extract_manifest(element)
            elif element.tag == '{http://www.idpf.org/2007/opf}spine':
                self.spine = _extract_spine(element)
            elif element.tag == '{http://www.idpf.org/2007/opf}guide':
                pass
            else:
                print('Unknown element: %s' % element.tag)

        #print(self.spine)
        self.title = u''
        if 'title' in self.metadata.keys():
            self.title = self.metadata['title']

        self.author = u''
        if 'creator' in self.metadata.keys():
            self.author = self.metadata['creator']

        
        # Create a special parser for dealing with the content files
        parser = XHTMLParser(load_dtd=True,dtd_validation=True)
        logger.info('SPINE: %s',self.spine)
        check_item = False
        spine_dict = {}
        docfrags = {}
        for item in self.spine:
            logger.info('---------------------------------')
            logger.info('SPINE ITEM >> %s', item)
            logger.info('>>')
            if item in spine_dict.keys():
                spine_dict[item] = True
            elif item in ['htmltoc']:
                pass
            else:
                spine_dict.update({item:check_item})
                docfragment = html.fromstring(self.zipfile.read(self.content_path+'/'+self.manifest[item]['href']))
                docfrags.update({item:docfragment})
                

        self.document = types.Document()
        self.document.title = self.title
        scoped_registry.book_title = self.title
        self.document.author = self.author
        self.docfrags = docfrags

    
