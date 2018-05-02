#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import re
import codecs

import simplejson as json

from collections import OrderedDict

from nti.contenttools.adapters.epub.reader import EPUBReader

from nti.contenttools.adapters.epub.tcia import adapt as adapt_tcia

from nti.contenttools.adapters.epub.ifsta import adapt as adapt_ifsta

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.renderers.LaTeX.base import render_node
from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.script.cleanup_tex_file import cleanup_subsubsection

from nti.contenttools.util.string_replacer import rename_filename

from nti.contenttools.types.interfaces import IParagraph
from nti.contenttools.types.interfaces import ISidebar
from nti.contenttools.types.interfaces import ITable
from nti.contenttools.types.interfaces import IEPUBBody

EPUB_COURSE_TYPE = (u'ifsta', u'ifsta_rf', u'tcia')

logger = __import__('logging').getLogger(__name__)


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
        self.glossary_entry_sections = []

        self.tables = []

        self.chapter_num = chapter_num

        self.epub_reader = EPUBReader(input_file)
        self.epub_reader(self)
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
            if item in docfrags.keys():
                fragment = docfrags[item]
                self.current_dir = item
                if self.epub_type == 'ifsta' or self.epub_type == 'ifsta_rf':
                    epub_chapter = adapt_ifsta(fragment, self)
                elif self.epub_type == 'tcia':
                    epub_chapter = adapt_tcia(fragment, self)
                else:
                    # TODO: create generic adapter
                    # epub_chapter = adapt(fragment)
                    pass
                tex_filename = u'%s.tex' % rename_filename(item)
                self.latex_filenames.append(tex_filename)
                logger.info("Processing ...")
                logger.info(tex_filename)
                if IEPUBBody.providedBy(epub_chapter):
                    context = DefaultRendererContext(name=u"LaTeX")
                    render_node(context, epub_chapter)
                    content = context.read()
                    content = self.update_image_ref(content)
                    content = self.cleanup_tex(content)
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
                self.tables = search_tables(epub_chapter, self.tables)

        self.create_main_latex()
        logger.info(epub_reader.spine)

        self.process_support_files()

    def cleanup_tex(self, content):
        # cleanup page number
        content = re.sub(r'(, p\.).[0-9]*[0-9]', u'', content)

        # consolidate list
        content = content.replace(u'\n\\end{itemize}\n\\begin{itemize}\n', u'')
        content = content.replace(u'\n\\end{itemize}\n\n\\begin{itemize}\n', u'')
        content = content.replace(u'\n\\end{itemize}\n\\\\\\begin{itemize}\n', u'')
        content = content.replace(u'\n\\end{itemize}\n\\\\ \n\n\\begin{itemize}\n', u'')

        # cleanup caption
        content = content.replace(u'\\caption{\\textbf{} ', u'\\caption{')
        content = content.replace(u'\\caption{\\textbf{ }', u'\\caption{')

        # remove extra newlines
        content = content.replace(u'\n\n\\end{itemize}', u'\n\\end{itemize}')
        content = content.replace(u'\n\n\n\n', u'\n\n')
        content = content.replace(u'\n\n\n', u'\n\n')

        # replace with subsubsection (works for book 1, 2 and 3)
        content = content.replace(u'\\textit{\\textbf{', 
                                  u'\\subsubsection{\\textit{')

        # cleanup extra newline after subsubsection
        content = cleanup_subsubsection(content)

        # cleanup extra newline before subsection and subsubsection
        content = content.replace(u'\\\\\n\n\n\\subsection{', u'\n\\subsection{')
        content = content.replace(u'\\\\\n\n\\subsection{', u'\n\\subsection{')
        content = content.replace(u'\\\\\n\n\\subsubsection{', u'\n\\subsubsection{')

        #remove unnecessary \newline
        content = content.replace(u'\\newline None', u'')

        #add css-class to sidebar
        content = content.replace(u'\\begin{sidebar}{CAUTION}', 
                                  u'\\begin{sidebar}[css-class=caution]{CAUTION}')

        content = content.replace(u'\\begin{sidebar}{WARNING}',
                                  u'\\begin{sidebar}[css-class=warning]{WARNING}')

        content = content.replace(u'\\begin{sidebar}{WARNING!}',
                                  u'\\begin{sidebar}[css-class=warning]{WARNING!}')
        
        content = content.replace(u'\\begin{sidebar}[css-class=note]{NOTE:}\nNOTE:',
                                  u'\\begin{sidebar}[css-class=note]{NOTE:}')
        content = content.replace(u'\\begin{sidebar}[css-class=note]{NOTE:}\n\\textbf{NOTE:}',
                                  u'\\begin{sidebar}[css-class=note]{NOTE:}')
        content = content.replace(u'\\begin{sidebar}[css-class=note]{NOTE:}\n\\textbf{NOTE: }',
                                  u'\\begin{sidebar}[css-class=note]{NOTE:}')

        content = content.replace(u'\\begin{sidebar}[css-class=note]{CAUTION:}\n\\textbf{CAUTION:}',
                                  u'\\begin{sidebar}[css-class=note]{CAUTION:}')
        content = content.replace(u'\\begin{sidebar}[css-class=note]{CAUTION:}\n\\textbf{CAUTION: }',
                                  u'\\begin{sidebar}[css-class=note]{CAUTION:}')

        content = content.replace(u'\\begin{sidebar}[css-class=note]{WARNING:}\n\\textbf{WARNING:}',
                                  u'\\begin{sidebar}[css-class=note]{WARNING:}')
        content = content.replace(u'\\begin{sidebar}[css-class=note]{WARNING:}\n\\textbf{WARNING: }',
                                  u'\\begin{sidebar}[css-class=note]{WARNING:}')
        content = content.replace(u'\\begin{sidebar}[css-class=note]{WARNING:}\n\\textbf{WARNING!:}',
                                  u'\\begin{sidebar}[css-class=note]{WARNING!:}')


        content = content.replace(u'\\\\ \n\n\\end{sidebar}', u'\n\\end{sidebar}')
        content = content.replace(u'\n\\end{sidebar}\n\\\\', u'\\end{sidebar}')
        content = content.replace(u'``', u'"')
        content = content.replace(u"''", u'"')

        content = content.replace(u"\\item *", u"\\item ")
        content = content.replace(u"*", u"\\item ")
        content = content.replace(u"\\renewcommand\\item ", u"\\renewcommand*")
        content = content.replace(u'\\item --- ', u'\\\\ --- ')

        content = content.replace(u'\n\\end{sidebar}\n\\\\\n\n\\begin{sidebar}{Case History}', u'')

        content = content.replace(u"\\textbf{ }", u" ")
        content = content.replace(u"\\textit{ }", u" ")
        content = content.replace(u"\\textbf{}", u"")
        content = content.replace(u"\\textit{}", u"")
        content = content.replace(u"‘", u"'")

        content = content.replace(u'\n\\end{itemize}\n\\begin{itemize}\n', u'\n')
        content = content.replace(u'\n\\end{itemize}\n\n\\begin{itemize}\n', u'\n')
        content = content.replace(u'\n\\end{itemize}\n\n\n\\begin{itemize}\n', u'\n')

        content = content.replace(u'\\ntiglossaryentry{ }{}', u'')

        content = content.replace(u'\\end{sidebar}\n\n\\begin{sidebar}{Case History}', u'\n')

        content = content.replace(u'\\end{quote}\n\\begin{quote}', u'')
        return content

    def process_support_files(self):
        support_dir = u'%s/SupportFiles' % self.output_directory
        if not os.path.exists(support_dir):
            os.makedirs(support_dir)

        if self.epub_type == 'ifsta_rf':
            content_fig = self.generate_figure_tex()
            self.write_to_file(content_fig,
                               support_dir,
                               'Figures.tex')

            content_sidebar_term = self.generate_sidebar_terms_nodes()
            self.write_to_file(content_sidebar_term,
                               support_dir,
                               'SidebarTerms.tex')

        content = u''.join(self.section_list)
        self.write_to_file(content,
                           support_dir,
                           'section_list.txt')

        glossaries = json.dumps(self.glossary_terms,
                                sort_keys=True,
                                indent='\t')
        self.write_to_file(glossaries, support_dir, 'glossary.json')

        glossary_labels = list(sorted(self.glossary_labels))
        glossary_labels_content = u''.join(glossary_labels)
        self.write_to_file(glossary_labels_content,
                           support_dir,
                           'glossary_label.txt')

        figure_labels = json.dumps(self.figure_labels,
                                   sort_keys=True,
                                   indent='\t')
        self.write_to_file(figure_labels, support_dir,
                           'figure_labels.json')

        tables = u'\n'.join(self.tables)
        self.write_to_file(tables.replace(u'\\label', u'\\ref'),
                           support_dir,
                           'table_toc.tex')
        self.write_to_file(tables.replace(u'\\label', u'\\ntiidref'),
                           support_dir,
                           'table_refs.tex')

        key_terms = process_key_terms_section(self.glossary_entry_sections)
        self.write_to_file(key_terms, support_dir, 'key_terms_toc.tex')

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
                label = sidebar.label.replace(u'\\label', u'\\ref')
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
    LATEX_PACKAGES = (
        u'graphix',
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
        title = u'\\title{%s}\n' % metadata['title']
    if 'creator' in metadata:
        author = u'\\author{%s}\n' % metadata['creator']
    package = get_packages()
    latex = get_included_tex(included_tex_list)
    return DOC_STRING % (package, title, author, latex)


def generate_glossary_term_from_sidebar(epub_body, glossary_terms, glossary_labels):
    search_sidebar_term(epub_body, glossary_terms, glossary_labels)


def search_sidebar_term(root, sidebars, labels):
    if ISidebar.providedBy(root):
        if root.type == "sidebar_term":
            sidebars[root.title] = root.base
            if root.label:
                label = root.label.replace(u'\\label', u'\\ref')
                label = u'%s\\\\\n' % (label)
                labels.append(label)
    elif hasattr(root, 'children'):
        for node in root:
            search_sidebar_term(node, sidebars, labels)
    return sidebars


def search_tables(root, tables):
    if ITable.providedBy(root):
        if root.label:
            tables.append(root.label)
    elif hasattr(root, 'children'):
        for node in root:
            search_tables(node, tables)
    return tables


def process_key_terms_section(lnodes):
    key_terms_section = {}
    # just in case there is sidebar found before section/subsection 
    # is defined in the epub
    label = u'temp'
    key_terms_section[label] = []
    for i, node in enumerate(lnodes):
        if i < len(lnodes) - 1:
            if IParagraph.providedBy(node) and ISidebar.providedBy(lnodes[i + 1]):
                label = node.label
                if label not in key_terms_section.keys():
                    key_terms_section[label] = []
        if ISidebar.providedBy(node):
            if node.title:
                key_terms_section[label].append(node.title)
                
    key_terms_toc = {}
    for key in key_terms_section:
        value = key.replace(u'\\label', u'\\ntiidref')
        for term in key_terms_section[key]:
            key_terms_toc[term] = value

    key_terms = []
    for key in sorted(key_terms_toc):
        term_link = u'%s<%s>\\\\\n' % (key_terms_toc[key], key)
        key_terms.append(term_link)

    return u''.join(key_terms)
