#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from IPython.core.debugger import Tracer

import os
import shutil
import subprocess

from argparse import ArgumentParser
from lxml import etree, html
from lxml.html import html5parser, XHTMLParser
from tempfile import mkdtemp
from zipfile import ZipFile

from .adapters import openstax as Adapter
from .. import types

from nti.contenttools.renders import LaTeX

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
        self.metadata = {}
        self.manifest = {}
        self.spine = []
        self.audio_list = []
        self.image_list = []
        self.video_list = []

        container = etree.fromstring(self.zipfile.read(u'META-INF/container.xml'))
        rootfile = etree.fromstring(self.zipfile.read(_get_rootfile( container )))
        self.content_path = os.path.dirname(_get_rootfile( container ))
        logger.info('container %s', container)
        logger.info('rootfile %s', rootfile)
        logger.info('_get_rootfile( container ) %s', _get_rootfile( container ))
        logger.info('content_path %s', self.content_path)

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

        docfrags = []
        doc_body = types.EPUBBody()
        # Create a special parser for dealing with the content files
        parser = XHTMLParser(load_dtd=True,dtd_validation=True)
        logger.info('SPINE: %s',self.spine)
        check_item = False
        for item in self.spine:
            logger.info('---------------------------------')
            logger.info('SPINE ITEM >> %s', item)
            logger.info('>>')
            if item in [u'id416082', u'id504556', 'id505853'] and not check_item:
                docfragment = html.fromstring(self.zipfile.read(self.content_path+'/'+self.manifest[item]['href']))
                check_item = True
                for child in Adapter.adapt( docfragment, self, item ):
                    doc_body.add_child(child)
            elif item in [u'id416082', u'id504556', 'id505853'] and check_item:
                logger.info ('found spine %s more than once',item)
            elif item in ['htmltoc', 'id903065','id4497651', 'id4497666']:
                #TODO we can specify the list of spine item that we do not need in command line
                logger.info('found htmltoc or index Glossary or things we do not want to put it the latex files')
            else:
                docfragment = html.fromstring(self.zipfile.read(self.content_path+'/'+self.manifest[item]['href']))
                for child in Adapter.adapt( docfragment, self, item ):
                    doc_body.add_child(child)
            logger.info('---------------------------------')

        # Remove the first child of the body if it is a Chapter or Section object
        #if isinstance(doc_body.children[0], types.Chapter) or isinstance(doc_body.children[0], types.Section):
        #    doc_body.children.pop(0)

        self.document = types.Document()
        self.document.add_child(doc_body)
        self.document.title = self.title
        self.document.author = self.author

    def render(self):
        return self.document.render()

    def render_body_child(self, body_child):
        body_element = self.document.children[0].children[body_child]
        glossary_dict = None
        tex_content = body_element.render()
        if isinstance(body_element, types.Chapter):
            if len(body_element.children) == 0:
                pass
            elif isinstance(body_element.children[0], types.Run):
                run_element = body_element.children[0]
                child_num = self.check_glossary_element(run_element)
                if child_num > -1:
                    glossary_dict = run_element.children[child_num].glossary_dict
                    logger.info('found Glossary')
        return tex_content, glossary_dict 

    def check_glossary_element(self, element):
        child_num = 0
        for child in element:
            if isinstance(child, types.Glossary):
                return child_num
            child_num = child_num + 1
        return -1

    def get_media(self, output_dir='.'):
        self.get_images(output_dir)
        self.get_videos(output_dir)

    def get_images(self, output_dir='.'):
        logger.info ("STORE IMAGES")
        if self.image_list == []:
            logger.info ("NO IMAGE FOUND")
        for image in self.image_list:
            new_path = 'images/%s' %(image.path)
            path = os.path.join( output_dir, new_path )
            if not os.path.exists(os.path.dirname(path)):
                os.mkdir(os.path.dirname(path))
            image.data.seek(0)
            with open( path, 'wb' ) as file:
                file.write(image.data.read())

    def get_videos(self, output_dir='.'):
        # Convert output_dir to an absolute path
        output_dir = os.path.abspath( os.path.expanduser(output_dir) )
        # Create a temporary working directory
        working_dir = mkdtemp()
        # Store the current working directory
        orig_dir = os.getcwd()
        # Change the current working directory to the temp directory
        os.chdir( working_dir )
        try:
            for video in self.video_list:
                # Create the tmp working directories if it does not exist
                if not os.path.exists( os.path.join( working_dir, os.path.dirname( video.path ) ) ):
                    os.mkdir( os.path.join( working_dir, os.path.dirname( video.path ) ) )
                # Extract the original video from the EPUB
                with open( os.path.join( working_dir, video.path ), 'wb' ) as file:
                    file.write(self.zipfile.read(os.path.join(self.content_path, video.path)))
                # Create the output path if it does not exist
                if not os.path.exists( os.path.join( output_dir, os.path.dirname( video.path ) ) ):
                    os.mkdir( os.path.join( output_dir, os.path.dirname( video.path ) ) )
                # Transcode video, first to webm and then to mp4
                override = '-n'
                src = os.path.join( working_dir, video.path )

                dest = os.path.join( output_dir, os.path.splitext(video.path)[0] + '.webm' )
                cmd = [ 'ffmpeg', '-v', 'quiet', override, '-i', src, '-strict', '-2', dest ]
                subprocess.call( cmd )

                dest = os.path.join( output_dir, os.path.splitext(video.path)[0] + '.mp4' )
                cmd = [ 'ffmpeg', '-v', 'quiet', override, '-i', src, '-strict', '-2', dest ]
                subprocess.call( cmd )

                # Extract the poster files, if any
                if not os.path.exists(os.path.join( output_dir, os.path.dirname( video.thumbnail )) ):
                    os.mkdir( os.path.join( output_dir, os.path.dirname( video.thumbnail )) )
                video.thumbnaildata.seek(0)
                with open( os.path.join( output_dir, video.thumbnail ), 'wb' ) as file:
                    file.write(video.thumbnaildata.read())
        finally:
            # Return to the original working directory
            os.chdir( orig_dir )
            # Remove the temp directory
            shutil.rmtree( working_dir )

def _parse_args():
    arg_parser = ArgumentParser( description="NTI EPUB Converter" )
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
