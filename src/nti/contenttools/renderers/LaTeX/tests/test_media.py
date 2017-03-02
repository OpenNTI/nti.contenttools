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

from nti.contenttools.types.media import Image
from nti.contenttools.types.media import Figure

from nti.contenttools.types.run import Run
from nti.contenttools.types.text import TextNode

from nti.contenttools.tests import ContentToolsTestCase

class TestMedia(ContentToolsTestCase):
    def test_empty_image(self):
        node = Image()
        output = render_output(node)
        assert_that(output, is_(u'\\includegraphics[width=0px,height=0px]{images/}'))
    
    def test_annotation_image(self):
        node = Image()
        node.width = 500
        node.height = 450
        node.predefined_image_path = True
        node.path = u'images/foo.png'
        output = render_output(node)
        assert_that(output, is_('\\ntiincludeannotationgraphics[width=500px,height=450px]{images/foo.png}'))
    
    def test_noannotation_image(self):
        node = Image()
        node.annotation = False
        node.width = 500
        node.height = 450
        node.predefined_image_path = True
        node.path = u'images/foo.png'
        output = render_output(node)
        assert_that(output, is_(u'\\ntiincludenoannotationgraphics[width=500px,height=450px]{images/foo.png}'))
    
    def test_inline_image(self):
        node = Image()
        node.inline_image = True
        node.width = 30
        node.height = 40
        node.predefined_image_path = True
        node.path = u'images/foo.png'
        output = render_output(node)
        assert_that(output, is_(u'\\includegraphics[width=30px,height=40px]{images/foo.png}'))
    
    def test_equation_image(self):
        node = Image()
        node.equation_image = True
        node.width = 30
        node.height = 40
        node.predefined_image_path = True
        node.path = u'images/foo.png'
        output = render_output(node)
        assert_that(output, is_(u'\\includegraphics[width=30px,height=40px]{images/foo.png}'))
    
    def test_figure(self):
        figure = Figure()
        output = render_output(figure)
        assert_that(output, is_(u'\\includegraphics[width=0px,height=0px]{images/}'))
        