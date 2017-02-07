#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from zope import component

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.renderers.LaTeX.base import render

from nti.contenttools.types.sectioning import Section

from nti.contenttools.tests import ContentToolsTestCase


class TestSectioning(ContentToolsTestCase):

    def test_section(self):
        section = Section(title='bleach', label='ichigo')
        renderer = component.getAdapter(section, IRenderer, name="LaTeX")
        assert_that(renderer, is_not(none()))
        output = render(section)
        assert_that(output,
                    is_(u'\\section{bleach}\n\\label{ichigo}\n'))

        section.suppressed = True
        output = render(section)
        assert_that(output,
                    is_(u'\\sectiontitlesuppressed{bleach}\n\\label{ichigo}\n'))
