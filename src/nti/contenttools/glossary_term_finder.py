#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module is useful to find glossary terms (with particular pattern) inside a latex file 
We need to provide a dictionary of glossary (stored in json file) to be able to replace text 
inside the latex file with ntiglossary{key}{definition}

for example:
	a latex files exported from docx format has glossary terms written using pattern
	'\\textbf{'...'}' where '...' refers to any terms
	
	if we want to replace string like: '\\textbf{autorhythmicity}' with 
	{\\ntiglossaryentry
		{autorhythmicity}
		{ability of cardiac muscle to initiate its own electrical impulse that triggers the mechanical contraction that pumps blood at a fixed pace without nervous or endocrine control}
		...
	it will work if we have 'autorhythmicity' in dictionary key and its value pair
	we run this program by typing the following command:
	
	./bin/nti_glossary_finder -s textbf -g 'json files' 'latex files'

if we don't have glossary.json yet, create the json file from from txt file or docx file if we already have the glossary list in this format>> use nti_glossary_exporter

.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import sys
import logging
import argparse
import simplejson as json

from zope.exceptions import log as ze_log

from .glossary import glossary_check


DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

def _parse_args():
	arg_parser = argparse.ArgumentParser( description="NTI Glossary Terms Finder" )
	arg_parser.add_argument( 'filename', 
							 help="The latex file" )
	arg_parser.add_argument( '-g', '--glossary', 
							 default=None, 
							 help="json file contains glossary")
	arg_parser.add_argument( '-s', '--search', 
							 default=None, 
							 help="string/text to replace")
	return arg_parser.parse_args()

def _title_escape( title ):
	return title.replace(' ', '_').replace('-','_').replace(':','_')

def _configure_logging(level='INFO'):
	numeric_level = getattr(logging, level.upper(), None)
	numeric_level = logging.INFO if not isinstance(numeric_level, int) else numeric_level
	logging.basicConfig(level=numeric_level)
	logging.root.handlers[0].setFormatter(ze_log.Formatter(DEFAULT_FORMAT_STRING))

def _setup_configs():
	_configure_logging()

def main():
	# Parse command line args
	args = _parse_args()
	_setup_configs()

	filename = os.path.expanduser(args.filename)

	# Verify the input file exists
	if not os.path.exists(filename):
		logger.info( 'The source file, %s, does not exist.',filename)
		sys.exit(-2)

	glossary_json = args.glossary
	
	# Verify if the json file exists
	if not os.path.exists(glossary_json):
		logger.info('The json file, %s, does not exist.', filename)
		sys.exit(-3)

	json_str = glossary_check.get_file_content(glossary_json)
	glossary_dict = json.loads(json_str)

	search_text = args.search

	# replace text in the latex file
	if search_text is not None:
		glossary_check.process_glossary(glossary_dict, filename, search_text)
	else:
		logger.warn ("Please provide search_text, for example 'textbf'")
		
if __name__ == '__main__':
	main()
