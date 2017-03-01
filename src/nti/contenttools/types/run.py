#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IRunNode

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(IRunNode)
class Run(DocumentStructureNode):
    createFieldProperties(IRunNode)

    def __init__(self, *args, **kwargs):
        super(Run, self).__init__(*args, **kwargs)
