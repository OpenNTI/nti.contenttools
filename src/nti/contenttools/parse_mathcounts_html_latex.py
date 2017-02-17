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

import requests

from nti.contenttools import scoped_registry

from nti.contenttools.mathcounts_parser import MathcountsHTMLParser

from nti.contenttools.util import string_replacer

DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

def _parse_args():
	arg_parser = argparse.ArgumentParser(description="NTI Mathcounts HTML -Latex Parser")
	arg_parser.add_argument('inputfile',
							 help="HTML file title")
	arg_parser.add_argument('-o', '--output',
							 default='output',
							 help="The output directory. The default is: %s" % 'output')
	return arg_parser.parse_args()

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

	# Create the output directory if it does not exist
	if not os.path.exists(args.output):
		os.mkdir(args.output)

	scoped_registry.output_directory = args.output

	inputfile = os.path.expanduser(args.inputfile)

	# Verify the input file exists
	if not os.path.exists(inputfile):
		logger.info('The source file, %s, does not exist.', inputfile)
		exit()
	script = u''

	with codecs.open(inputfile,'r', 'utf-8') as f:
		script = f.read()
	
	title = string_replacer.rename_filename(args.inputfile)
	title = title.replace('.html', '')
	scoped_registry.id = title
	scoped_registry.counter_id = 1

	parser = MathcountsHTMLParser(script)
	tex = parser.process()
	filepath = u'%s/%s.tex' %(scoped_registry.output_directory, title)
	with codecs.open(filepath,'w', 'utf-8') as file_:
		file_.write(tex)
		
if __name__ == '__main__':  # pragma: no cover
	main()
