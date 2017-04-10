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

from nti.contenttools.adapters.epub.ifsta.paragraph import Paragraph

from lxml import html

from nti.contenttools.tests import ContentToolsTestCase

class TestParagraphAdapter(ContentToolsTestCase):
    def test_simple_paragraph(self):
        script = u'<p>This is the first paragraph</p>'
        
        element = html.fromstring(script)
        node = Paragraph.process(element)
        print(node.children)
        output = render_output(node)
        
        assert_that(output,
                    is_(u'This is the first paragraph\n\n'))
    
    def test_simple_paragraph_2(self):
        script = u'<p>This is the first paragraph</p><p>This is the second paragraph</p>'
        
        element = html.fromstring(script)
        node = Paragraph.process(element)
        output = render_output(node)
        
        assert_that(output,
                    is_(u'This is the first paragraph\n\nThis is the second paragraph\n\n\n\n'))