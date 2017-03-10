#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.contenttools.types.interfaces import ICode
from nti.contenttools.types.interfaces import ICodeLine
from nti.contenttools.types.interfaces import IVerbatim

from nti.contenttools.types.code import Code
from nti.contenttools.types.code import CodeLine
from nti.contenttools.types.code import Verbatim

from nti.contenttools.tests import ContentToolsTestCase


class TestCode(ContentToolsTestCase):

    def test_code(self):
        node = Code()
        assert_that(node, validly_provides(ICode))
        assert_that(node, verifiably_provides(ICode))
    
    def test_code_line(self):
        node = CodeLine()
        assert_that(node, validly_provides(ICodeLine))
        assert_that(node, verifiably_provides(ICodeLine))
    
    def test_verbatim(self):
        node = Verbatim()
        assert_that(node, validly_provides(IVerbatim))
        assert_that(node, verifiably_provides(IVerbatim))