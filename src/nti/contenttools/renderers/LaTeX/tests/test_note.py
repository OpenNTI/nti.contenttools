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
from nti.contenttools.types.note import NoteInteractive
from nti.contenttools.types.note import OpenstaxNote
from nti.contenttools.types.note import OpenstaxNoteBody
from nti.contenttools.types.note import OpenstaxExampleNote

from nti.contenttools.types.run import Run

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

    def test_note_interactive(self):
        node = NoteInteractive()
        output = render_output(node)
        assert_that(
            output,
            is_(u'\n\\begin{nticard}{}\n\\label{}\n\\caption{}\n\\includegraphics{images/}\n\n\\end{nticard}\n'))

    def test_openstax_note(self):
        node = OpenstaxNote()
        node.body = OpenstaxNoteBody()
        output = render_output(node)
        assert_that(output, is_(u'\n\\begin{sidebar}{}\n\n\\end{sidebar}\n'))

    def test_openstax_note_with_title(self):
        node = OpenstaxNote()
        node.body = OpenstaxNoteBody()
        node.title = "Title"
        node.label = Run()
        output = render_output(node)
        assert_that(output, is_(u'\n\\begin{sidebar}{Title}\n\n\\end{sidebar}\n'))

    def test_openstax_note_with_label_and_title(self):
        node = OpenstaxNote()
        node.body = OpenstaxNoteBody()
        node.title = "Title"
        node.label = "Label001"
        output = render_output(node)
        assert_that(
            output,
            is_(u'\n\\begin{sidebar}{Title}\n\\label{Label001}\n\\end{sidebar}\n'))

    def test_openstax_example_note(self):
        node = OpenstaxExampleNote()
        node.body = OpenstaxNoteBody()
        output = render_output(node)
        assert_that(output, is_(u'\n\\begin{sidebar}{}\n\n\\end{sidebar}\n'))

    def test_openstax_note_body(self):
        node = OpenstaxNoteBody()
        child_1 = Run()
        child_2 = Run()
        child_3 = Run()
        node.add(child_1)
        node.add(child_2)
        node.add(child_3)
        output = render_output(node)
        assert_that(output, is_(u''))
