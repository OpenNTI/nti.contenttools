#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import ICode
from nti.contenttools.types.interfaces import ICodeLine
from nti.contenttools.types.interfaces import IVerbatim

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(ICode)
class Code(DocumentStructureNode):
    createFieldProperties(ICode)

    def __init__(self, *args, **kwargs):
        super(Code, self).__init__(*args, **kwargs)


@interface.implementer(ICodeLine)
class CodeLine(DocumentStructureNode):
    createFieldProperties(ICodeLine)

    def __init__(self, *args, **kwargs):
        super(CodeLine, self).__init__(*args, **kwargs)


@interface.implementer(IVerbatim)
class Verbatim(DocumentStructureNode):
    createFieldProperties(IVerbatim)

    def __init__(self, *args, **kwargs):
        super(Verbatim, self).__init__(*args, **kwargs)
