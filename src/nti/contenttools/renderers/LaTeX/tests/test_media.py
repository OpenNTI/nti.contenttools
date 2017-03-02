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
    
    def test_simple_figure(self):
        figure = Figure()
        output = render_output(figure)
        assert_that(output, is_(u'\\begin{figure}\n\\begin{center}\n\n\\end{center}\n\\end{figure}\n'))
    
    def test_figure_with_title(self):
        figure = Figure()
        figure.title= TextNode(u'This is a figure title')
        output = render_output(figure)
        assert_that(output, is_(u'\\begin{figure}\n\\begin{center}\n\\textbf{This is a figure title}\\\\\n\n\\end{center}\n\\end{figure}\n'))
    
    def test_figure_with_caption(self):
        figure = Figure()
        figure.caption = u'This is figure caption'
        output = render_output(figure)
        assert_that(output, is_(u'\\begin{figure}\n\\begin{center}\n\\caption{This is figure caption}\n\n\\end{center}\n\\end{figure}\n'))
    
    def test_figure_with_label(self):
        figure = Figure()
        figure.label = Run()
        child = TextNode(u'fig_label')
        figure.label.add(child)
        output = render_output(figure)
        assert_that(output, is_(u'\\begin{figure}\n\\begin{center}\n\\label{fig_label}\n\\end{center}\n\\end{figure}\n'))
    
    def test_figure_with_image(self):
        figure = Figure()
        img = Image()
        img.width = 500
        img.height = 450
        img.predefined_image_path = True
        img.path = u'images/foo.png'
        figure.add(img)
        output = render_output(figure)
        assert_that(output, is_(u'\\begin{figure}\n\\begin{center}\n\\ntiincludeannotationgraphics[width=500px,height=450px]{images/foo.png}\n\\end{center}\n\\end{figure}\n'))
    
    def test_figure(self):
        figure = Figure()
        figure.title= u'fig title'
        figure.caption = u'fig caption'
        figure.label = u'fig_label'
        img = Image()
        img.width = 70
        img.height = 90
        img.predefined_image_path = True
        img.path = u'images/foo.png'
        figure.add(img)
        output = render_output(figure)
        assert_that(output, is_(u'\\begin{figure}\n\\begin{center}\n\\textbf{fig title}\\\\\n\\ntiincludeannotationgraphics[width=70px,height=90px]{images/foo.png}\\caption{fig caption}\n\\label{fig_label}\n\\end{center}\n\\end{figure}\n'))
        