#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component
from zope import interface

from zope.component.hooks import getSite
from zope.component.hooks import setSite

from zope.interface.interfaces import IComponents

from zope.location.interfaces import ILocation

logger = __import__('logging').getLogger(__name__)


@interface.implementer(ILocation)
class TrivialSite(object):

    __name__ = ''
    __parent__ = None

    def __init__(self, sm):
        self.sm = sm

    def getSiteManager(self):
        return self.sm


def prepare_site(name=None):
    if name:
        site = getSite()
        campus = component.getUtility(IComponents, name=name)
        new_site = TrivialSite(campus)
        new_site.__name__ = name
        new_site.__parent__ = site
        setSite(new_site)
        return TrivialSite
