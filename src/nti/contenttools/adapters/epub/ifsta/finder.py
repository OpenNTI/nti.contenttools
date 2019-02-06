#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re
import copy

from nti.contenttools.renderers.LaTeX.base import render_output
from nti.contenttools.renderers.LaTeX.base import render_children_output

from nti.contenttools.renderers.LaTeX.utils import create_label
from nti.contenttools.renderers.LaTeX.utils import get_variant_field_string_value
from nti.contenttools.renderers.LaTeX.utils import search_run_node_and_remove_styles

from nti.contenttools.types import Run
from nti.contenttools.types import Item
from nti.contenttools.types import Sidebar
from nti.contenttools.types import TextNode
from nti.contenttools.types import UnorderedList

from nti.contenttools.types.interfaces import ICell
from nti.contenttools.types.interfaces import IImage
from nti.contenttools.types.interfaces import ITable
from nti.contenttools.types.interfaces import IFigure
from nti.contenttools.types.interfaces import IRunNode
from nti.contenttools.types.interfaces import ISidebar
from nti.contenttools.types.interfaces import IParagraph
from nti.contenttools.types.interfaces import IGlossaryEntry
from nti.contenttools.types.interfaces import IDocumentStructureNode


def search_sidebar_info(root, nodes):
    if ISidebar.providedBy(root):
        if root.type == u"sidebar_term":
            pass
        else:
            nodes.append(root)
    elif hasattr(root, u'children'):
        for child in root.children:
            if IFigure.providedBy(child):
                if child.floating == True and child.icon == True:
                    nodes.append(child)
            else:
                search_sidebar_info(child, nodes)
    return nodes


def add_icon_to_sidebar_info(nodes):
    figures = get_particular_nodes(nodes, IFigure)
    sidebars = get_particular_nodes(nodes, ISidebar)
    if len(figures) == len(sidebars):
        for i, sidebar in enumerate(sidebars):
            sidebar.children.insert(0, figures[i])
    else:
        logger.warn("The number of sidebar and figure icon is different")
    return figures


def remove_extra_figure_icon(root, figure):
    if figure == root:
        if hasattr(root, u'__parent__'):
            parent = root.__parent__
            children = []
            if not ISidebar.providedBy(parent):
                for child in parent.children:
                    if not IFigure.providedBy(child):
                        children.append(child)
                parent.children = children
    elif hasattr(root, u'children'):
        for node in root:
            remove_extra_figure_icon(node, figure)


def get_particular_nodes(nodes, ntype):
    snodes = []
    for node in nodes:
        if ntype.providedBy(node):
            snodes.append(node)
    return snodes


def process_paragraph_captions(captions):
    rendered_captions = {}
    for token, caption in captions.items():
        output = render_output(caption)
        rendered_captions[token] = output.strip()
    return rendered_captions


def search_and_update_figure_caption(root, captions):
    if IFigure.providedBy(root):
        old_cap = root.caption
        if old_cap in captions.keys():
            root.caption = captions[old_cap]
        else:
            logger.warn("PARAGRAPH CAPTION NOT FOUND for %s", old_cap)
    elif hasattr(root, u'children'):
        for node in root:
            search_and_update_figure_caption(node, captions)


def remove_paragraph_caption_from_epub_body(root):
    if IParagraph.providedBy(root):
        if hasattr(root, u'__parent__') and root.element_type == u'caption':
            parent = root.__parent__
            children = []
            for child in parent.children:
                if not child.element_type == u'caption':
                    children.append(child)
            parent.children = children
    elif hasattr(root, u'children'):
        for node in root:
            remove_paragraph_caption_from_epub_body(node)


def search_sidebar_head_and_body(root, nodes):
    if ISidebar.providedBy(root):
        if root.type == u'sidebar-head':
            nodes.append(root)
    elif hasattr(root, u'children'):
        for child in root.children:
            if IParagraph.providedBy(child):
                if child.element_type == u"sidebars-body":
                    nodes.append(child)
            else:
                search_sidebar_head_and_body(child, nodes)


def process_sidebar_head_and_body(nodes):
    sidebars = []
    sidebar = None
    for child in nodes:
        if ISidebar.providedBy(child):
            sidebar = child
            sidebars.append(sidebar)
        else:
            parent = child.__parent__
            if sidebar:
                parent.children.remove(child)
                sidebar.add(child)
            else:
                sidebar = Sidebar()
                for i, node in enumerate(parent):
                    if child == node:
                        parent.remove(child)
                        sidebar.add(child)
                        parent.children.insert(i, sidebar)
                sidebars.append(sidebar)
    return sidebars


def search_sidebar_terms(root, sidebars, sidebar_nodes, chapter_num=None, glossary_entry_sections=None):
    if IParagraph.providedBy(root):
        if any(style in root.styles for style in ('Section', 'Subsection',)):
            glossary_entry_sections.append(root)
    elif ISidebar.providedBy(root):
        if root.type == u"sidebar_term":
            node = copy.deepcopy(root)
            search_run_node_and_remove_styles(node)
            base = render_children_output(node)
            str_pos = base.find('---')
            if str_pos > -1:
                term = base[0:str_pos].strip()
                sidebars[term] = render_children_output(root)
                term = re.sub(r'[{}]', '', term)
                term = term.strip()
                root.title = term
                if chapter_num:
                    term = '%s_%s' % (term, chapter_num)
                label = create_label('sidebar_term',
                                     term.replace(u'textbf', u'').replace(u'textit', u''))
                root.label = label
            sidebar_nodes.append(root)
            glossary_entry_sections.append(root)

            # we don't want to include the sidebar term in the generated tex
            rparent = root.__parent__
            rparent.remove(root)
    elif hasattr(root, u'children'):
        for child in root:
            search_sidebar_terms(child, sidebars, sidebar_nodes, chapter_num, glossary_entry_sections)


def search_and_update_glossary_entries(root, sidebars, term_defs):
    if IGlossaryEntry.providedBy(root):
        node = copy.deepcopy(root.term)
        search_run_node_and_remove_styles(node)
        term = render_output(node).strip()
        term_lower = term.lower()
        term_capital = term.title()
        terms = (term, term_capital,)
        for word in terms:
            if word in sidebars.keys():
                root.definition = sidebars[word]
                root.key_term = unicode(word)

        if not root.definition:
            for key in term_defs.keys():
                if key in term_lower or term_lower in key:
                    root.definition = term_defs[key]
                    root.key_term = unicode(key)
        if not root.definition:
            logger.warning('Glossary definition is empty')
            logger.warning(term)
    elif hasattr(root, u'children'):
        for child in root:
            search_and_update_glossary_entries(child, sidebars, term_defs)


def update_caption_list(captions):
    new_captions = []
    for caption in captions:
        new_captions.append(render_output(caption))
    return new_captions


def search_and_update_figure_caption_reflowable(root, captions, figures, figure_ref):
    if IFigure.providedBy(root):
        if root.data_type == u'ifsta-numbering-fig':
            old_cap = root.caption
            caps = [cap for cap in captions if old_cap in cap]
            if caps:
                new_cap = caps[0]
                token = u'Figure %s' % (old_cap)
                new_cap = new_cap.replace(token.rstrip(), u'')
                root.caption = new_cap.rstrip()
                figures.append(root)
                label = get_variant_field_string_value(root.label)
                ref = u'\\ntiidref{%s}' % label
                figure_ref[token.rstrip()] = ref
            else:
                root.caption = u'Undefined Caption'
                figures.append(root)
                logger.warn('CAPTION NOT FOUND >> %s', old_cap)
    if hasattr(root, u'children'):
        for node in root:
            search_and_update_figure_caption_reflowable(
                node, captions, figures, figure_ref)


def search_paragraph_section(root, sections, chapter=None):
    if IParagraph.providedBy(root):
        if chapter and root.label:
            if IDocumentStructureNode.providedBy(root.label):
                root.label.add(TextNode(chapter))
            elif isinstance(root.label, (str, unicode)):
                root.label = u'%s%s' % (label, chapter)
        if 'Section' in root.styles:
            ref = get_section_label_ref(root, 'section')
            sections.append(ref)
        elif 'Subsection' in root.styles:
            ref = get_section_label_ref(root, 'subsection')
            sections.append(u'\\begin{quote}\n')
            sections.append(ref)
            sections.append(u'\\end{quote}\n')
    if hasattr(root, u'children'):
        for node in root:
            search_paragraph_section(node, sections, chapter)


def get_section_label_ref(root, section_type):
    label = create_label(section_type, root.label)
    root.label = label
    ref = label.replace(u'\\label', u'\\ref')
    ref = u'%s\\\\\n' % (ref)
    return ref


def process_sidebar_figure_info_rf(sfnodes):
    for i, node in enumerate(sfnodes):
        if i < len(sfnodes) - 1:
            if IFigure.providedBy(node) and ISidebar.providedBy(sfnodes[i + 1]):
                sfnodes[i + 1].children.insert(0, node)
                parent = node.__parent__
                parent.remove(node)


def search_table(root, tables):
    if ITable.providedBy(root):
        tables.append(root)
    if hasattr(root, u'children'):
        for node in root:
            search_table(node, tables)


def cleanup_table_element(tables):
    for node in tables or ():
        search_and_update_table_element(node)
        node.border = True


def search_and_update_table_element(root):
    if IParagraph.providedBy(root):
        el = Run()
        el.children = root.children
        parent = root.__parent__
        for i, child in enumerate(parent):
            if child == root:
                parent.remove(child)
                parent.children.insert(i, el)

    if ICell.providedBy(root):
        root.children.insert(0, TextNode(u'\n\n'))
    if IImage.providedBy(root):
        el = Run()
        parent = root.__parent__
        for i, child in enumerate(parent):
            if child == root:
                el.add(root)
                parent.remove(child)
                el.add(TextNode(u'\n\\newline\n'))
                parent.children.insert(i, el)
    if hasattr(root, u'children'):
        for node in root:
            search_and_update_table_element(node)


def search_thead_element(root, cells):
    if ICell.providedBy(root):
        el = Run()
        el.children = root.children
        cells.append(el)
    elif hasattr(root, u'children'):
        for node in root:
            search_thead_element(node, cells)


def search_figure_icon_on_sidebar_title(tnode, figs):
    if IFigure.providedBy(tnode):
        figs.append(tnode)
        parent = tnode.__parent__
        parent.remove(tnode)
    elif hasattr(tnode, u'children'):
        for child in tnode:
            search_figure_icon_on_sidebar_title(child, figs)
    return figs


def search_figure_icon_on_sidebar_body(tnode, figs):
    if IFigure.providedBy(tnode):
        if tnode.icon:
            figs.append(tnode)
    elif hasattr(tnode, u'children'):
        for child in tnode:
            search_figure_icon_on_sidebar_body(child, figs)
    return figs


def update_sidebar_body_bullet(node):
    if IRunNode.providedBy(node) and node.element_type == 'bullet':
        bullet_class = UnorderedList()
        new_item = Item()
        new_item.children = node.children
        bullet_class.children = [new_item]
        parent = node.__parent__
        idx = parent.children.index(node)
        parent.remove(node)
        parent.children.insert(idx, bullet_class)
    elif hasattr(node, 'children'):
        for child in node:
            update_sidebar_body_bullet(child)


def search_span_note(node, notes):
    if IRunNode.providedBy(node):
        if node.element_type == 'span-note':
            notes.append(node)
    elif hasattr(node, u'children'):
        for child in node:
            search_span_note(child, notes)
    return notes


def search_glossary_section(root, glossary_entry_sections=()):
    if IParagraph.providedBy(root):
        if any(style in root.styles for style in ('Section', 'Subsection',)):
            glossary_entry_sections.append(root)
    elif IGlossaryEntry.providedBy(root):
        glossary_entry_sections.append(root)

    if hasattr(root, u'children'):
        for child in root:
            search_glossary_section(child, glossary_entry_sections)
