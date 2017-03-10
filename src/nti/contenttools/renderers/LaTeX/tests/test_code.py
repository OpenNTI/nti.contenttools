#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

from nti.contenttools.renderers.LaTeX.base import render_output

# from nti.contenttools.types.code import Code
from nti.contenttools.types.code import CodeLine
from nti.contenttools.types.code import Verbatim

from nti.contenttools.types.run import Run
from nti.contenttools.types.text import TextNode

from nti.contenttools.tests import ContentToolsTestCase


class TestCode(ContentToolsTestCase):

    def test_code_line(self):
        node = CodeLine()
        run = Run()
        run.add(TextNode(u'temp = 0'))
        node.add(run)
        output = render_output(node)
        assert_that(output, is_(u'\\texttt{temp = 0}'))

    def test_verbatim(self):
        node = Verbatim()
        run = Run()
        run.add(TextNode(u'a = 2\nb=3'))
        node.add(run)
        output = render_output(node)
        # TODO : there is a problem here
        # the text 'a = 2' should not be rendered to '$a = 2$'
        # the text in verbatim environment should not be rendered using content
        # fragment
        assert_that(output, 
                    is_(u'\\begin{verbatim}\na = 2\nb=3\n\\end{verbatim}\n'))
