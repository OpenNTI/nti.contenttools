#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: note.py 108980 2017-03-16 07:16:31Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IHyperlink

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(IHyperlink)
class Hyperlink(DocumentStructureNode):
    createFieldProperties(IHyperlink)