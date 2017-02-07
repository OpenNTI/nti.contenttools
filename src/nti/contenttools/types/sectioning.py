#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttools.types.interfaces import IChapter
from nti.contenttools.types.interfaces import ISection
from nti.contenttools.types.interfaces import ISubSection
from nti.contenttools.types.interfaces import ISubSubSection
from nti.contenttools.types.interfaces import ISubSubSubSection
from nti.contenttools.types.interfaces import ISubSubSubSubSection

from nti.contenttools.types.node import DocumentStructureNode

from nti.schema.fieldproperty import createFieldProperties


class TitleLabelMixin(object):

    def set_title(self, title):
        self.title = title

    def set_label(self, label):
        self.label = label


@interface.implementer(IChapter)
class Chapter(DocumentStructureNode, TitleLabelMixin):
    createFieldProperties(IChapter)


@interface.implementer(ISection)
class Section(DocumentStructureNode, TitleLabelMixin):
    createFieldProperties(ISection)


@interface.implementer(ISubSection)
class SubSection(Section):
    createFieldProperties(ISubSection)


@interface.implementer(ISubSubSection)
class SubSubSection(Section):
    createFieldProperties(ISubSubSection)


@interface.implementer(ISubSubSubSection)
class SubSubSubSection(Section):
    createFieldProperties(ISubSubSubSection)


@interface.implementer(ISubSubSubSubSection)
class SubSubSubSubSection(Section):
    createFieldProperties(ISubSubSubSubSection)
