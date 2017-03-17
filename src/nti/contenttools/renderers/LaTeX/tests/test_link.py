#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.link import Hyperlink 

from nti.contenttools.types.run import Run

from nti.contenttools.types.text import TextNode

from nti.contenttools.tests import ContentToolsTestCase

class TestLink(ContentToolsTestCase):
    def test_hyperlink(self):
        node = Hyperlink()
        node.type = u'Normal'
        node.target = u'http://www.nationalgeographic.com/travel/features/best-trips-2017/'
        run = Run()
        run.add(TextNode(u'Best Trips Nature'))
        node.add(run)
        output = render_output(node)
        assert_that(output, is_(u'\\href{http://www.nationalgeographic.com/travel/features/best-trips-2017/}{Best Trips Nature}'))
        