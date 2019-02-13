#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.concept import ConceptHierarchy
from nti.contenttools.types.concept import Concept

from nti.contenttools.types.run import Run

from nti.contenttools.types.text import TextNode

from nti.contenttools.tests import ContentToolsTestCase


class TestConcept(ContentToolsTestCase):

    def test_concept_hierarchy(self):
        node = ConceptHierarchy()
        output = render_output(node)
        assert_that(output, is_(u'\\begin{concepthierarchy}\n\n\\end{concepthierarchy}\n'))

    def test_concept(self):
        node = Concept(name=u'NFPA 1720')
        output = render_output(node)
        assert_that(output, is_(u'\\begin{concept}<NFPA 1720>\n\\label{concept:NFPA_1720}\n\\end{concept}\n'))

    def test_concepts_1(self):
        node = ConceptHierarchy()
        concept_1 = Concept(name=u'NFPA 1720')
        concept_2 = Concept(name=u'NFPA 1002')
        node.add_child(concept_1)
        node.add_child(concept_2)
        output = render_output(node)
        assert_that(output, is_(u'\\begin{concepthierarchy}\n\\begin{concept}<NFPA 1720>\n\\label{concept:NFPA_1720}\n\\end{concept}\n\\begin{concept}<NFPA 1002>\n\\label{concept:NFPA_1002}\n\\end{concept}\n\n\\end{concepthierarchy}\n'))

    def test_concepts_2(self):
        node = ConceptHierarchy()
        concept_1 = Concept(name=u'NFPA 1720')
        concept_1_1 = Concept(name=u'NFPA 1720 - 1')
        concept_1_2 = Concept(name=u'NFPA 1720 - 2')
        concept_1.add_child(concept_1_1)
        concept_1.add_child(concept_1_2)
        concept_2 = Concept(name=u'NFPA 1002')
        node.add_child(concept_1)
        node.add_child(concept_2)
        output = render_output(node)
        assert_that(output, is_(u'\\begin{concepthierarchy}\n\\begin{concept}<NFPA 1720>\n\\label{concept:NFPA_1720}\\begin{concept}<NFPA 1720 - 1>\n\\label{concept:NFPA_1720___1}\n\\end{concept}\n\\begin{concept}<NFPA 1720 - 2>\n\\label{concept:NFPA_1720___2}\n\\end{concept}\n\n\\end{concept}\n\\begin{concept}<NFPA 1002>\n\\label{concept:NFPA_1002}\n\\end{concept}\n\n\\end{concepthierarchy}\n'))
