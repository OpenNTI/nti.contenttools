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
import logging
import argparse

from zope.exceptions import log as ze_log

from .docx.read import DocxFile

DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

def _parse_args():
	arg_parser = argparse.ArgumentParser( description="NTI DOCX Converter" )
	arg_parser.add_argument( 'inputfile', help="The DOCX file" )
	arg_parser.add_argument( '-o', '--output', default='output',
							 help="The output directory. The default is: %s" % 'output' )
	return arg_parser.parse_args()

def _configure_logging(level='INFO'):
	numeric_level = getattr(logging, level.upper(), None)
	numeric_level = logging.INFO if not isinstance(numeric_level, int) else numeric_level
	logging.basicConfig(level=numeric_level)
	logging.root.handlers[0].setFormatter(ze_log.Formatter(DEFAULT_FORMAT_STRING))

def _setup_configs():
	_configure_logging()

def _title_escape( title ):
	return title.replace(' ', '_').replace('-','_').replace(':','_')

def main():
	# Parse command line args
	args = _parse_args()
	_setup_configs()
	inputfile = os.path.expanduser(args.inputfile)

	# Verify the input file exists
	if not os.path.exists( inputfile ):
		logger.info( 'The source file, %s, does not exist.' % inputfile )
		exit()

	# Create the output directory if it does not exist
	if not os.path.exists( args.output ):
		os.mkdir( args.output )

	# Open document from input string
	logger.info('Beginning Conversion of ' + inputfile)

	docxFile = DocxFile( inputfile )
	if docxFile.title:
		name = _title_escape(docxFile.title) + '.tex'
		outputfile = os.path.join(args.output, name)
	else:
		name = _title_escape(os.path.splitext(os.path.basename(inputfile))[0]) + '.tex'
		outputfile = os.path.join(args.output, name)
		
	with codecs.open( outputfile, 'w', 'utf-8' ) as fp:
		fp.write( docxFile.render() )

	# Copy Document Images to Subfolder
	img_exportfolder = os.path.join(os.path.abspath(os.path.dirname(outputfile)), docxFile.image_dir)
	docxFile.get_images( img_exportfolder )
	
	logger.info('Conversion successful, output written to ' + outputfile)

if __name__ == '__main__':
	main()
