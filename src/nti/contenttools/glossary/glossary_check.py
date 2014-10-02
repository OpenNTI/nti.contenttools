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

def process_glossary(glossary_dict, filename):
        content = get_file_content(filename)
        content = content.decode('utf-8')
        for key in glossary_dict.keys():
                key_text =key.rstrip()
                search_text = u'\\ntiglossaryentry{\\textbf{%s}}{definition}' % (key_text)
                definition = glossary_dict[key].rstrip()
                new_text = u'\\ntiglossaryentry{\\textbf{%s}}{%s}' % (key_text, definition)
                logger.info(new_text)
                content = content.replace(search_text, new_text)
        new_content = content
        replace_file_content(filename, new_content)


def get_file_content(filename):
        file_str = u''
        with codecs.open(filename) as fp:
                file_str = fp.read()
        return file_str


def replace_file_content(filename, new_content):
        with codecs.open( filename, 'w', 'utf-8' ) as fp:
                fp.write(new_content)
