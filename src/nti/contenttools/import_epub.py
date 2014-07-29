#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import codecs
import argparse

from .epub.epub import EPUBFile

def _parse_args():
    arg_parser = argparse.ArgumentParser( description="NTI EPUB Converter" )
    arg_parser.add_argument( 'inputfile', help="The EPUB file" )
    arg_parser.add_argument( '-o', '--output', default='output',
                             help="The output directory. The default is: %s" % 'output' )
    return arg_parser.parse_args()

def _title_escape( title ):
    return title.replace(' ', '_').replace('-','_').replace(':','_')

def main():
    # Parse command line args
    args = _parse_args()
    inputfile = os.path.expanduser(args.inputfile)

    # Verify the input file exists
    if not os.path.exists( inputfile ):
        print( 'The source file, %s, does not exist.' % inputfile )
        exit()

    # Create the output directory if it does not exist
    if not os.path.exists( args.output ):
        os.mkdir( args.output )

    epub = EPUBFile(args.inputfile)
    if epub.title:
        outputfile = os.path.join(args.output, _title_escape(epub.title)+'.tex')
    else:
        outputfile = os.path.join(args.output, _title_escape(os.path.splitext(inputfile)[0])+'.tex')
    with codecs.open( outputfile, 'w', 'utf-8' ) as fp:
        fp.write( epub.render() )

    epub.get_media(args.output)


if __name__ == '__main__': # pragma: no cover
    main()
