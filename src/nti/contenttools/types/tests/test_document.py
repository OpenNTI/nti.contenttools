#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property
does_not = is_not

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import IBody
from nti.contenttools.types.interfaces import IDocument
from nti.contenttools.types.interfaces import IEPUBBody
from nti.contenttools.types.interfaces import IChapterCounter

from nti.contenttools.types.document import Body
from nti.contenttools.types.document import Document
from nti.contenttools.types.document import EPUBBody
from nti.contenttools.types.document import ChapterCounter

from nti.contenttools.tests import ContentToolsTestCase


class TestDocument(ContentToolsTestCase):

    def test_document(self):
        node = Document(doc_type='manga', title='bleach', author='kube')
        assert_that(node, validly_provides(IDocument))
        assert_that(node, verifiably_provides(IDocument))
        assert_that(node, has_property('doc_type', is_('manga')))
        assert_that(node, has_property('title', is_('bleach')))
        assert_that(node, has_property('author', is_('kube')))
        assert_that(node, has_property('packages', has_length(11)))

    def test_body(self):
        node = Body()
        assert_that(node, validly_provides(IBody))
        assert_that(node, verifiably_provides(IBody))
        
    def test_epub_body(self):
        node = EPUBBody()
        assert_that(node, validly_provides(IEPUBBody))
        assert_that(node, verifiably_provides(IEPUBBody))

    def test_chapter_counter(self):
        node = ChapterCounter()
        assert_that(node, validly_provides(IChapterCounter))
        assert_that(node, verifiably_provides(IChapterCounter))
        assert_that(node, has_property('counter_number', is_(1)))
