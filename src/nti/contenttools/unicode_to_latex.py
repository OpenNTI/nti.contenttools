#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
original XML at http://www.w3.org/Math/characters/unicode.xml
XSL for conversion: https://gist.github.com/798546

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

resource_filename = __import__('pkg_resources').resource_filename

import simplejson


class FrozenDict(dict):

    def __setitem__(self, key, value):
        raise NotImplementedError('Invalid operation')


_unicode_to_latex = None


def unicode_to_latex():
    global _unicode_to_latex
    if _unicode_to_latex is None:
        source = resource_filename(__name__, 'resources/unicode_to_latex.json')
        with open(source, "rU") as fp:
            _unicode_to_latex = FrozenDict(simplejson.load(fp))
    return _unicode_to_latex


def replace_unicode_with_latex_tag(text):
    # this is useful when text is a part of equation contain
    # one unicode char
    new_text = text
    if text in unicode_to_latex():
        new_text = new_text.replace(text, unicode_to_latex()[text])
    return new_text
_replace_unicode_with_latex_tag = replace_unicode_with_latex_tag


def replace_multi_char(text):
    # this is useful when text is a part of equation contain more
    # than one unicode char
    new_text = []
    token_dict = {}
    for idx, s in enumerate(text):
        new_text.append(s)
        if s not in token_dict:
            token_dict[s] = idx
            if s in unicode_to_latex():
                new_text[idx] = unicode_to_latex()[s]
    return ''.join(new_text)
_replace_multi_char = replace_multi_char
