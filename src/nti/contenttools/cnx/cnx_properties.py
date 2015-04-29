#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: cnx_properties.py 62939 2015-04-10 23:28:10Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)


collxml 	= u'http://cnx.rice.edu/collxml'
mdml 		= u'http://cnx.rice.edu/mdml'

cnx_prefixes = {
	'metadata'		: u'{%s}metadata' %collxml,
    'content'		: u'{%s}content' %collxml,
    'module'		: u'{%s}module' %collxml,
    'subcollection' : u'{%s}subcollection' %collxml,
    'repository'	: u'{%s}repository' %mdml,
    'content-url'	: u'{%s}content-url' %mdml,
    'content-id'	: u'{%s}content-id' %mdml,
    'title'			: u'{%s}title' %mdml,
    'version'		: u'{%s}version' %mdml,
    'created'		: u'{%s}created' %mdml,
    'revised'		: u'{%s}revised' %mdml,
    'actors'		: u'{%s}actors' %mdml,
    'roles'			: u'{%s}roles' %mdml,
    'license'		: u'{%s}license' %mdml,
    'subjectlist'	: u'{%s}subjectlist' %mdml,
    'abstract'		: u'{%s}abstract' %mdml,
    'language'		: u'{%s}language' %mdml,
}

