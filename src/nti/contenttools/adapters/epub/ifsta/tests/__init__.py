#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

import os
import codecs

import simplejson as json

from zope.component.hooks import clearSite

from nti.contenttools.adapters.common import prepare_site

from nti.contenttools.tests import ContentToolsTestCase


class Object(object):
    css_dict = None


def create_epub_object():
    epub = Object()
    css_file = os.path.join(os.path.dirname(__file__),
                            "files", "css.json")
    with codecs.open(css_file, 'r', 'utf-8') as fp:
        epub.css_dict = json.load(fp)
    epub.chapter_num = None
    epub.term_defs = {}
    return epub


class IFSTATestCase(ContentToolsTestCase):

    def setUp(self):
        prepare_site("ifsta")

    def tearDown(self):
        clearSite()
