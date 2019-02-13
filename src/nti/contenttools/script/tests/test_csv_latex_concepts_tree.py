#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

import os

from hamcrest import is_
from hamcrest import assert_that

from nti.contenttools.script.csv_latex_concepts_tree import read_csv
from nti.contenttools.script.csv_latex_concepts_tree import build_concepts_tree

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.tests import ContentToolsTestCase


class TestCSVLaTeXConceptsTree(ContentToolsTestCase):
    def data_file(self, name):
        return os.path.join(os.path.dirname(__file__), 'data', name)

    def test_csv_to_latex(self):
        names = read_csv(self.data_file('ConceptTrees.csv'), 'Concepts')
        ctree = build_concepts_tree(names)
        tex_tree = render_output(ctree)
        assert_that(tex_tree, u'\\begin{concepthierarchy}\n\\begin{concept}<NFPA 1072>\n\\label{concept:NFPA_1072}\n\\end{concept}\n\\begin{concept}<NFPA 472>\n\\label{concept:NFPA_472}\n\\end{concept}\n\n\\end{concepthierarchy}\n')
