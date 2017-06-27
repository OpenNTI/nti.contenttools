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
from nti.contenttools.types.document import EPUBBody
from nti.contenttools.types.document import ChapterCounter

from nti.contenttools.types.sectioning import Section

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

    def test_body_with_children(self):
        body = Body()
        section_1 = Section(title='Adventure', label='adventure101')
        section_2 = Section(title='Climate', label='climate101')
        body.add(section_1)
        body.add(section_2)
        output = render_output(body)
        assert_that(output,
                    is_(u'\\begin{document}\n\section{Adventure}\n\label{adventure101}\n\section{Climate}\n\label{climate101}\n\n\\end{document}\n'))

    def test_epub_body(self):
        body = EPUBBody()
        output = render_output(body)
        assert_that(output,
                    is_(u''))

    def test_body_and_document(self):
        document = Document(doc_type='book',
                            packages=('graphicx',))
        document.add(Body())
        output = render_output(document)
        assert_that(output,
                    is_(u'\\documentclass{book}\n\\usepackage{graphicx}\n\\begin{document}\n\n\\end{document}\n'))

    
    def test_chapter_counter(self):
        node = ChapterCounter()
        output = render_output(node)
        assert_that(output,
                    is_(u'\\setcounter{figure}{0}\n\\setcounter{table}{0}\n\\setcounter{chapter}{1}\n\\setcounter{section}{0}\n\n\\renewcommand*{\\thefigure}{1.\\arabic{figure}}\n\\renewcommand*{\\thetable}{1.\\arabic{table}}\n'))