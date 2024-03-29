#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import six
import logging
import argparse

from zope.component.hooks import setHooks

from zope.configuration import xmlconfig

import nti.contenttools

from nti.contenttools.adapters.common import prepare_site

from nti.contenttools.adapters.epub.parser import EPUBParser

from nti.contenttools.util import string_replacer

DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

logger = __import__('logging').getLogger(__name__)


def parse_args():
    arg_parser = argparse.ArgumentParser(description="NTI EPUB-Latex Parser")
    arg_parser.add_argument('inputfile',
                            help="The epub filepath")
    arg_parser.add_argument('-o', '--output',
                            default='output',
                            help="The output directory. The default is: %s" % 'output')
    arg_parser.add_argument('-t', '--type',
                            default='generic',
                            help="The epub type. The default is: %s" % 'generic')
    arg_parser.add_argument('-c', '--cssjson',
                            default=None,
                            help="""A json file converted from epub css. This is useful for fixed/reflowable epub
                            generated from Adobe InDesign""")
    arg_parser.add_argument('-ch', '--chapternum',
                            default=None,
                            help="The chapter number")
    arg_parser.add_argument('-s', '--site',
                            default='site',
                            help="The base components")
    arg_parser.add_argument('-pt', '--paraterm',
                            default=None,
                            help="Only use for special case")
    return arg_parser.parse_args()


def title_escape(title):
    return string_replacer.rename_filename(title)


def configure_logging(level='INFO'):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, six.integer_types):
        numeric_level = logging.INFO
    logging.basicConfig(level=numeric_level)


def setup_configs():
    configure_logging()


def setup_context(context=None):
    context = xmlconfig.file('configure.zcml',
                             package=nti.contenttools,
                             context=context)
    return context


def main():
    # Parse command line args
    args = parse_args()
    setup_configs()

    # Verify the input file exists
    inputfile = os.path.expanduser(args.inputfile)
    if not os.path.exists(inputfile):
        logger.info('The source file, %s, does not exist.', inputfile)
        exit()

    # Create the output directory if it does not exist
    if not os.path.exists(args.output):
        os.mkdir(args.output)

    setHooks()
    setup_context()
    prepare_site(args.site)

    # create a txt file to store information about image's name and location
    # used in nticard
    epub = EPUBParser(inputfile, args.output, args.type,
                      args.cssjson, args.chapternum, args.paraterm)
    epub.nticard_images_filename = os.path.join(args.output,
                                                'nticard_images.txt')
    epub.process_fragment()


if __name__ == '__main__':  # pragma: no cover
    main()
