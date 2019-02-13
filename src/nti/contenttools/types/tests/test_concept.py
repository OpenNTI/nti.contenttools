#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import assert_that

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import IConceptHierarchy
from nti.contenttools.types.interfaces import IConcept

from nti.contenttools.types.concept import ConceptHierarchy
from nti.contenttools.types.concept import Concept

from nti.contenttools.tests import ContentToolsTestCase


class TestConcept(ContentToolsTestCase):

    def test_concept_hierarchy(self):
        node = ConceptHierarchy()
        assert_that(node, validly_provides(IConceptHierarchy))
        assert_that(node, verifiably_provides(IConceptHierarchy))

    def test_concept(self):
        node = Concept()
        assert_that(node, validly_provides(IConcept))
        assert_that(node, verifiably_provides(IConcept))
