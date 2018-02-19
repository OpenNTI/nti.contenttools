#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import codecs

import simplejson as json

class Object(object):
	pass

def create_epub_object():
	epub = Object()
	with codecs.open(u'src/nti/contenttools/adapters/epub/ifsta/tests/files/css.json', 'r', 'utf-8') as fp:
		epub.css_dict = json.load(fp)
	return epub