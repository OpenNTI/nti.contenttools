#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import six
import logging
import argparse

from nti.contenttools.adapters.epub.parser import EPUBParser

from nti.contenttools.util import string_replacer

DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'


def _parse_args():
    arg_parser = argparse.ArgumentParser(description="NTI EPUB-Latex Parser")
    arg_parser.add_argument('inputfile',
                            help="The epub filepath")
    arg_parser.add_argument('-o', '--output',
                            default='output',
                            help="The output directory. The default is: %s" % 'output')
    arg_parser.add_argument('-t', '--type',
                            default='generic',
                            help="The epub type. The default is: %s" % 'generic')
    return arg_parser.parse_args()


def _title_escape(title):
    return string_replacer.rename_filename(title)


def _configure_logging(level='INFO'):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, six.integer_types):
        numeric_level = logging.INFO
    logging.basicConfig(level=numeric_level)


def _setup_configs():
    _configure_logging()


def main():
    # Parse command line args
    args = _parse_args()

    _setup_configs()

    inputfile = os.path.expanduser(args.inputfile)

    # Verify the input file exists
    if not os.path.exists(inputfile):
        logger.info('The source file, %s, does not exist.', inputfile)
        exit()

    # Create the output directory if it does not exist
    if not os.path.exists(args.output):
        os.mkdir(args.output)

    # create a txt file to store information about image's name and location
    # used in nticard
    epub = EPUBParser(inputfile, args.output, args.type)
    epub.nticard_images_filename = os.path.join(args.output,
                                                'nticard_images.txt')
    epub.process_fragment()


if __name__ == '__main__':  # pragma: no cover
    main()
