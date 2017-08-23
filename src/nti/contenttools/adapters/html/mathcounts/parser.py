#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml import html

from os.path import basename

from nti.contenttools.adapters.html.mathcounts.run import HTMLBody

from nti.contenttools.renderers.LaTeX.base import render_node

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.util.string_replacer import rename_filename


def adapt(fragment, html):
    body = fragment.find('body')
    html_body = HTMLBody.process(body, html)
    return html_body


class MathcountsHTMLParser(object):

    def __init__(self, script, output_dir, tex_filename=None):
        self.script = script
        self.output_dir = output_dir
        self.naq_counter = 0
        self.tex_filename = tex_filename

    def process(self):
        self.cleanup_filename()
        element = html.fromstring(self.script)
        node = adapt(element, self)
        context = DefaultRendererContext(name="LaTeX")
        render_node(context, node)
        _ = context.read()

    def cleanup_filename(self):
        self.tex_filename = rename_filename(self.tex_filename)
        if '.tex' in self.tex_filename:
            self.labelling = basename(self.tex_filename)
        else:
            self.labelling = self.tex_filename
            self.tex_filename = '%s.tex' % self.tex_filename
