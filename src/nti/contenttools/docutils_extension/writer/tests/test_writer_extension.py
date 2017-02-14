#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: test_writer_extension.py 105532 2017-01-31 15:52:58Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from hamcrest import assert_that
from hamcrest import contains_string

import os

from nti.contenttools.docutils_extension.writer import latex
from nti.contenttools.tests import ContentToolsTestCase


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
    return os.path.join(os.path.dirname(__file__), filename)


class TestNTIWriter(ContentToolsTestCase):

    def test_package_requirements(self):
        rst = read_file(get_relative_path('data/section.rst'))
        tex = latex.generate_tex_from_rst(rst)
        assert_that(tex, contains_string(u'\\usepackage{ulem}'))
        assert_that(tex, contains_string(u'\\usepackage{Tabbing}'))
        assert_that(tex, contains_string(u'\\usepackage{textgreek}'))
        assert_that(tex, contains_string(u'\\usepackage{nticourse}'))
        assert_that(tex, contains_string(u'\\usepackage{ntiassessment}'))
        assert_that(tex, contains_string(u'\\usepackage{ntislidedeck}'))
        assert_that(tex, contains_string(u'\\usepackage{ntiglossary}'))
        assert_that(tex, contains_string(u'\\usepackage{ntilatexmacros}'))


class TestWriterExtension(ContentToolsTestCase):

    def test_section(self):
        rst = read_file(get_relative_path('data/section.rst'))
        self.assertTrue(isinstance(rst, basestring))
        tex = latex.generate_tex_from_rst(rst)
        self.assertTrue(isinstance(tex, basestring))
        assert_that(tex, contains_string(u'\\section'))
        assert_that(tex, contains_string(u'\\subsection'))

    def test_list(self):
        rst = read_file(get_relative_path('data/lists.rst'))
        self.assertTrue(isinstance(rst, basestring))
        tex = latex.generate_tex_from_rst(rst)
        self.assertTrue(isinstance(tex, basestring))
        assert_that(tex, contains_string(u'\\begin{itemize}'))
        assert_that(tex, contains_string(u'\\end{itemize}'))
        assert_that(tex, contains_string(u'\\begin{enumerate}'))
        assert_that(tex, contains_string(u'\\end{enumerate}'))

    def test_nested_list(self):
        rst = read_file(get_relative_path('data/bulleted_list.rst'))
        self.assertTrue(isinstance(rst, basestring))
        tex = latex.generate_tex_from_rst(rst)
        self.assertTrue(isinstance(tex, basestring))
        assert_that(tex, contains_string(u'\\begin{itemize}'))
        assert_that(tex, contains_string(u'\\end{itemize}'))
    
    def test_paragraph(self):
        rst = read_file(get_relative_path('data/paragraph.rst'))
        self.assertTrue(isinstance(rst, basestring))
        tex = latex.generate_tex_from_rst(rst)
        assert_that(tex, contains_string(u"You see? It's curious. Ted did figure it out - time travel. And when we get back, we gonna tell everyone. How it's possible, how it's done, what the dangers are."))

    def test_references(self):
        rst = read_file(get_relative_path('data/references.rst'))
        self.assertTrue(isinstance(rst, basestring))
        tex = latex.generate_tex_from_rst(rst)
        self.assertTrue(isinstance(tex, basestring))
        assert_that(tex, contains_string(u'{hyperref}'))
        assert_that(tex, contains_string(u'{External Hyperlink Targets}'))
        assert_that(tex, contains_string(
            u'\\href{http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html\#embedded-uris}{here}'))
        # todo : check inline styles
        assert_that(tex, contains_string(u'\\hyperref[inline-styles]{Inline Styles}'))

    def test_custom(self):
        rst = read_file(get_relative_path('data/custom.rst'))
        self.assertTrue(isinstance(rst, basestring))
        tex = latex.generate_tex_from_rst(rst)
        self.assertTrue(isinstance(tex, basestring))
        write_file(get_relative_path('test_result/custom.tex'), tex)
        assert_that(tex, contains_string(u'\\textbf{\\emph{bolditalic}}'))
        assert_that(tex, contains_string(u'\\textbf{\\underline{boldunderline}}'))
        assert_that(tex, contains_string(u'\\emph{\\underline{italicunderlined}}'))
        assert_that(
            tex,
            contains_string(u'\\textbf{\\emph{\\underline{bolditalicunderlined}}}'))
