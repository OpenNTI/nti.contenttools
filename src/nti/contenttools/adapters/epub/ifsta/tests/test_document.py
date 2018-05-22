#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from lxml import html

from zope import component

from nti.contenttools.adapters.epub.ifsta import EPUBBody

from nti.contenttools.adapters.epub.ifsta.tests import IFSTATestCase

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.types.interfaces import IEPUBBody


class TestDocumentAdapter(IFSTATestCase):

    def test_simple_epub_body(self):
        script = u'<div><p>This is the first paragraph</p></div>'
        element = html.fromstring(script)

        node = EPUBBody.process(element)

        assert_that(node, validly_provides(IEPUBBody))
        assert_that(node, verifiably_provides(IEPUBBody))

        renderer = component.getAdapter(node,
                                        IRenderer,
                                        name=u'LaTeX')
        context = DefaultRendererContext(name=u"LaTeX")
        renderer.render(context, node)

        output = render_output(node)
        assert_that(output,
                    is_(u'This is the first paragraph\n\n'))

        assert_that(output, is_(context.read()))
