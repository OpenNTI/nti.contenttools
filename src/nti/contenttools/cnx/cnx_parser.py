#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parse each index.cnxml.html found in each module to latex format

.. $Id: cnx_parser.py 58552 2015-01-29 23:10:30Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import codecs
import simplejson as json

from lxml import html

from ..util import rename_filename

from ..renders.LaTeX.base import base_renderer

from .. import scoped_registry

from .xml_reader import CNX_XML

from .adapters.run_adapter import adapt

from . import cnx_glossary


class CNXParser(object):

    def __init__(self, input_file, output_directory):
        cnx_xml = CNX_XML()
        self.collection = cnx_xml.read_xml(input_file)
        self.image_list = []
        self.latex_filenames = []
        self.content_folder = []  # will be use to retrieve images or pdf
        self.latex_main_files = u''

        head, _ = os.path.split(input_file)
        self.cnx_directory = head
        self.output_directory = output_directory
        scoped_registry.output_directory = output_directory
        self.tex_filepath = []

    def process_collection(self):
        collection = self.collection
        self.metadata = collection.metadata

        if u'title' in self.metadata:
            title = rename_filename(self.metadata[u'title'])
            self.latex_main_files = u'MAIN_%s.tex' % title
            scoped_registry.book_title = title

        content = collection.content
        if content.modules:
            self.process_modules(content.modules,
                                 type_=u'collection')

        subcollections = content.subcollections
        if subcollections:
            for subcollection in subcollections:
                self.process_subcollection(subcollection)

        self.create_main_latex()

    def process_modules(self, modules, type_=None, latex_filename=None):
        result = []
        result_append = result.append
        for module in modules:
            if type_ == u'collection':
                scoped_registry.cnx_glossary = []
                doc_content = self.process_document(module.document)
                tex_filename = u'%s.tex' % rename_filename(module.title)
                self.latex_filenames.append(tex_filename)
                doc_content = self.process_glossary(doc_content)
                attribution = self.get_attribution()
                if attribution is not None:
                    doc_content = u'%s\n\n%s' % (doc_content, attribution)
                self.write_to_file(doc_content, tex_filename)
            elif type_ == u'subcollection':
                doc_content = self.process_document(module.document)
                result_append(doc_content)
        if type_ == u'subcollection':
            return u''.join(result)

    def process_document(self, document_folder):
        logger.info(u'________________________________________')
        logger.info(u'Process document %s', document_folder)
        tex_content = u''
        if len(self.cnx_directory) == 0:
            folder = u'%s' % (document_folder)
        else:
            folder = u'%s/%s' % (self.cnx_directory, document_folder)
        scoped_registry.current_dir = folder
        self.content_folder.append(folder)
        cnxml_html_file = u'%s/index.cnxml.html' % (folder)
        logger.info(cnxml_html_file)
        if os.path.exists(cnxml_html_file):
            with codecs.open(cnxml_html_file, 'r', 'utf-8') as file_:
                doc_fragment = html.fromstring(file_.read())
            cnx_html_body = adapt(doc_fragment, self)
            tex_content = base_renderer(cnx_html_body)
        attribution = self.get_attribution()
        if attribution is not None:
            tex_content = u'%s\n\n%s' % (tex_content, attribution)
        logger.info(u'________________________________________')
        return u'%s\n\n' % tex_content

    def process_subcollection(self, subcollection):
        scoped_registry.cnx_glossary = []
        tex_filename = u'%s.tex' % rename_filename(subcollection.title)
        self.latex_filenames.append(tex_filename)

        content = subcollection.content
        if content.modules:
            subcollection_content = self.process_modules(content.modules,
                                                         type_=u'subcollection',
                                                         latex_filename=tex_filename)
            subcollection_content = self.process_glossary(subcollection_content)
            chapter = u'\\chaptertitlesuppressed{%s}\n' % (subcollection.title)
            subcollection_content = u'%s\n%s' % (chapter, subcollection_content)
            self.write_to_file(subcollection_content, tex_filename)

    def write_to_file(self, content, filename, type_=None):
        if type_ is None:
            filepath = u'%s/%s' % (self.output_directory, filename)
            self.tex_filepath.append(filepath)
            with codecs.open(filepath, 'w', 'utf-8') as file_:
                file_.write(content)

    def create_main_latex(self):
        main_tex_content = generate_main_tex_content(self.metadata, self.latex_filenames)
        self.write_to_file(main_tex_content, self.latex_main_files)

    def process_glossary_(self):
        latex_files = self.tex_filepath
        glossary_dict = cnx_glossary.create_glossary_dictionary(
            scoped_registry.cnx_glossary)
        json_file = u'%s/glossary.json' % (self.output_directory)
        self.dictionary_to_json(glossary_dict, json_file)
        for file_ in latex_files:
            cnx_glossary.lookup_glossary_term_in_tex_file(file_,
                                                          glossary_dict,
                                                          search_text=None)

    def process_glossary(self, content):
        glossary_dict = cnx_glossary.create_glossary_dictionary(
            scoped_registry.cnx_glossary)
        return cnx_glossary.lookup_glossary_term_in_content(content,
                                                            glossary_dict,
                                                            search_text=None)

    def dictionary_to_json(self, dictionary, json_file):
        """
        save dictionary to json file
        """
        dict_json = json.dumps(dictionary, sort_keys=True, indent=4 * ' ')
        with codecs.open(json_file, 'w', 'utf-8') as fp:
            fp.write(dict_json)

    def get_attribution(self):
        if u'content-url' in self.metadata:
            atthref = self.metadata[u'content-url']
            attribution = u'\\subsection{Attribution}\n\\textbf{Original book can be downloaded at \\href{%s}{%s}}' % (
                atthref, atthref)
            return attribution


def get_packages():
    LATEX_PACKAGES = [
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
    ]
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


def generate_main_tex_content(metadata, included_tex_list):
    title = u'\\title{%s}\n' % metadata[u'title'] if 'title' in metadata else u''
    author = get_book_authors(metadata)
    author = u'\\author{%s}\n' % author if author is not None else u''
    package = get_packages()
    latex = get_included_tex(included_tex_list)
    return u'\\documentclass{book}\n%s%s%s\\begin{document}\n%s\\end{document}' % (
        package, title, author, latex)


def get_book_authors(metadata):
    if u'actors' in metadata:
        actors = metadata[u'actors']
        if u'person' in actors:
            person = actors[u'person']
            if u'fullname' in person:
                return person[u'fullname']


def main():
    cnx_parser = CNXParser(u'collection.xml')
    cnx_parser.process_collection()
    logger.info(cnx_parser.latex_main_files)
    logger.info(cnx_parser.latex_filenames)
    logger.info(cnx_parser.content_folder)

if __name__ == '__main__':
    main()
