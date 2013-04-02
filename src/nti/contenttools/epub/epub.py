#!/usr/bin/env python2.7

import argparse
import os

from lxml import etree, html
from lxml.html import html5parser, XHTMLParser
from zipfile import ZipFile

from .adapters import wiley as Adapter
from .. import types

class EPUBFile( object ):
    """Class to open, read, and close EPUB documents."""

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
        self.metadata = {}
        self.manifest = {}
        self.spine = []
        self.image_list = []

        container = etree.fromstring(self.zipfile.read(u'META-INF/container.xml'))
        rootfile = etree.fromstring(self.zipfile.read(_get_rootfile( container )))
        self.content_path = os.path.dirname(_get_rootfile( container ))

        for element in rootfile:
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

        self.title = u''
        if 'title' in self.metadata.keys():
            self.title = self.metadata['title']

        self.author = u''
        if 'creator' in self.metadata.keys():
            self.author = self.metadata['creator']

        docfrags = []
        doc_body = types.Body()
        # Create a special parser for dealing with the content files
        parser = XHTMLParser(load_dtd=True,dtd_validation=True)
        for item in self.spine:
            docfragment = html.fromstring(self.zipfile.read('OEBPS/'+self.manifest[item]['href']))
            for child in Adapter.adapt( docfragment, self, item ):
                doc_body.add_child( child )

        # Remove the first child of the body if it is a Chapter or Section object
        if isinstance(doc_body.children[0], types.Chapter) or isinstance(doc_body.children[0], types.Section):
            doc_body.children.pop(0)

        self.document = types.Document()
        self.document.add_child(doc_body)

        self.document.title = self.title
        self.document.author = self.author

    def render(self):
        return self.document.render()

    def get_images(self, output_dir='.'):
        for image in self.image_list:
            path = os.path.join( output_dir, image.path )
            if not os.path.exists(os.path.dirname(path)):
                os.mkdir(os.path.dirname(path))
            image.data.seek(0)
            with open( path, 'wb' ) as file:
                file.write(image.data.read())


def _parse_args():
    arg_parser = argparse.ArgumentParser( description="NTI EPUB Converter" )
    arg_parser.add_argument( 'inputfile', help="The EPUB file" )
    return arg_parser.parse_args()

def main():
    # Parse command line args
    args = _parse_args()
    inputfile = os.path.expanduser(args.inputfile)

    # Verify the input file exists
    if not os.path.exists( inputfile ):
        print( 'The source file, %s, does not exist.' % inputfile )
        exit()

    doc = EPUBFile(args.inputfile)

if __name__ == '__main__': # pragma: no cover
    main()
