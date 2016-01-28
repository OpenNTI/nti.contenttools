#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: parse_html_latex.py 58552 2015-01-29 23:10:30Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import logging
import argparse
import requests


from .html_parser import HTMLParser

from . import scoped_registry

DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

def _parse_args():
	arg_parser = argparse.ArgumentParser(description="NTI EPUB-Latex Parser")
	arg_parser.add_argument('url',
							 help="url")
	arg_parser.add_argument('-iu', '--image_url',
							 help="url to retrieve images")
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

	url = args.url
	scoped_registry.image_url = args.image_url 
	scoped_registry.output_directory = args.output
	response = requests.get(url, stream=True)
	if response.status_code == 200:
		script = response.content
		parser = HTMLParser(script)
		tex = parser.process()

if __name__ == '__main__':  # pragma: no cover
	main()
