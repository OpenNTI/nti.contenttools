#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

#!/usr/bin/python

# word2lyx is a document parsing script used to
# convert Microsoft Word documents to LyX documents.
# (C) Robert Oakes, 2012. Released under the terms
# of the GNU Lesser General Public License (LGPL).
# Preferred Dependencies: lxml, elyxer

# Import xml.etree.ElementTree, to be used for parsing docx files
from xml.etree import ElementTree


class etree_element(ElementTree.Element):
    '''Extended subclass of ElementTree.Element which offers a iterchildren
            element. This makes it possible to use either lxml or xml.etree for
            parsing docx files.'''

    def iterchildren(self):
        return self.getchildren()

# Replace ElementTree.Element with etree_element, which provides
# custom methods to make it API compatible with lxml
ElementTree.Element = etree_element
