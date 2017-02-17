#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from docutils.writers.latex2e import Writer, LaTeXTranslator
import docutils.core
import os

from nti.contenttools.docutils_extension.custom_directive import register_directive

nti_packages = {'ulem': u'\\usepackage{ulem}',
                'tabbing': u'\\usepackage{Tabbing}',
                'textgreek': u'\\usepackage{textgreek}',
                'nticourse': u'\\usepackage{nticourse}',
                'ntilatexmacros': u'\\usepackage{ntilatexmacros}',
                'ntiassessment': u'\\usepackage{ntiassessment}',
                'ntislidedeck': u'\\usepackage{ntislidedeck}',
                'ntiglossary': u'\\usepackage{ntiglossary}'}


class NTIWriter(Writer):
    default_template = 'default.tex'
    default_template_path = os.path.dirname(os.path.abspath(__file__))
    default_preamble = '\n'.join([r''])

    def __init__(self):
        register_directive()
        Writer.__init__(self)
        self.translator_class = NTILaTeXTranslator


class NTILaTeXTranslator(LaTeXTranslator):

    def __init__(self, document):
        LaTeXTranslator.__init__(self, document)
        self.head_prefix = []
        self.head = []
        self.body_prefix = []
        self.in_title = False
        for key in nti_packages.keys():
            self.requirements[key] = nti_packages.get(key)

    def visit_bolditalic(self, node):
        self.out.append(u'\\textbf{\\emph{')
        if node['classes']:
            self.visit_inline(node)

    def depart_bolditalic(self, node):
        if node['classes']:
            self.depart_inline(node)
        self.out.append('}}')

    def visit_boldunderlined(self, node):
        self.out.append(u'\\textbf{\\underline{')
        if node['classes']:
            self.visit_inline(node)

    def depart_boldunderlined(self, node):
        if node['classes']:
            self.depart_inline(node)
        self.out.append('}}')

    def visit_italicunderlined(self, node):
        self.out.append(u'\\emph{\\underline{')
        if node['classes']:
            self.visit_inline(node)

    def depart_italicunderlined(self, node):
        if node['classes']:
            self.depart_inline(node)
        self.out.append('}}')

    def visit_bolditalicunderlined(self, node):
        self.out.append(u'\\textbf{\\emph{\\underline{')
        if node['classes']:
            self.visit_inline(node)

    def depart_bolditalicunderlined(self, node):
        if node['classes']:
            self.depart_inline(node)
        self.out.append('}}}')


def generate_tex_from_rst(source):
    latex_writer = NTIWriter()
    tex = docutils.core.publish_string(source=source, writer=latex_writer, writer_name="latex")
    return tex
