#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import codecs

from nti.contenttools.adapters.epub.reader import EPUBReader

from nti.contenttools.adapters.epub.ifsta import adapt as adapt_ifsta

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.renderers.LaTeX.base import render_node

from nti.contenttools.util.string_replacer import rename_filename

from nti.contenttools.types.interfaces import IEPUBBody


class EPUBParser(object):

    def __init__(self, input_file, output_directory, epub_type):
        self.image_list = []
        self.latex_filenames = []
        self.content_folder = []  # will be use to retrieve images or pdf
        self.epub_type = epub_type

        self.input_file = input_file
        self.output_directory = output_directory
        self.tex_filepath = []

        self.epub_reader = EPUBReader(input_file, self)
        main_title = rename_filename(self.epub_reader.title)
        self.book_title = main_title
        self.tex_main_file = u'MAIN_%s.tex' % main_title

    def process_fragment(self):
        epub_reader = self.epub_reader
        docfrags = epub_reader.docfrags
        self.latex_filenames = []
        for item in epub_reader.spine:
            fragment = docfrags[item]
            self.current_dir = item
            if self.epub_type == 'ifsta':
                epub_chapter = adapt_ifsta(fragment, self)
            else:
                pass
                # TODO create generic adapter
                #epub_chapter = adapt(fragment)
            tex_filename = u'%s.tex' % rename_filename(item)
            self.latex_filenames.append(tex_filename)
            if IEPUBBody.providedBy(epub_chapter):
                logger.debug('render EPUB body')
                logger.debug(epub_chapter)
                # TODO : find out why line 65 causes ComponentLookupError(object, interface, name)
                # HOWEVER nose2 -v  -s
                # src/nti/contenttools/adapters/epub/ifsta/tests/ test_document
                # is OK
                context = DefaultRendererContext(name="LaTeX")
                render_node(context, epub_chapter)
                self.write_to_file(context.read(), tex_filename)
        self.create_main_latex()
        logger.info(epub_reader.spine)

    def create_main_latex(self):
        main_tex_content = generate_main_tex_content(self.epub_reader.metadata,
                                                     self.latex_filenames)
        self.write_to_file(main_tex_content, self.tex_main_file)

    def write_to_file(self, content, filename, type_=None):
        if type_ is None:
            filepath = u'%s/%s' % (self.output_directory, filename)
            self.tex_filepath.append(filepath)
            with codecs.open(filepath, 'w', 'utf-8') as file_:
                file_.write(content)


def get_packages():
    LATEX_PACKAGES = (u'graphix',
                      u'hyperref',
                      u'ulem',
                      u'Tabbing',
                      u'textgreek',
                      u'amsmath',
                      u'nticourse',
                      u'ntilatexmacros',
                      u'ntiassessment',
                      u'ntislidedeck',
                      u'ntiglossary',
                      )
    package_list = []
    package_list_append = package_list.append
    for package in LATEX_PACKAGES:
        string = u'\\usepackage{%s}\n' % (package)
        package_list_append(string)
    return u''.join(package_list)


def get_included_tex(included_tex_list):
    result = []
    result_append = result.append
    for tex in included_tex_list:
        inc = u'\\include{%s}\n' % (tex)
        result_append(inc)
    return u''.join(result)


DOC_STRING = u'\\documentclass{book}\n%s%s%s\\begin{document}\n%s\\end{document}'


def generate_main_tex_content(metadata, included_tex_list):
    author = u''
    title = u'\\title{%s}\n' % metadata[u'title'] if 'title' in metadata else u''
    if u'creator' in metadata.keys():
        author = u'\\author{%s}\n' % metadata['creator']
    package = get_packages()
    latex = get_included_tex(included_tex_list)
    return DOC_STRING % (package, title, author, latex)
