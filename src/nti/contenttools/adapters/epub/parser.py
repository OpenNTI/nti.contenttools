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

import simplejson as json

from nti.contenttools.adapters.epub.reader import EPUBReader

from nti.contenttools.adapters.epub.ifsta import adapt as adapt_ifsta

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.renderers.LaTeX.base import render_node

from nti.contenttools.renderers.LaTeX.utils import create_label

from nti.contenttools.util.string_replacer import rename_filename

from nti.contenttools.types.interfaces import ISidebar
from nti.contenttools.types.interfaces import IEPUBBody

EPUB_COURSE_TYPE = (u'ifsta')


class EPUBParser(object):

    def __init__(self, input_file, output_directory, epub_type, css_json=None):
        self.image_list = []
        self.latex_filenames = []
        self.content_folder = []  # will be use to retrieve images or pdf
        self.epub_type = epub_type

        self.input_file = input_file
        self.output_directory = output_directory

        self.section_list = []
        self.subsection_list = []
        self.glossary_terms = {}
        self.glossary_labels = []
        self.figure_labels = {}
        self.css_dict = {}
        self.captions = {}
        self.figures = []

        self.epub_reader = EPUBReader(input_file, self)
        main_title = rename_filename(self.epub_reader.title)
        self.book_title = main_title
        self.tex_main_file = u'MAIN_%s.tex' % main_title

        if epub_type in EPUB_COURSE_TYPE:
            data = (output_directory, self.book_title)
            reading_def_dir = u'%s/Definitions/Readings/%s' % data
            if not os.path.exists(reading_def_dir):
                os.makedirs(reading_def_dir)
            self.reading_def_dir = reading_def_dir
        else:
            self.reading_def_dir = None

        if css_json is not None:
            with codecs.open(css_json, 'r', 'utf-8') as fp:
                self.css_dict = json.load(fp)

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
                # TODO: create generic adapter
                # epub_chapter = adapt(fragment)
            tex_filename = u'%s.tex' % rename_filename(item)
            self.latex_filenames.append(tex_filename)
            logger.info("Processing ...")
            logger.info(tex_filename)
            if IEPUBBody.providedBy(epub_chapter):
                context = DefaultRendererContext(name="LaTeX")
                render_node(context, epub_chapter)
                if self.reading_def_dir:
                    self.write_to_file(context.read(),
                                       self.reading_def_dir,
                                       tex_filename)

                    generate_glossary_term_from_sidebar(epub_chapter,
                                                        self.glossary_terms,
                                                        self.glossary_labels)
                else:
                    self.write_to_file(context.read(),
                                       self.output_directory,
                                       tex_filename)
        self.create_main_latex()
        logger.info(epub_reader.spine)
        if self.reading_def_dir:
            self.process_support_files()

    def process_support_files(self):
        section_labels = generate_sectioning_list(self.section_list,
                                                  u'section')
        subsection_labels = generate_sectioning_list(self.subsection_list,
                                                     u'subsection')
        section_labels = section_labels + subsection_labels
        content = u''.join(section_labels)
        self.write_to_file(content,
                           self.output_directory,
                           'section_list.txt')

        glossaries = json.dumps(self.glossary_terms,
                                sort_keys=True,
                                indent='\t')
        self.write_to_file(glossaries, self.output_directory, 'glossary.json')

        glossary_labels = list(sorted(self.glossary_labels))
        glossary_labels_content = u''.join(glossary_labels)
        self.write_to_file(glossary_labels_content,
                           self.output_directory,
                           'glossary_label.txt')

        figure_labels = json.dumps(self.figure_labels,
                                   sort_keys=True,
                                   indent='\t')
        self.write_to_file(
            figure_labels, self.output_directory, 'figure_labels.json')

    def create_main_latex(self):
        if not self.reading_def_dir:
            main_tex_content = generate_main_tex_content(self.epub_reader.metadata,
                                                         self.latex_filenames)
        else:
            included = get_included_tex(self.latex_filenames, self.book_title)
            reading_def = u'\\chapter{Readings}\n\n%s' % included
            reading_dir = u'%s/Definitions/Readings/' % (self.output_directory)
            self.write_to_file(reading_def, reading_dir, u'Readings.tex')

            latex_main_list = (u'Definitions/Readings/Readings.tex',)
            main_tex_content = generate_main_tex_content(self.epub_reader.metadata,
                                                         latex_main_list)
        self.write_to_file(main_tex_content,
                           self.output_directory,
                           self.tex_main_file)

    def write_to_file(self, content, folder, filename):
        filepath = u'%s/%s' % (folder, filename)
        with codecs.open(filepath, 'w', 'utf-8') as fp:
            fp.write(content)


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


def get_included_tex(included_tex_list, sub_dir=None):
    result = []
    result_append = result.append
    for tex in included_tex_list:
        if sub_dir:
            inc = u'\\include{%s/%s}\n' % (sub_dir, tex)
        else:
            inc = u'\\include{%s}\n' % (tex)
        result_append(inc)
    return u''.join(result)


DOC_STRING = u'\\documentclass{book}\n%s%s%s\\begin{document}\n%s\\end{document}'


def generate_main_tex_content(metadata, included_tex_list):
    title = author = u''
    if 'title' in metadata:
        title = u'\\title{%s}\n' % metadata[u'title']
    if u'creator' in metadata.keys():
        author = u'\\author{%s}\n' % metadata['creator']
    package = get_packages()
    latex = get_included_tex(included_tex_list)
    return DOC_STRING % (package, title, author, latex)


def generate_sectioning_list(labels, section_type):
    rendered_labels = []
    for label in labels:
        label = create_label(section_type, label)
        label = label.replace(u'\\label', u'\\ref')
        label = u'%s\\\\\n' % (label)
        rendered_labels.append(label)
    return rendered_labels


def generate_glossary_term_from_sidebar(epub_body, glossary_terms, glossary_labels):
    search_sidebar_term(epub_body, glossary_terms, glossary_labels)


def search_sidebar_term(root, sidebars, labels):
    if ISidebar.providedBy(root):
        if root.type == u"sidebar_term":
            sidebars[root.title] = root.base
            if root.label:
                label = root.label.replace('\\label', '\\ref')
                label = u'%s\\\\\n' % (label)
                labels.append(label)
    elif hasattr(root, u'children'):
        for node in root:
            search_sidebar_term(node, sidebars, labels)
    return sidebars
