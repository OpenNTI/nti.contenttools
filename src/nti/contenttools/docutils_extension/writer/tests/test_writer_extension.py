#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: test_writer_extension.py 105532 2017-01-31 15:52:58Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from unittest import TestCase

import os

from nti.contenttools.docutils_extension.writer import latex

def read_file(filename):
    with open(filename, 'r') as rfile:
        data = rfile.read()
    return data


def write_file(filename, data):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, 'w') as wfile:
        wfile.write(data)

def get_relative_path(filename):
    return os.path.join(os.path.dirname(__file__),filename)

class TestWriterExtension(TestCase):

    def test_section(self):
        rst = read_file(get_relative_path('data/section.rst'))
        self.assertTrue(isinstance(rst, basestring))
        tex = latex.generate_tex_from_rst(rst)
        self.assertTrue(isinstance(rst, basestring))
        write_file(get_relative_path('test_result/section.tex'), tex)
    
    def test_custom(self):
        rst = read_file(get_relative_path('data/custom.rst'))
        self.assertTrue(isinstance(rst, basestring))
        tex = latex.generate_tex_from_rst(rst)
        self.assertTrue(isinstance(rst, basestring))
        write_file(get_relative_path('test_result/custom.tex'), tex)
