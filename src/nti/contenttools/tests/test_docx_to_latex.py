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
	pass

def factory(base_name):
	test_name = 'test_'+base_name
	def test(self):
		testdir = os.path.dirname(__file__)
		docx_sample_dir = os.path.join(testdir, 'docx_sample')
		tex_from_docx_dir = os.path.join(testdir, 'tex_from_docx')
		tex_sample_dir = os.path.join(testdir, 'tex_sample')

		inputfile = os.path.join(docx_sample_dir, base_name+".docx")

		docxFile = DocxFile(inputfile)
		if docxFile.title:
			outputfile = os.path.join(tex_from_docx_dir, _title_escape(docxFile.title)+'.tex')
		else:
			outputfile = os.path.join(tex_from_docx_dir, _title_escape(os.path.splitext(os.path.basename(inputfile))[0])+'.tex')

		texname = base_name+'.tex'
		testfile = os.path.join(tex_sample_dir, texname)
		assert_that(os.path.join(tex_from_docx_dir, texname),is_(outputfile))

		with open(testfile, 'r') as testfile:
			assertion_file = testfile.read()
		assert_that(docxFile.render(), assertion_file)
	return test_name, test

_INPUTS = ['equation_sample',
		   'image_sample',
		   'math_sample',
		   'math_sample2',
		   'math_sample3',
		   'numbering_sample',
		   'reference_sample',
		   'table_sample']
def build_tests(inputs):
	for testinput in inputs:
		name, test = factory(testinput)
		setattr(TestDocxToLatex, name, test)
build_tests(_INPUTS)


