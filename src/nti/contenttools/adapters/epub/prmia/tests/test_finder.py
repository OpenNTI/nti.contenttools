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

from nti.contenttools.adapters.epub.prmia.finder import search_footnote_refs
from nti.contenttools.adapters.epub.prmia.finder import search_href_node

class TestFinder(PRMIATestCase):
    def test_find_ref_node(self):
        script = u"""<div><p class="fnote"><sup><a id="ch03fn28"></a><a href="ch03.html#ch03fn_28">28</a></sup>Federal Reserve Chairman Ben S. Bernanke said &#8220;the Fed plans to avert strains in the banking system by pushing financial companies to better manage liquidity risk and reduce reliance on wholesale funding. Regulators will continue to press banks to reduce further their dependence on wholesale funding, which proved highly unreliable during the crisis.&#8221; Speech given on April 8, 2013, in Stone Mountain, Georgia.</p></div>"""
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
        script = u"""<div><p class="fnote"><sup><a id="ch03fn28"></a><a href="ch03.html#ch03fn_28">28</a></sup>Federal Reserve Chairman Ben S. Bernanke said &#8220;the Fed plans to avert strains in the banking system by pushing financial companies to better manage liquidity risk and reduce reliance on wholesale funding. Regulators will continue to press banks to reduce further their dependence on wholesale funding, which proved highly unreliable during the crisis.&#8221; Speech given on April 8, 2013, in Stone Mountain, Georgia.</p></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        parent_type = u'Fnote'
        label_dict={}
        find_label_node(node, parent_type, label_dict)
        assert_that(label_dict.keys(), has_item('Fnote'))
        assert_that(label_dict['Fnote'], is_('ch03fn28'))

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
        script = u"""<div><p class="fnote"><sup><a id="ch03fn28"></a><a href="ch03.html#ch03fn_28">28</a></sup>Federal Reserve Chairman Ben S. Bernanke said &#8220;the Fed plans to avert strains in the banking system by pushing financial companies to better manage liquidity risk and reduce reliance on wholesale funding. Regulators will continue to press banks to reduce further their dependence on wholesale funding, which proved highly unreliable during the crisis.&#8221; Speech given on April 8, 2013, in Stone Mountain, Georgia.</p></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        node_type = 'Fnote'
        label_dict = {}
        label_ref_dict = {}
        sup_nodes = {}
        find_superscript_node(node, node_type, label_dict, label_ref_dict, sup_nodes)
        assert_that(label_dict.keys(), has_item('Fnote_Superscript'))
        assert_that(label_dict['Fnote_Superscript'], is_('ch03fn28'))
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
        sup_nodes = {}
        find_superscript_node(node, node_type, label_dict, label_ref_dict, sup_nodes)
        assert_that(label_dict.keys(), has_item('Div_Superscript'))
        assert_that(label_dict['Div_Superscript'], is_('ch03fn28'))
        assert_that(label_ref_dict.keys(), has_item('ch03fn28'))
        assert_that(label_ref_dict['ch03fn28'], is_('ch03fn_28'))

    def test_find_superscript_node_footnote(self):
        script = u"""<div><p class="footnote"><sup><a id="ch03fn28"></a><a href="ch03.html#ch03fn_28">28</a></sup>This is a footnote</div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        for item in epub.footnote_ids:
            footnote_node = epub.footnote_ids[item]
            output = render_output(footnote_node)
            assert_that(output, is_(u'\\footnote{\\label{ch03fn28}This is a footnote}'))

    def test_find_search_footnote_refs(self):
        script = u"""<div><p>Hello...</p><p>This refers to footnote <sup><a id="ch03fn_28"></a><a href="ch03.html#ch03fn28">28</a></sup></p></p><p class="footnote"><sup><a id="ch03fn28"></a><a href="ch03.html#ch03fn_28">28</a></sup>This is a footnote</div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        label_dict, label_ref_dict, sup_nodes = search_footnote_refs(node, epub)
        output = render_output(node)
        assert_that(output, is_(u'Hello...\n\nThis refers to footnote \\footnote{\\label{ch03fn28}This is a footnote}\n\n'))

    def test_find_search_footnote_refs2(self):
        script = u"""<div><p>1 <sup><a id="ch03fn_40"></a><a href="ch03.html#ch03fn40">42</a></sup></p><p>2 <sup><a id="ch03fn_41"></a><a href="ch03.html#ch03fn41">41</a></sup></p><p class="footnote"><sup><a id="ch03fn40"></a><a href="ch03.html#ch03fn_40">40</a></sup>Footnote 1</p><p class="footnote"><sup><a id="ch03fn41"></a><a href="ch03.html#ch03fn_41">41</a></sup>Footnote 2</p></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        label_dict, label_ref_dict, sup_nodes = search_footnote_refs(node, epub)
        output = render_output(node)
        assert_that(output, is_(u'1 \\footnote{\\label{ch03fn40}Footnote 1}\n\n2 \\footnote{\\label{ch03fn41}Footnote 2}\n\n'))

    def test_search_href_node(self):
        script = u"""<div><p>Box <a href="ch03.html#ch03sb1">Box 3-1</a></p><div class="sidebar"><p class="side-title"><a id="ch03sb1"></a><strong>BOX 3-1 BANK REGULATION AND RISK MANAGEMENT</strong></p><p class="noindentt">Para 1</p><p class="indent">Para 2</p></div></div>"""
        element = html.fromstring(script)
        epub = create_epub_object()
        node = Run.process(element, epub=epub)
        search_href_node(node, epub)
        output = render_output(node)
        assert_that(output, is_(u'Box \\ntiidref{ch03sb1}<Box 3-1>\n\n\n\\begin{sidebar}{\\textbf{BOX 3-1 BANK REGULATION AND RISK MANAGEMENT}}\n\\label{ch03sb1}Para 1\n\nPara 2\n\n\n\\end{sidebar}\n\\\\\n'))