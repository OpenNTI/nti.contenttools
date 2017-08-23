#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from lxml import html

from nti.contenttools.adapters.html.mathcounts.run import HTMLBody

from nti.contenttools.renderers.LaTeX.base import render_node

from nti.contenttools.renderers.model import DefaultRendererContext

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
        element = html.fromstring(self.script)
        node = adapt(element, self)
        context = DefaultRendererContext(name="LaTeX")
        render_node(context, node)
        content = context.read()