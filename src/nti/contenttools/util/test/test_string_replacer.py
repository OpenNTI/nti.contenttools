#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

import unittest
from nti.contenttools.util import string_replacer


class TestStringReplacer(unittest.TestCase):
	def test_percentage(self):
		text = u'http://kompas.com/travel%toraja%home'
		old_char = u'%'
		new_char = u'\\%'
		new_text = u'http://kompas.com/travel\\%toraja\\%home'
		result = string_replacer.modify_string(text, old_char, new_char)
		self.assertEqual(new_text,result)

		text = u'http://topics.nytimes.com/top/reference/timestopics/organizations/o/occupy_wall_street/index.html?scp=1-spot&sq=occupy\\%20wall%20street&st=cse'
		new_text = u'http://topics.nytimes.com/top/reference/timestopics/organizations/o/occupy_wall_street/index.html?scp=1-spot&sq=occupy\\%20wall\\%20street&st=cse'
		result = string_replacer.modify_string(text, old_char, new_char)
		self.assertEqual(new_text,result)

		text = u'http://topics.nytimes.com/top/reference/timestopics/organizations/o/occupy_wall_street/index.html?scp=1-spot&sq=occupy\\%20wall\\%20street&st=cse'
		new_text = u'http://topics.nytimes.com/top/reference/timestopics/organizations/o/occupy_wall_street/index.html?scp=1-spot&sq=occupy\\%20wall\\%20street&st=cse'
		result = string_replacer.modify_string(text, old_char, new_char)

		text = u'\href{http://edu.learnsoc.org/Chapters/3\\%20theories\%20of\\%20sociology/11\%20modernization\\%20theory.htm'
		new_text = u'\href{http://edu.learnsoc.org/Chapters/3\\%20theories\\%20of\\%20sociology/11\\%20modernization\\%20theory.htm'
		result = string_replacer.modify_string(text, old_char, new_char)
		self.assertEqual(new_text,result)
