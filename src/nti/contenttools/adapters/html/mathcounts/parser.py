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

from nti.contenttools.renderers.LaTeX.base import base_renderer


def adapt(fragment):
    body = fragment.find('body')
    html_body = HTMLBody.process(body)
    return html_body


class MathcountsHTMLParser(object):

    def __init__(self, script):
        self.script = script

    def process(self):
        element = html.fromstring(self.script)
        nodes = adapt(element)
        tex = base_renderer(nodes)
        return tex
