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

from .docx.read import DocxFile
from nti.contenttools.renders import LaTeX

def _parse_args():
	arg_parser = argparse.ArgumentParser( description="NTI DOCX Converter" )
	arg_parser.add_argument( 'inputfile', help="The DOCX file" )
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

	# Open document from input string
	print('Beginning Conversion of ' + inputfile)

	docxFile = DocxFile( inputfile )
	if docxFile.title:
		outputfile = os.path.join(args.output, _title_escape(docxFile.title)+'.tex')
	else:
		outputfile = os.path.join(args.output, _title_escape(os.path.splitext(os.path.basename(inputfile))[0])+'.tex')
	with codecs.open( outputfile, 'w', 'utf-8' ) as fp:
		fp.write( docxFile.render() )

	# Copy Document Images to Subfolder
	img_exportfolder = os.path.join(os.path.abspath(os.path.dirname(outputfile)), docxFile.image_dir)
	docxFile.get_images( img_exportfolder )
	
	print('Conversion successful, output written to ' + outputfile)

if __name__ == '__main__': # pragma: no cover
	main()
