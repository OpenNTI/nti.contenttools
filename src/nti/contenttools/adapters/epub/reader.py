#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
from zipfile import ZipFile

from lxml import html
from lxml import etree

from nti.contenttools import types

etree_fromstring = getattr(etree, 'fromstring')


class EPUBReader(object):
    """
    Class to open and read EPUB documents.
    """

    @classmethod
    def _get_rootfile(cls, container):
        rootfilename = ''
        for child in container:
            if child.tag == '{urn:oasis:names:tc:opendocument:xmlns:container}rootfiles':
                for rootfile in child:
                    if rootfile.attrib['media-type'] == 'application/oebps-package+xml':
                        rootfilename = rootfile.attrib['full-path']
                        break
        return rootfilename

    @classmethod
    def _extract_manifest(cls, manifest):
        result = {}
        for item in manifest:
            if hasattr(item, 'tag') \
                    and item.tag == '{http://www.idpf.org/2007/opf}item':
                result[item.attrib['id']] = {
                    'href': item.attrib['href'],
                    'media-type': item.attrib['media-type']
                }
        return result

    @classmethod
    def _extract_metadata(cls, metadata):
        result = {}
        for element in metadata:
            if element.tag == '{http://purl.org/dc/elements/1.1/}title':
                result['title'] = unicode(element.text)
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

    @classmethod
    def _extract_spine(cls, spine):
        result = []
        for itemref in spine:
            result.append(itemref.attrib['idref'])
        return result

    def __init__(self, source, epub):
        self.zipfile = ZipFile(source)
        epub.zipfile = self.zipfile
        self.metadata = {}
        self.manifest = {}
        self.spine = []
        self.audio_list = []
        self.image_list = []
        self.video_list = []

        container = etree_fromstring(
            self.zipfile.read(u'META-INF/container.xml'))
        rootfile = etree_fromstring(
            self.zipfile.read(self._get_rootfile(container)))
        self.content_path = os.path.dirname(self._get_rootfile(container))
        epub.content_path = self.content_path

        for element in rootfile:
            logger.info(element)
            if element.tag == '{http://www.idpf.org/2007/opf}metadata':
                self.metadata = self._extract_metadata(element)
            elif element.tag == '{http://www.idpf.org/2007/opf}manifest':
                self.manifest = self._extract_manifest(element)
            elif element.tag == '{http://www.idpf.org/2007/opf}spine':
                self.spine = self._extract_spine(element)
            elif element.tag == '{http://www.idpf.org/2007/opf}guide':
                pass
            else:
                print('Unknown element: %s' % element.tag)

        self.title = u''
        if 'title' in self.metadata.keys():
            self.title = self.metadata['title']

        self.author = u''
        if 'creator' in self.metadata.keys():
            self.author = self.metadata['creator']

        logger.info('SPINE: %s', self.spine)
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
                spine_dict.update({item: check_item})
                docfragment = html.fromstring(
                    self.zipfile.read(
                        self.content_path +
                        '/' +
                        self.manifest[item]['href']))
                docfrags.update({item: docfragment})

        self.document = types.Document()
        self.document.author = self.author
        self.document.title = self.title
        self.docfrags = docfrags
