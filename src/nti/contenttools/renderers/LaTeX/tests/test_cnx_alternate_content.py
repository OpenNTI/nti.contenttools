#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.cnx import CNXProblemSolution

from nti.contenttools.types.run import Run
from nti.contenttools.types.text import TextNode

from nti.contenttools.tests import ContentToolsTestCase


class TestCNXAlternateContent(ContentToolsTestCase):

    def test_cnx_problem_solution(self):
        node = CNXProblemSolution()
        node.title = TextNode(u'Title')
        run_1 = Run()
        run_1.add(TextNode(u'CNX Problem'))
        node.add(run_1)
        node.add(TextNode(u'\n'))
        run_2 = Run()
        run_2.add(TextNode(u'CNX Solution'))
        node.add(run_2)

        output = render_output(node)
        assert_that(output, 
                    is_(u'\\textbf{Title}\\\\\nCNX Problem\nCNX Solution'))
