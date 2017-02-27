#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.note import Note
from nti.contenttools.types.lists import UnorderedList

from nti.contenttools.tests import ContentToolsTestCase

class TestNote(ContentToolsTestCase):
    def test_note(self):
        node = Note()
        output = render_output(node)
        assert_that(output, is_(u''))
    
    def test_footnote(self):
        node = Note()
        child = UnorderedList()
        node.add(child)
        output = render_output(node)
        assert_that(output, is_(u'\\footnote{\\begin{itemize}\n\n\\end{itemize}\n'))