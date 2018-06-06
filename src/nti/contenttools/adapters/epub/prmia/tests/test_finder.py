#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_item 
from hamcrest import assert_that

from lxml import html

from nti.contenttools.adapters.epub.prmia.run import Run

from nti.contenttools.renderers.LaTeX.base import render_output

from nti.contenttools.adapters.epub.prmia.tests import PRMIATestCase

from nti.contenttools.adapters.epub.prmia.tests import create_epub_object

from nti.contenttools.adapters.epub.prmia.finder import find_ref_node
from nti.contenttools.adapters.epub.prmia.finder import find_label_node
from nti.contenttools.adapters.epub.prmia.finder import find_superscript_node

class TestFinder(PRMIATestCase):
    def test_find_ref_node(self):
        script = u"""<div><p class="footnote"><sup><a id="ch03fn28"></a><a href="ch03.html#ch03fn_28">28</a></sup>Federal Reserve Chairman Ben S. Bernanke said &#8220;the Fed plans to avert strains in the banking system by pushing financial companies to better manage liquidity risk and reduce reliance on wholesale funding. Regulators will continue to press banks to reduce further their dependence on wholesale funding, which proved highly unreliable during the crisis.&#8221; Speech given on April 8, 2013, in Stone Mountain, Georgia.</p></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        ref_label_node = []
        ref_label_node = find_ref_node(node, ref_label_node)
        assert_that(ref_label_node[0],is_('ch03fn_28'))

    def test_find_ref_node2(self):
        script = u"""<div><sup><a id="ch03fn28"></a><a href="ch03.html#ch03fn_28">28</a></sup></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        ref_label_node = []
        ref_label_node = find_ref_node(node, ref_label_node)
        assert_that(ref_label_node[0],is_('ch03fn_28'))

    def test_find_ref_node3(self):
        script = u"""<div><a href="ch03.html#ch03fn_28">28</a></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        ref_label_node = []
        ref_label_node = find_ref_node(node, ref_label_node)
        assert_that(ref_label_node[0],is_('ch03fn_28'))

    def test_find_label_node(self):
        script = u"""<div><p class="footnote"><sup><a id="ch03fn28"></a><a href="ch03.html#ch03fn_28">28</a></sup>Federal Reserve Chairman Ben S. Bernanke said &#8220;the Fed plans to avert strains in the banking system by pushing financial companies to better manage liquidity risk and reduce reliance on wholesale funding. Regulators will continue to press banks to reduce further their dependence on wholesale funding, which proved highly unreliable during the crisis.&#8221; Speech given on April 8, 2013, in Stone Mountain, Georgia.</p></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        parent_type = u'Footnote'
        label_dict={}
        find_label_node(node, parent_type, label_dict)
        assert_that(label_dict.keys(), has_item('Footnote'))
        assert_that(label_dict['Footnote'], is_('ch03fn28'))

    def test_find_label_node2(self):
        script = u"""<div><sup><a id="ch03fn28"></a><a href="ch03.html#ch03fn_28">28</a></sup></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        parent_type = u'Superscript'
        label_dict={}
        find_label_node(node, parent_type, label_dict)
        assert_that(label_dict.keys(), has_item('Superscript'))
        assert_that(label_dict['Superscript'], is_('ch03fn28'))

    def test_find_label_node2(self):
        script = u"""<div><a id="ch03fn28"></a></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        parent_type = u'Div'
        label_dict={}
        find_label_node(node, parent_type, label_dict)
        assert_that(label_dict.keys(), has_item('Div'))
        assert_that(label_dict['Div'], is_('ch03fn28'))

    def test_find_superscript_node(self):
        script = u"""<div><p class="footnote"><sup><a id="ch03fn28"></a><a href="ch03.html#ch03fn_28">28</a></sup>Federal Reserve Chairman Ben S. Bernanke said &#8220;the Fed plans to avert strains in the banking system by pushing financial companies to better manage liquidity risk and reduce reliance on wholesale funding. Regulators will continue to press banks to reduce further their dependence on wholesale funding, which proved highly unreliable during the crisis.&#8221; Speech given on April 8, 2013, in Stone Mountain, Georgia.</p></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        node_type = 'Footnote'
        label_dict = {}
        label_ref_dict = {}
        find_superscript_node(node, node_type, label_dict, label_ref_dict)
        assert_that(label_dict.keys(), has_item('Footnote_Superscript'))
        assert_that(label_dict['Footnote_Superscript'], is_('ch03fn28'))
        assert_that(label_ref_dict.keys(), has_item('ch03fn28'))
        assert_that(label_ref_dict['ch03fn28'], is_('ch03fn_28'))

    def test_find_superscript_node2(self):
        script = u"""<div><sup><a id="ch03fn28"></a><a href="ch03.html#ch03fn_28">28</a></sup></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        node_type = 'Div'
        label_dict = {}
        label_ref_dict = {}
        find_superscript_node(node, node_type, label_dict, label_ref_dict)
        assert_that(label_dict.keys(), has_item('Div_Superscript'))
        assert_that(label_dict['Div_Superscript'], is_('ch03fn28'))
        assert_that(label_ref_dict.keys(), has_item('ch03fn28'))
        assert_that(label_ref_dict['ch03fn28'], is_('ch03fn_28'))

