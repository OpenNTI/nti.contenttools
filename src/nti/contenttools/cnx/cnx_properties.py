#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

mdml = u'http://cnx.rice.edu/mdml'
collxml = u'http://cnx.rice.edu/collxml'

cnx_prefixes = {
    'metadata': u'{%s}metadata' % collxml,
    'content': u'{%s}content' % collxml,
    'module': u'{%s}module' % collxml,
    'subcollection': u'{%s}subcollection' % collxml,
    'repository': u'{%s}repository' % mdml,
    'content-url': u'{%s}content-url' % mdml,
    'content-id': u'{%s}content-id' % mdml,
    'title': u'{%s}title' % mdml,
    'version': u'{%s}version' % mdml,
    'created': u'{%s}created' % mdml,
    'revised': u'{%s}revised' % mdml,
    'actors': u'{%s}actors' % mdml,
    'roles': u'{%s}roles' % mdml,
    'license': u'{%s}license' % mdml,
    'subjectlist': u'{%s}subjectlist' % mdml,
    'subject': u'{%s}subject' % mdml,
    'abstract': u'{%s}abstract' % mdml,
    'language': u'{%s}language' % mdml,
    'role': u'{%s}role' % mdml,
    'person': u'{%s}person' % mdml,
    'firstname': u'{%s}firstname' % mdml,
    'surname': u'{%s}surname' % mdml,
    'fullname': u'{%s}fullname' % mdml,
    'email': u'{%s}email' % mdml,
    'keyword': u'{%s}keyword' % mdml,
    'keywordlist': u'{%s}keywordlist' % mdml,
    'organization': u'{%s}organization' % mdml,
    'shortname': u'{%s}shortname' % mdml,
    'fullname': u'{%s}fullname' % mdml,
}
