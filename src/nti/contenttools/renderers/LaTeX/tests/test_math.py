#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division

__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.types.math import Mtr
from nti.contenttools.types.math import Mtd
from nti.contenttools.types.math import Math
from nti.contenttools.types.math import MRow
from nti.contenttools.types.math import MSup
from nti.contenttools.types.math import MSub
from nti.contenttools.types.math import MFrac
from nti.contenttools.types.math import MRoot
from nti.contenttools.types.math import MOver
from nti.contenttools.types.math import Msqrt
from nti.contenttools.types.math import MText
from nti.contenttools.types.math import MUnder
from nti.contenttools.types.math import MSpace
from nti.contenttools.types.math import Mtable
from nti.contenttools.types.math import MathRun
from nti.contenttools.types.math import MFenced
from nti.contenttools.types.math import MSubSup
from nti.contenttools.types.math import MMenclose
from nti.contenttools.types.math import MUnderover
from nti.contenttools.types.math import MMprescripts
from nti.contenttools.types.math import MMultiscripts

from nti.contenttools.tests import ContentToolsTestCase

class TestMath(ContentToolsTestCase):
    def test_math(self):
        node = Math()
        output = render_output(node)
        assert_that(output, is_(u'')) 
    
    def test_mrow(self):
        node = MRow()
        output = render_output(node)
        assert_that(output, is_(u''))
    
    def test_mfenced(self):
        node = MFenced()
        output = render_output(node)
        assert_that(output, is_(u'')) 
    
    def test_math_run(self):
        node = MathRun()
        output = render_output(node)
        assert_that(output, is_(u'')) 
    