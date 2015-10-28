#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: epub.py 58552 2015-01-29 23:10:30Z egawati.panjei $

Parse each index.cnxml.html found in each module to latex format

"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml import etree, html

import os
import codecs

from .epub_reader import EPUBReader
from .adapters import adapt
from ..util.string_replacer import rename_filename
from ..renders.LaTeX.base import base_renderer

from .. import scoped_registry
from .. import types


class EPUBParser(object):
    def __init__(self, input_file, output_directory):
        self.image_list = []
        self.latex_filenames = []
        self.content_folder = [] #will be use to retrieve images or pdf
        self.latex_main_files = u''

        self.input_file = input_file
        self.output_directory = output_directory
        scoped_registry.output_directory = output_directory
        self.tex_filepath = []

        self.epub_reader = EPUBReader(input_file)

        def process_fragment():
            epub_reader = self.epub_reader
            docfrags = epub_reader.docfrags
            for item in docfrags:
                fragment = docfrags[item]
                epub_chapter = adapt(fragment)
                logger.info('HERE')

        result = process_fragment()


