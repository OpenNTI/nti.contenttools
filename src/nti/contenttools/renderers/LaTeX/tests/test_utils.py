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

from nti.contenttools.renderers.LaTeX.utils import search_node
from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value
from nti.contenttools.renderers.LaTeX.utils import search_and_update_node_property

from nti.contenttools.types.document import Document

from nti.contenttools.types.interfaces import IItem
from nti.contenttools.types.interfaces import ISection
from nti.contenttools.types.interfaces import IDocument
from nti.contenttools.types.interfaces import IOMathRun
from nti.contenttools.types.interfaces import IOMathDPr
from nti.contenttools.types.interfaces import ITextNode
from nti.contenttools.types.interfaces import IOMathBase
from nti.contenttools.types.interfaces import IOMathFrac
from nti.contenttools.types.interfaces import IOMathMatrix
from nti.contenttools.types.interfaces import IOrderedList

from nti.contenttools.types.lists import Item
from nti.contenttools.types.lists import OrderedList

from nti.contenttools.types.media import Figure

from nti.contenttools.types.omath import OMath
from nti.contenttools.types.omath import OMathDPr
from nti.contenttools.types.omath import OMathRun
from nti.contenttools.types.omath import OMathBase
from nti.contenttools.types.omath import OMathPara
from nti.contenttools.types.omath import OMathFrac
from nti.contenttools.types.omath import OMathMatrix
from nti.contenttools.types.omath import OMathDelimiter
from nti.contenttools.types.omath import OMathNumerator
from nti.contenttools.types.omath import OMathDenominator

from nti.contenttools.types.run import Run

from nti.contenttools.types.text import TextNode

from nti.contenttools.types.sectioning import Section

from nti.contenttools.tests import ContentToolsTestCase


class TestUtils(ContentToolsTestCase):

    def test_search_node_true(self):
        root = Document()
        section_1 = Section()
        section_2 = Section()
        list_1 = OrderedList()
        item_1 = Item()
        item_2 = Item()
        list_1.add(item_1)
        list_1.add(item_2)
        section_2.add(list_1)
        root.add(section_1)
        root.add(section_2)
        result = search_node(IItem, root)
        assert_that(result, is_(True))

    def test_search_node_false(self):
        root = Document()
        section_1 = Section()
        section_2 = Section()
        list_1 = OrderedList()
        section_2.add(list_1)
        root.add(section_1)
        root.add(section_2)
        result = search_node(IItem, root)
        assert_that(result, is_(False))

    def test_search_node_2(self):
        root = Document()

        section_1 = Section()
        omath_matrix = OMathMatrix()
        run = OMathRun()
        section_1.add(omath_matrix)
        section_1.add(run)

        section_2 = Section()
        list_1 = OrderedList()
        section_2.add(list_1)

        root.add(section_1)
        root.add(section_2)

        result_doc = search_node(IDocument, root)
        assert_that(result_doc, is_(True))
        result_section = search_node(ISection, root)
        assert_that(result_section, is_(True))
        result_list = search_node(IOrderedList, root)
        assert_that(result_list, is_(True))
        result_matrix = search_node(IOMathMatrix, root)
        assert_that(result_matrix, is_(True))
        result_run = search_node(IOMathRun, root)
        assert_that(result_run, is_(True))

    def test_search_node_3(self):
        delimiter = OMathDelimiter()

        dPr = OMathDPr()
        dPr.begChr = u'['
        dPr.endChr = u']'

        e = OMathBase()
        run = OMathRun()
        run.add(TextNode(u'a+b'))
        e.add(run)

        delimiter.add(dPr)
        delimiter.add(e)

        result_dPr = search_node(IOMathDPr, delimiter)
        assert_that(result_dPr, is_(True))

        result_base = search_node(IOMathBase, delimiter)
        assert_that(result_base, is_(True))

        result_run = search_node(IOMathRun, delimiter)
        assert_that(result_run, is_(True))

        result_text = search_node(ITextNode, delimiter)
        assert_that(result_text, is_(True))

    def test_get_variant_field_string_value(self):
        node = Figure()

        node.caption = u'This is a figure caption'
        caption = get_variant_field_string_value(node.caption)
        assert_that(caption, is_(u'This is a figure caption'))

        node.title = TextNode(u'This is a figure title')
        title = get_variant_field_string_value(node.title)
        assert_that(title, is_(u'This is a figure title'))

        node.label = Run()
        child = TextNode(u'This is a figure label')
        node.label.add(child)
        label = get_variant_field_string_value(node.label)
        assert_that(label, is_(u'This is a figure label'))

    def test_search_and_update_node_property(self):
        omath = OMath()
        omath_para = OMathPara()

        numerator = OMathNumerator()
        num_child = TextNode(u'3', type_text='omath')
        numerator.add(num_child)

        denominator = OMathDenominator()
        den_child = TextNode(u'4', type_text='omath')
        denominator.add(den_child)

        frac = OMathFrac()
        frac.add(numerator)
        frac.add(denominator)

        omath_para.add(frac)
        omath.add(omath_para)

        assert_that(frac.frac_type, is_(None))

        search_and_update_node_property(IOMathFrac, 
                                        omath, 
                                        {'frac_type': 'lin'})
        assert_that(frac.frac_type, is_(u'lin'))

        search_and_update_node_property(IOMathFrac,
                                        omath,
                                        {'frac_type': 'skw'})
        assert_that(frac.frac_type, is_(u'skw'))

        search_and_update_node_property(IOMathFrac, 
                                        omath, 
                                        {'frac_type': 'noBar'})
        assert_that(frac.frac_type, is_(u'noBar'))
