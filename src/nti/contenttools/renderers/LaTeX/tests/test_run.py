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

from nti.contenttools.types.run import Run

from nti.contenttools.tests import ContentToolsTestCase

class TestRunNode(ContentToolsTestCase):
    def test_run_bold(self):
        node = Run()
        node.styles = ['bold']
        output = render_output(node)
        assert_that(output, is_(u'\\textbf{}'))
    
    def test_run_modified(self):
        node = Run()
        node.styles = ['inserted']
        output = render_output(node)
        assert_that(output, is_(u'\\modified{}'))
    
    def test_run_italic(self):
        node = Run()
        node.styles = ['italic']
        output = render_output(node)
        assert_that(output, is_(u'\\textit{}'))