#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that

from zope import component

from nti.contenttools.docx.read import DocxFile
from nti.contenttools.word2latex import _title_escape
from nti.contenttools.tests import ContentToolsTestCase

import os
import codecs

class TestDocxToLatex(ContentToolsTestCase):
	def test_on_reference(self):
		inputfile = "src/nti/contenttools/tests/docx_sample/reference_sample.docx"
		outputdir = 'src/nti/contenttools/tests/tex_from_docx/'
		if not os.path.exists( outputdir ):
			os.mkdir( outputdir )		
		docxFile = DocxFile(inputfile)
		if docxFile.title:
			outputfile = os.path.join(outputdir, _title_escape(docxFile.title)+'.tex')
		else:
			outputfile = os.path.join(outputdir, _title_escape(os.path.splitext(os.path.basename(inputfile))[0])+'.tex')

		testfile = 'src/nti/contenttools/tests/tex_sample/reference_sample.tex'
		assert_that('src/nti/contenttools/tests/tex_from_docx/reference_sample.tex',is_(outputfile))

		with codecs.open( outputfile, 'w', 'utf-8' ) as fp:
			fp.write( docxFile.render() )
		
		latex_file = open(testfile, 'r')
		result_file = open(outputfile, 'r')

		assert_that(latex_file.read(), is_(result_file.read()))

		def test_on_numbering(self):
		inputfile = "src/nti/contenttools/tests/docx_sample/numbering_sample.docx"
		outputdir = 'src/nti/contenttools/tests/tex_from_docx/'
		if not os.path.exists( outputdir ):
			os.mkdir( outputdir )		
		docxFile = DocxFile(inputfile)
		if docxFile.title:
			outputfile = os.path.join(outputdir, _title_escape(docxFile.title)+'.tex')
		else:
			outputfile = os.path.join(outputdir, _title_escape(os.path.splitext(os.path.basename(inputfile))[0])+'.tex')

		testfile = 'src/nti/contenttools/tests/tex_sample/numbering_sample.tex'
		assert_that('src/nti/contenttools/tests/tex_from_docx/numbering_sample.tex',is_(outputfile))

		with codecs.open( outputfile, 'w', 'utf-8' ) as fp:
			fp.write( docxFile.render() )
		
		latex_file = open(testfile, 'r')
		result_file = open(outputfile, 'r')

		assert_that(latex_file.read(), is_(result_file.read()))