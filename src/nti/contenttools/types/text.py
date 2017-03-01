#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contentfragments.interfaces import PlainTextContentFragment

from nti.contentfragments.latex import PlainTextToLatexFragmentConverter

from nti.contenttools.types.interfaces import ITextNode

from nti.contenttools.types.node import NodeMixin

from nti.contenttools.unicode_to_latex import replace_multi_char
from nti.contenttools.unicode_to_latex import replace_unicode_with_latex_tag


def to_latex(text, type_text):
    # replace special unicode in TextNode with latex tag when text is
    # a part of equation (math element)
    # we use unicode_to_latex._replace_unicode_with_latex_tag(text) to
    # avoid going through large extended escape_list
    # otherwise the text replacement will take place when calling in
    # nti.contentfragments.latex.PlainTextToLatexFragmentConverter
    # and try to keep escape list for
    # nti.contentfragments.latex.PlainTextToLatexFragmentConverter small
    if type_text == 'omath':
        if text and len(text) > 1:
            text = replace_multi_char(text)
        elif text:
            text = replace_unicode_with_latex_tag(text)
    elif text:
        text = PlainTextToLatexFragmentConverter(text)
    return text


@interface.implementer(ITextNode)
class TextNode(PlainTextContentFragment, NodeMixin):

    def __new__(cls, text='', type_text=None):
        return super(TextNode, cls).__new__(cls, to_latex(text, type_text))

    def __init__(self, text='', type_text=None):
        # Note: __new__ does all the actual work, because these are immutable
        # as strings
        super(TextNode, self).__init__(self, to_latex(text, type_text))

    def add(self, child):
        pass
    add_child = add

    def remove(self, child):
        pass
    remove_child = remove
