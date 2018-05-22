#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from z3c.baseregistry.baseregistry import BaseComponents

from nti.contenttools.adapters.epub.generic.sites import GENERIC

TCIA = BaseComponents(GENERIC,
                      name='tcia',
                      bases=(GENERIC,))
