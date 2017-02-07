#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_property
does_not = is_not

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.renderers.interfaces import IRenderContext

from nti.contenttools.renderers.model import DefaultRendererContext

from nti.contenttools.types.document import Document 


from nti.contenttools.tests import ContentToolsTestCase


class TestDocument(ContentToolsTestCase):

    def test_render(self):
        document = Document(doc_type='manga', title='bleach', author='kube')
        