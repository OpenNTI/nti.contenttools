#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.glossary import GlossaryEntry

from nti.contenttools.types.text import TextNode

from nti.contenttools.tests import ContentToolsTestCase


class TestGlossary(ContentToolsTestCase):

    def test_glossary_entry(self):
        node = GlossaryEntry()

        term = TextNode(u'term')
        definition = TextNode(u'definition')

        node.term = term
        node.definition = definition

        output = render_output(node)

        assert_that(output, is_(u'\\ntiglossaryentry{term}{definition}'))
