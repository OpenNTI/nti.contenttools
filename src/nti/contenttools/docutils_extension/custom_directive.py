#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from docutils import nodes
from docutils.nodes import TextElement, Inline
from docutils.parsers import rst
from docutils.parsers.rst import directives, roles, languages


class bolditalic(Inline, TextElement):
    pass


class boldunderlined(Inline, TextElement):
    pass


class italicunderlined(Inline, TextElement):
    pass


class bolditalicunderlined(Inline, TextElement):
    pass


class CustomEmphasisDirective(rst.Directive):
    required_arguments = 0
    optional_arguments = 0
    has_content = True

    def run(self):
        text = '\n'.join(self.content)
        return [nodes.emphasis(self.block_text, text)]


def registerRole(name, cls):
    languages.en.roles[name] = name
    roles.register_generic_role(name, cls)


def register_custom_directive():
    registerRole('bolditalic', bolditalic)
    registerRole('boldunderlined', boldunderlined)
    registerRole('italicunderlined', italicunderlined)
    registerRole('bolditalicunderlined', bolditalicunderlined)
    directives.register_directive('custom_emphasis_directive', CustomEmphasisDirective)

register_directive = register_custom_directive
