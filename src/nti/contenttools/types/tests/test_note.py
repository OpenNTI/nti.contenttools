#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property
does_not = is_not

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import INote
from nti.contenttools.types.interfaces import INoteInteractive
from nti.contenttools.types.interfaces import INoteInteractiveImage

from nti.contenttools.types.note import Note
from nti.contenttools.types.note import NoteInteractive
from nti.contenttools.types.note import NoteInteractiveImage

from nti.contenttools.tests import ContentToolsTestCase


class TestNote(ContentToolsTestCase):

    def test_note(self):
        node = Note()
        assert_that(node, validly_provides(INote))
        assert_that(node, verifiably_provides(INote))

    def test_note_interactive(self):
        node = NoteInteractive()
        assert_that(node, validly_provides(INoteInteractive))
        assert_that(node, verifiably_provides(INoteInteractive))

    def test_note_interactive_image(self):
        node = NoteInteractiveImage()
        assert_that(node, validly_provides(INoteInteractiveImage))
        assert_that(node, verifiably_provides(INoteInteractiveImage))
