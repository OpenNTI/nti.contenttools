#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import INaqSymmath
from nti.contenttools.types.interfaces import INaqSymmathPart
from nti.contenttools.types.interfaces import INaqSymmathPartSolution
from nti.contenttools.types.interfaces import INaqSymmathPartSolutionValue
from nti.contenttools.types.interfaces import INaqSymmathPartSolutionExplanation

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(INaqSymmath)
class NaqSymmath(DocumentStructureNode):
    createFieldProperties(INaqSymmath)


@interface.implementer(INaqSymmathPart)
class NaqSymmathPart(DocumentStructureNode):
    createFieldProperties(INaqSymmathPart)


@interface.implementer(INaqSymmathPartSolution)
class NaqSymmathPartSolution(DocumentStructureNode):
    createFieldProperties(INaqSymmathPartSolution)


@interface.implementer(INaqSymmathPartSolutionValue)
class NaqSymmathPartSolutionValue(DocumentStructureNode):
    createFieldProperties(INaqSymmathPartSolutionValue)


@interface.implementer(INaqSymmathPartSolutionExplanation)
class NaqSymmathPartSolutionExplanation(DocumentStructureNode):
    createFieldProperties(INaqSymmathPartSolutionExplanation)
