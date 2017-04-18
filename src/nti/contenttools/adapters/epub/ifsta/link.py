#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: link.py 110445 2017-04-10 13:34:47Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools import types

from nti.contenttools.adapters.epub.ifsta import check_child
from nti.contenttools.adapters.epub.ifsta import check_element_text
from nti.contenttools.adapters.epub.ifsta import check_element_tail

from nti.contenttools.adapters.epub.ifsta.run import Run

from nti.contenttools._compat import unicode_

class Hyperlink( types.Hyperlink ):

    def __init__(self):
        self.type = 'Normal'

    @classmethod
    def process(cls, link):
        me = cls()
        me.target = unicode_(link.attrib['href'])
        if u'class' in link.attrib : 
            if link.attrib[u'class'] == u'autogenerated-content':
                me.type = u'Pageref'
                if u'/contents/' in me.target:
                    idx = me.target.find(u'#')
                    me.target = me.target[idx:]
                if u'#' in me.target :  me.target = me.target.replace(u'#', u'')
        if link.text:
            me.add_child(types.TextNode(link.text ) )
        for child in link:
            me.add_child(Run.process(child))
        return me