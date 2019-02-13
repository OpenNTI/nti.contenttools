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

from nti.contenttools.adapters.epub.prmia import adapt as adapt_prmia

from nti.contenttools.adapters.epub.prmia.finder import search_href_node as search_href_node_prmia
from nti.contenttools.adapters.epub.prmia.finder import cleanup_label_node as cleanup_label_node_prmia
from nti.contenttools.adapters.epub.prmia.finder import search_sections_of_real_page_number as search_sections_of_real_page_number_prmia

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.renderers.LaTeX.base import render_node
from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.script.cleanup_tex_file import cleanup_subsubsection

from nti.contenttools.util.string_replacer import rename_filename

from nti.contenttools.types.interfaces import IParagraph
from nti.contenttools.types.interfaces import ISidebar
from nti.contenttools.types.interfaces import ITable
from nti.contenttools.types.interfaces import IEPUBBody
from nti.contenttools.types.interfaces import IGlossaryEntry

EPUB_COURSE_TYPE = (u'ifsta', u'ifsta_rf', u'tcia', u'prmia')
EPUB_REMOVE_PAGE_NUMBER = (u'ifsta', u'ifsta_rf')
EPUB_REPLACE_STAR_WITH_ITEM = (u'ifsta', u'ifsta_rf')

logger = __import__('logging').getLogger(__name__)


class EPUBParser(object):

    def __init__(self, input_file, output_directory, epub_type, css_json=None, chapter_num=None, para_term=None):
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
        self.term_defs = {}

        self.tables = []
        self.chapter_num = chapter_num

        self.ids = []

        self.labels = {}  # id - id type
        self.footnote_ids = {}  # footnote id - content
        self.last_footnote_id = u''
        self.label_refs = {}  # id - id to ref

        self.page_numbers = {}  # page_number - section id

        self.para_term = para_term

        self.epub_reader = EPUBReader(input_file)
        self.epub_chapters = {}
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
                    self.epub_chapters[item] = epub_chapter
                elif self.epub_type == 'tcia':
                    epub_chapter = adapt_tcia(fragment, self)
                    self.epub_chapters[item] = epub_chapter
                elif self.epub_type == 'prmia':
                    epub_chapter = adapt_prmia(fragment, self)
                    search_sections_of_real_page_number_prmia(epub_chapter, [], self.page_numbers)
                    self.epub_chapters[item] = epub_chapter
        self.write_chapter_to_tex_file()
        self.create_main_latex()
        logger.info(epub_reader.spine)
        self.process_support_files()

    def write_chapter_to_tex_file(self):
        for item in self.epub_chapters.keys():
            epub_chapter = self.epub_chapters[item]
            if self.epub_type == 'prmia':
                search_href_node_prmia(epub_chapter, self)
                cleanup_label_node_prmia(epub_chapter, self)
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
                else:
                    self.write_to_file(content,
                                       self.output_directory,
                                       tex_filename)
            self.tables = search_tables(epub_chapter, self.tables)

    def cleanup_tex(self, content):
        if self.epub_type in EPUB_REMOVE_PAGE_NUMBER:
            content = re.sub(r'(, p\.).[0-9]*[0-9]', u'', content)

        if self.epub_type in EPUB_REPLACE_STAR_WITH_ITEM:
            content = content.replace(u"*", u"\\item ")
            content = content.replace(u"\\renewcommand\\item ", u"\\renewcommand*")
            content = content.replace(u'\\item --- ', u'\\\\ --- ')

        content = content.replace(u"\\item *", u"\\item ")

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

        # remove unnecessary \newline
        content = content.replace(u'\\newline None', u'')

        # add css-class to sidebar
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

        if self.chapter_num == 'Index':
            content = content.replace(u'\\end{quote}\n\\begin{quote}', u'')

        content = content.replace(u'\\begin{center}\n\item \item \item \n\\end{center}', u'\\begin{center}\n *** \n\\end{center}\n')
        content = content.replace(u'\\end{itemize}\n}', u'\\end{itemize}}')

        content = content.replace(u'\\item \\textbf{\\item }', u'\\item ')
        content = content.replace(u'\\item \\item', u'\\item ')
        content = content.replace(u'\\textbf{\\item }', u'\\item ')
        content = content.replace(u'\\textbf{\\item}', u'\\item ')

        content = content.replace(u'\\newline\\\\', u'\\\\')
        content = content.replace(u'[css-class=note]{CAUTION:}', u'[css-class=caution]{CAUTION:}')
        content = content.replace(u'[css-class=note]{WARNING:}', u'[css-class=warning]{WARNING:}')

        content = content.replace(u' }', u'} ')
        content = content.replace(u'} {', u'}{')
        content = content.replace(u'\\end{figure}\n\\\\', u'\\end{figure}\\\\')
        return content

    def process_support_files(self):
        support_dir = u'%s/SupportFiles' % self.output_directory
        if not os.path.exists(support_dir):
            os.makedirs(support_dir)

        content_fig = self.generate_figure_tex()
        self.write_to_file(content_fig,
                           support_dir,
                           'Figures.tex')

        content_sidebar_term = self.generate_terms_tex()
        self.write_to_file(content_sidebar_term,
                           support_dir,
                           'Terms.tex')

        content = u''.join(self.section_list)
        content = self.cleanup_extra_quote(content)
        self.write_to_file(content,
                           support_dir,
                           'section_list.txt')

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

        key_terms_section = process_key_terms_section(self.glossary_entry_sections)
        key_terms_toc = build_key_terms_toc(key_terms_section)
        key_terms = create_terms_toc_string(key_terms_toc)
        self.write_to_file(key_terms, support_dir, 'key_terms_toc.tex')

        gterms = synchronize_key_terms(key_terms_section, self.term_defs.keys())
        glossaries = json.dumps(gterms,
                                sort_keys=True,
                                indent='\t')
        if self.chapter_num:
            glossary_index = 'glossary_{}.json'.format(self.chapter_num)
        else:
            glossary_index = 'glossary.json'
        self.write_to_file(glossaries, support_dir, glossary_index)

    def cleanup_extra_quote(self, content):
        content = content.replace(u'\\end{quote}\n\\begin{quote}\n', u'')
        content = content.replace(u'\\\\\n\\begin{quote}', u'\n\\begin{quote}')
        content = content.replace(u'\\\\\n\\end{quote}', u'\n\\end{quote}')
        return content

    def generate_figure_tex(self):
        figures = []
        for fig in self.figure_node:
            figures.append(render_output(fig))
        content = u'\n'.join(figures)
        return content

    def generate_terms_tex(self):
        if self.sidebar_term_nodes:
            sidebars = []
            for sidebar in self.sidebar_term_nodes:
                sidebars.append(render_output(sidebar))
                self.glossary_terms[sidebar.title] = sidebar.base
                if sidebar.label:
                    label = sidebar.label.replace(u'\\label', u'\\ref')
                    label = u'%s\\\\\n' % (label)
                    self.glossary_labels.append(label)
            return u'\n'.join(sidebars)
        else:
            clist = []
            for term in sorted(self.term_defs):
                clist.append(u'{}'.format(self.term_defs[term]))
            return u'\n\n'.join(clist)

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
            if IParagraph.providedBy(node) and \
                    (ISidebar.providedBy(lnodes[i + 1]) or IGlossaryEntry.providedBy(lnodes[i + 1])):
                label = node.label
                if label not in key_terms_section:
                    key_terms_section[label] = []
        if ISidebar.providedBy(node):
            if node.title:
                key_terms_section[label].append(node.title)
        elif IGlossaryEntry.providedBy(node):
            if node.key_term:
                key_terms_section[label].append(node.key_term)
            else:
                key_terms_section[label].append(render_output(node.term))
    return key_terms_section


def build_key_terms_toc(key_terms_section):
    key_terms_toc = {}
    for key in key_terms_section:
        value = key.replace(u'\\label', u'\\ntiidref')
        for term in key_terms_section[key]:
            key_terms_toc[term] = value
    return key_terms_toc


def create_terms_toc_string(key_terms_toc):
    key_terms = []
    for key in sorted(key_terms_toc):
        term_link = u'%s<%s>\\\\\n' % (key_terms_toc[key], key)
        key_terms.append(term_link)
    return u''.join(key_terms)


def synchronize_key_terms(key_terms_section, term_defs):
    key_terms = {}
    for key in key_terms_section:
        value = key.replace(u'\\label', u'\\ntiidref')
        for term in key_terms_section[key]:
            for td in term_defs:
                if td.lower() in term.lower() or term.lower() in td.lower():
                    key_terms[td] = value
    for td in term_defs:
        if td not in key_terms:
            key_terms[td] = 'NOT FOUND'
    return key_terms
