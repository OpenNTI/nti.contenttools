#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: parse_epub_latex.py 58552 2015-01-29 23:10:30Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import codecs
import logging
import argparse
import simplejson as json

from .util import string_replacer
from .epub_parser import EPUBParser
from . import scoped_registry

DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

def _parse_args():
	arg_parser = argparse.ArgumentParser( description="NTI EPUB-Latex Parser" )
	arg_parser.add_argument( 'inputfile', 
							 help="The epub filepath" )
	arg_parser.add_argument( '-o', '--output', 
							 default='output',
							 help="The output directory. The default is: %s" % 'output' )
	return arg_parser.parse_args()

def _title_escape( title ):
	return string_replacer.rename_filename(title)

def _configure_logging(level='INFO'):
	numeric_level = getattr(logging, level.upper(), None)
	numeric_level = logging.INFO if not isinstance(numeric_level, int) else numeric_level
	logging.basicConfig(level=numeric_level)

def _setup_configs():
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

	# create a txt file to store information about image's name and location used in nticard
	scoped_registry.nticard_images_filename = os.path.join(args.output, 'nticard_images.txt')

	epub = EPUBParser(inputfile, args.output)
	epub.process_fragment()

if __name__ == '__main__': # pragma: no cover
	main()
