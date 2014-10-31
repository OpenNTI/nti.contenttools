#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest

from lxml import html

from nti.contenttools.renders.LaTeX import register
from nti.contenttools.epub.adapters.note import OpenstaxNote

register()

class TestNote(unittest.TestCase):
	
	def test_openstax_note(self):
		html_script = u'<div id="m42092-fs-id3166459" class="note">\
		<div class="title">\
		<span class="cnx-gentext-tip-t">Models, Theories, and Laws</span>\
		</div>\
		<div class="body">\
		<p><span id="m42092-import-auto-id2590130"></span>Models, theories, and laws\
		are used to help scientists analyze the data they have already collected.\
		However, often after a model, theory, or law has been developed, it points\
		scientists toward new discoveries they would not otherwise have made.</p>\
		</div>\
		</div>'
		render_check = u'\n\\begin{sidebar}{Models, Theories, and Laws}\label{m42092-fs-id3166459}\nModels, theories, and laws are used to help scientists analyze the data they have already collected. However, often after a model, theory, or law has been developed, it points scientists toward new discoveries they would not otherwise have made.\n\\end{sidebar}\\newline\n'

		element = html.fromstring(html_script)
		el = OpenstaxNote.process(element, None)
		result = el.render()
		self.assertEqual(result, render_check) 





