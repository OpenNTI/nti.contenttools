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

from lxml import html

from nti.contenttools.adapters.epub.prmia.run import Run

from nti.contenttools.adapters.epub.prmia.link import Hyperlink

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.adapters.epub.prmia.tests import PRMIATestCase

from nti.contenttools.adapters.epub.prmia.tests import create_epub_object

class TestHyperlinkAdapter(PRMIATestCase):
    def test_link_id(self):
        script = u'<div><a id="ch01fig1"></a></div>'
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        assert_that(epub.ids, is_(["ch01fig1"]))

    def test_ignored_link(self):
    	script = u'<div>This is an ignored <a id="page_240"></a>link</div>'
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        output = render_output(node)
        assert_that(output, is_(u'This is an ignored link'))


        