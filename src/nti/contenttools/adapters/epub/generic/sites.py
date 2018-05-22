#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from z3c.baseregistry.baseregistry import BaseComponents

from zope.component import globalSiteManager as BASE

GENERIC = BaseComponents(BASE,
                         name='generic',
                         bases=(BASE,))
