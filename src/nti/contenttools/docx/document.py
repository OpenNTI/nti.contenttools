#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import properties as docx

from ..import types
from .body import Body


class Document(types.Document):

    @classmethod
    def process(cls, document, docxfile):
        me = cls()
        doc_main_prefix = docx.nsprefixes['w']
        body_el = '{%s}body' % (doc_main_prefix)
        # Iterate over the structure of the document, process document body
        for element in document.iterchildren():
            # Process Elements in Document Body
            if element.tag == body_el:
                me.add_child(Body.process(element, docxfile))
            else:
                logger.warn('Did not handle document element: %s' % element.tag)

        return me
