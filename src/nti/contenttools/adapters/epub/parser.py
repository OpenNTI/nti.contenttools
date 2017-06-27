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

from collections import OrderedDict

from nti.contenttools.adapters.epub.reader import EPUBReader

from nti.contenttools.adapters.epub.ifsta import adapt as adapt_ifsta

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.renderers.LaTeX.base import render_node
from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.renderers.LaTeX.utils import create_label

from nti.contenttools.util.string_replacer import rename_filename

from nti.contenttools.types.interfaces import ISidebar
from nti.contenttools.types.interfaces import IEPUBBody

EPUB_COURSE_TYPE = (u'ifsta', u'ifsta_rf')


class EPUBParser(object):

    def __init__(self, input_file, output_directory, epub_type, css_json=None, chapter_num=None):
        self.image_list = []
        self.latex_filenames = []
        self.content_folder = []  # will be use to retrieve images or pdf
        self.epub_type = epub_type

        self.input_file = input_file
        self.output_directory = output_directory

        self.css_dict = {}
        self.captions = {}
        self.caption_list = []
        self.figure_labels = {}
        self.glossary_terms = {}
        
        self.figures = []
        self.figure_node = []
        self.figure_ref = {}

        self.sidebar_term_nodes = []
        
        self.section_list = []
        self.glossary_labels = []

        self.epub_reader = EPUBReader(input_file)
        self.epub_reader(self)
        main_title = rename_filename(self.epub_reader.title)
        self.book_title = main_title
        self.tex_main_file = u'MAIN_%s.tex' % main_title

        self.chapter_num = chapter_num

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
            if self.epub_type == 'ifsta' or self.epub_type == 'ifsta_rf':
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
                content = context.read()
                content = self.update_image_ref(content)
                if self.reading_def_dir:
                    self.write_to_file(content,
                                       self.reading_def_dir,
                                       tex_filename)
                    if self.epub_type == u'ifsta':
                        generate_glossary_term_from_sidebar(epub_chapter,
                                                        self.glossary_terms,
                                                        self.glossary_labels)
                else:
                    self.write_to_file(content,
                                       self.output_directory,
                                       tex_filename)
        self.create_main_latex()
        logger.info(epub_reader.spine)
        if self.reading_def_dir:
            self.process_support_files()

    def process_support_files(self):
        if self.epub_type == 'ifsta_rf':
            content_fig = self.generate_figure_tex()
            self.write_to_file(content_fig,
                self.output_directory,
                'Figures.tex')

            content_sidebar_term = self.generate_sidebar_terms_nodes()
            self.write_to_file(content_sidebar_term,
                self.output_directory,
                'SidebarTerms.tex')

        content = u''.join(self.section_list)
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


    def generate_figure_tex(self):
        figures = []
        for fig in self.figure_node:
            figures.append(render_output(fig))
        content = u'\n'.join(figures)
        return content

    def generate_sidebar_terms_nodes(self):
        sidebars = []
        for sidebar in self.sidebar_term_nodes:
            sidebars.append(render_output(sidebar))
            self.glossary_terms[sidebar.title] = sidebar.base
            if sidebar.label:
                label = sidebar.label.replace('\\label', '\\ref')
                label = u'%s\\\\\n' % (label)
                self.glossary_labels.append(label)
        content = u'\n'.join(sidebars)
        return content

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

    def update_image_ref(self, content):
        figure_ref = OrderedDict(sorted(self.figure_ref.items(), 
                                        key=lambda t: t[1], 
                                        reverse=False))
        figure_ref = list(figure_ref.items())
        for ref in figure_ref:
            content = content.replace(ref[0], ref[1])
        return content


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
