#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division

__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import codecs

from lxml import html

from os.path import splitext

from nti.contenttools.adapters.html.mathcounts.run import HTMLBody

from nti.contenttools.renderers.LaTeX.base import render_node

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.util.string_replacer import rename_filename


def adapt(fragment, html):
    body = fragment.find('body')
    logger.info(body)
    html_body = HTMLBody.process(body, html)
    return html_body


class MathcountsHTMLParser(object):

    def __init__(self, script, output_dir, tex_filename):
        self.script = script
        self.output_dir = output_dir
        self.naq_counter = 0
        self.image_counter = 0
        self.tex_filename = tex_filename

    def process(self):
        self.cleanup_filename()
        element = html.fromstring(self.script)
        node = adapt(element, self)
        logger.info(node.children)
        self.context = DefaultRendererContext(name=u'LaTeX')
        render_node(self.context, node)

    def cleanup_filename(self):
        self.tex_filename = rename_filename(self.tex_filename)
        if '.tex' in self.tex_filename:
            self.labelling, _ = splitext(self.tex_filename)
        else:
            self.labelling = self.tex_filename
            self.tex_filename = '%s.tex' % self.tex_filename

    def write_to_file(self):
        filepath = '%s/%s' % (self.output_dir, self.tex_filename)
        with codecs.open(filepath, 'w', 'utf-8') as fp:
            fp.write(self.context.read())
