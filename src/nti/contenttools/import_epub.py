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
import codecs
import argparse
import logging
from zope.exceptions import log as ze_log
from . import types
from .epub.openstax_epub import EPUBFile
from .glossary import glossary_check

import simplejson as json
from collections import OrderedDict

DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

def _parse_args():
    arg_parser = argparse.ArgumentParser( description="NTI EPUB Converter" )
    arg_parser.add_argument( 'inputfile', help="The EPUB file" )
    arg_parser.add_argument( '-o', '--output', default='output',
                             help="The output directory. The default is: %s" % 'output' )
    return arg_parser.parse_args()

def _title_escape( title ):
    return title.replace(' ', '_').replace('-','_').replace(':','_')

def _configure_logging(level='INFO'):
    numeric_level = getattr(logging, level.upper(), None)
    numeric_level = logging.INFO if not isinstance(numeric_level, int) else numeric_level
    logging.basicConfig(level=numeric_level)
    logging.root.handlers[0].setFormatter(ze_log.Formatter(DEFAULT_FORMAT_STRING))

def _setup_configs():
    # logging
    _configure_logging()
    

def main():
    # Parse command line args
    args = _parse_args()

    _setup_configs()

    inputfile = os.path.expanduser(args.inputfile)

    # Verify the input file exists
    if not os.path.exists( inputfile ):
        logger.info( 'The source file, %s, does not exist.', inputfile )
        exit()

    # Create the output directory if it does not exist
    if not os.path.exists( args.output ):
        os.mkdir( args.output )

    epub = EPUBFile(args.inputfile)    
    logger.info ('Number of spine %s', len(epub.spine))
    if epub.title:
        outputfile = os.path.join(args.output, _title_escape(epub.title)+'.tex')
    else:
        outputfile = os.path.join(args.output, _title_escape(os.path.splitext(inputfile)[0])+'.tex')


    with codecs.open( outputfile, 'w', 'utf-8' ) as fp:
        fp.write( epub.render() )

    document = epub.document
    
    #since document only has one body
    body = document.children[0]
    body_child = 0
    glossary_file = os.path.join(args.output, 'glossary.json')
    global_glossary = {}
    for child in body:
        #write each body child into different latex file
        #we use this format : file_1.tex
        outputfile = os.path.join(args.output, 'file_'+str(body_child)+'.tex')
        logger.info('------------')
        logger.info(outputfile)
        tex_content, glossary_dict = epub.render_body_child(body_child)
        with codecs.open( outputfile, 'w', 'utf-8' ) as fp:
            fp.write(tex_content)
        if glossary_dict is not None:
            global_glossary.update(glossary_dict)
            glossary_check.process_glossary(glossary_dict, outputfile)
        body_child = body_child + 1
        logger.info('------------')

    #clean global glossary
    glossary = clean_global_glossary(global_glossary)
    #save glossary to json

    glossary_json = json.dumps(glossary, sort_keys=True, indent=4 * ' ')
    with codecs.open( glossary_file, 'w', 'utf-8' ) as fp:
        fp.write(glossary_json)
    epub.get_media(args.output)

def clean_global_glossary(glossary):
    for key in glossary.keys():
        value = glossary[key]
        new_value = value.rstrip('\n')
        glossary[key] = new_value
    return glossary

if __name__ == '__main__': # pragma: no cover
    main()
