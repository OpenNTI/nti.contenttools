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

from nti.contenttools.types.document import Body
from nti.contenttools.types.document import Document

from nti.contenttools.tests import ContentToolsTestCase


class TestDocument(ContentToolsTestCase):

    def test_document(self):
        document = Document(doc_type='manga',
                            title='bleach',
                            author='kube',
                            packages=('graphicx',))
        output = render_output(document)
        assert_that(output,
                    is_(u'\\documentclass{manga}\n\\usepackage{graphicx}\n\\title{bleach}\n\\author{kube}\n'))
        
    def test_body(self):
        body = Body()
        output = render_output(body)
        assert_that(output,
                    is_(u'\\begin{document}\n\n\\end{document}\n'))
        
    def test_body_and_document(self):
        document = Document(doc_type='book',
                            packages=('graphicx',))
        document.add(Body())
        output = render_output(document)
        assert_that(output,
                    is_(u'\\documentclass{book}\n\\usepackage{graphicx}\n\\begin{document}\n\n\\end{document}\n'))
