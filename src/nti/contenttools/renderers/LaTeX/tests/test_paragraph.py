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

from nti.contenttools.types.paragraph import Paragraph

from nti.contenttools.tests import ContentToolsTestCase


class TestParagraph(ContentToolsTestCase):

    def test_document(self):
        par = Paragraph(element_type='manga')
        output = render_output(par)
        assert_that(output,
                    is_(u'\\documentclass{manga}\n'))
