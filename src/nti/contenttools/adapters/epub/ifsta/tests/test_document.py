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

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import IEPUBBody

from nti.contenttools.adapters.epub.ifsta.paragraph import Paragraph

from nti.contenttools.adapters.epub.ifsta import EPUBBody

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.tests import ContentToolsTestCase

class TestDocumentAdapter(ContentToolsTestCase):

    def test_simple_epub_body(self):
        script = u'<div><p>This is the first paragraph</p></div>'
        element = html.fromstring(script)

        node = EPUBBody.process(element)
        assert_that(node, validly_provides(IEPUBBody))
        assert_that(node, verifiably_provides(IEPUBBody))

        output = render_output(node)
        assert_that(output,
                    is_(u'This is the first paragraph\n\n'))


