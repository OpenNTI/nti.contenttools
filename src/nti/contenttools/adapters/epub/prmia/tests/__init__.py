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

from nti.contenttools.tests import ContentToolsTestCase

from nti.contenttools.adapters.common import prepare_site

class Object(object):
    css_dict = None


def create_epub_object():
    epub = Object()
    epub.ids = []
    epub.book_title = 'PRMIATest'
    epub.input_file = None
    epub.label_refs = {}
    epub.footnote_ids = {}
    return epub


class PRMIATestCase(ContentToolsTestCase):

    def setUp(self):
        prepare_site("prmia")

    def tearDown(self):
        clearSite()