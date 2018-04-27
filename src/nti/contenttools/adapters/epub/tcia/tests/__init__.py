#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

import os
import codecs

import simplejson as json


class Object(object):
    css_dict = None


def create_epub_object():
    epub = Object()
    css_file = os.path.join(os.path.dirname(__file__),
							"files", "css.json")
    with codecs.open(css_file, 'r', 'utf-8') as fp:
        epub.css_dict = json.load(fp)
    return epub
