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

from nti.contenttools.types.interfaces import IDocxImage
from nti.contenttools.types.interfaces import IImage
from nti.contenttools.types.interfaces import IVideo
from nti.contenttools.types.interfaces import IFigure
from nti.contenttools.types.interfaces import IEquationImage

from nti.contenttools.types.media import Image
from nti.contenttools.types.media import DocxImage
from nti.contenttools.types.media import Video
from nti.contenttools.types.media import Figure
from nti.contenttools.types.media import EquationImage

from nti.contenttools.tests import ContentToolsTestCase


class TestMedia(ContentToolsTestCase):

    def test_image(self):
        node = Image()
        assert_that(node, validly_provides(IImage))
        assert_that(node, verifiably_provides(IImage))
        assert_that(node, has_property('path', is_(u'')))
        assert_that(node, has_property('caption', is_(u'')))
        assert_that(node, has_property('width', is_(0)))
        assert_that(node, has_property('height', is_(0)))
        assert_that(node, has_property('equation_image', is_(False)))
        assert_that(node, has_property('inline_image', is_(False)))
        assert_that(node, has_property('predefined_image_path', is_(False)))

    def test_docx_image(self):
        node = DocxImage()
        assert_that(node, validly_provides(IDocxImage))
        assert_that(node, verifiably_provides(IDocxImage))
        assert_that(node, has_property('path', is_(u'')))
        assert_that(node, has_property('caption', is_(u'')))
        assert_that(node, has_property('width', is_(0)))
        assert_that(node, has_property('height', is_(0)))
        assert_that(node, has_property('equation_image', is_(False)))
        assert_that(node, has_property('inline_image', is_(False)))
        assert_that(node, has_property('predefined_image_path', is_(False)))

    def test_video(self):
        node = Video()
        assert_that(node, validly_provides(IVideo))
        assert_that(node, verifiably_provides(IVideo))
        assert_that(node, has_property('path', is_(u'')))
        assert_that(node, has_property('caption', is_(u'')))
        assert_that(node, has_property('thumbnail', is_(u'')))
        assert_that(node, has_property('width', is_(0)))
        assert_that(node, has_property('height', is_(0)))

    def test_figure(self):
        node = Figure()
        assert_that(node, validly_provides(IFigure))
        assert_that(node, verifiably_provides(IFigure))
        assert_that(node, has_property('caption', is_(None)))
        assert_that(node, has_property('label', is_(None)))

    def test_equation_image(self):
        node = EquationImage()
        assert_that(node, validly_provides(IEquationImage))
        assert_that(node, verifiably_provides(IEquationImage))
        assert_that(node, has_property('text', is_(None)))
        assert_that(node, has_property('label', is_(None)))
        assert_that(node, has_property('image', is_(None)))
