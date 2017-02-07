#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from zope import component

from nti.contenttools.renderers.interfaces import IRenderer

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.types.document import Document

from nti.contenttools.tests import ContentToolsTestCase


class TestDocument(ContentToolsTestCase):

    def test_render(self):
        context = DefaultRendererContext()
        document = Document(doc_type='manga',
                            title='bleach',
                            author='kube',
                            packages=('graphicx',))
        renderer = component.getAdapter(document, IRenderer, name="LaTeX")
        assert_that(renderer, is_not(none()))
        renderer.render(context)
        output = context.read()
        assert_that(output,
                    is_(u'\\documentclass{manga}\n\\usepackage{graphicx}\n\\title{bleach}\n\\author{kube}\n'))
