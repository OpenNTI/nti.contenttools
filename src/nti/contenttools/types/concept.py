#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IConceptHierarchy
from nti.contenttools.types.interfaces import IConcept

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties


@interface.implementer(IConceptHierarchy)
class ConceptHierarchy(DocumentStructureNode):
    createFieldProperties(IConceptHierarchy)


@interface.implementer(IConcept)
class Concept(DocumentStructureNode):
    createFieldProperties(IConcept)
