#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_property
does_not = is_not

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import IParagraph

from nti.contenttools.types.interfaces import ICNXCollection
from nti.contenttools.types.interfaces import ICNXSubcollection
from nti.contenttools.types.interfaces import ICNXContent
from nti.contenttools.types.interfaces import ICNXModule
from nti.contenttools.types.interfaces import ICNXHTMLBody
from nti.contenttools.types.interfaces import ICNXGlossary
from nti.contenttools.types.interfaces import ICNXProblemSolution

from nti.contenttools.types.cnx import CNXCollection
from nti.contenttools.types.cnx import CNXSubcollection
from nti.contenttools.types.cnx import CNXContent
from nti.contenttools.types.cnx import CNXModule
from nti.contenttools.types.cnx import CNXHTMLBody
from nti.contenttools.types.cnx import CNXGlossary
from nti.contenttools.types.cnx import CNXProblemSolution

from nti.contenttools.tests import ContentToolsTestCase


class TestCNX(ContentToolsTestCase):

    def test_cnx_collection(self):
        node = CNXCollection()
        assert_that(node, validly_provides(ICNXCollection))
        assert_that(node, verifiably_provides(ICNXCollection))

    def test_cnx_subcollection(self):
        node = CNXSubcollection()
        assert_that(node, validly_provides(ICNXSubcollection))
        assert_that(node, verifiably_provides(ICNXSubcollection))

    def test_cnx_content(self):
        node = CNXContent()
        assert_that(node, validly_provides(ICNXContent))
        assert_that(node, verifiably_provides(ICNXContent))

    def test_cnx_module(self):
        node = CNXModule()
        assert_that(node, validly_provides(ICNXModule))
        assert_that(node, verifiably_provides(ICNXModule))

    def test_cnx_html_body(self):
        node = CNXHTMLBody()
        assert_that(node, validly_provides(ICNXHTMLBody))
        assert_that(node, verifiably_provides(ICNXHTMLBody))

    def test_cnx_glossary(self):
        node = CNXGlossary()
        assert_that(node, validly_provides(ICNXGlossary))
        assert_that(node, verifiably_provides(ICNXGlossary))

    def test_cnx_problem_solution(self):
        node = CNXProblemSolution()
        assert_that(node, validly_provides(ICNXProblemSolution))
        assert_that(node, verifiably_provides(ICNXProblemSolution))
