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

from nti.contenttools.types.sectioning import Section
from nti.contenttools.types.sectioning import SubSection
from nti.contenttools.types.sectioning import SubSubSection
from nti.contenttools.types.sectioning import SubSubSubSection
from nti.contenttools.types.sectioning import SubSubSubSubSection

from nti.contenttools.tests import ContentToolsTestCase


class TestSectioning(ContentToolsTestCase):

    def test_section(self):
        node = Section(title='bleach', label='ichigo')
        output = render_output(node)
        assert_that(output,
                    is_(u'\\section{bleach}\n\\label{ichigo}\n'))

        node.suppressed = True
        output = render_output(node)
        assert_that(output,
                    is_(u'\\sectiontitlesuppressed{bleach}\n\\label{ichigo}\n'))

    def test_subsection(self):
        node = SubSection(title='bleach', label='ichigo')
        output = render_output(node)
        assert_that(output,
                    is_(u'\\subsection{bleach}\n\\label{ichigo}\n'))

    def test_subsubsection(self):
        node = SubSubSection(title='bleach', label='ichigo')
        output = render_output(node)
        assert_that(output,
                    is_(u'\\subsubsection{bleach}\n\\label{ichigo}\n'))

    def test_subsubsubsection(self):
        node = SubSubSubSection(title='bleach', label='ichigo')
        output = render_output(node)
        assert_that(output,
                    is_(u'\\subsubsubsection{}\n'))

    def test_subsubsubsubsection(self):
        node = SubSubSubSubSection()
        output = render_output(node)
        assert_that(output,
                    is_(u'\\subsubsubsubsection{}\n'))
