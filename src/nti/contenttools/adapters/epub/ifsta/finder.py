#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: finder.py 113572 2017-05-25 09:09:52Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.contenttools.types.interfaces import IFigure
from nti.contenttools.types.interfaces import ISidebar
from nti.contenttools.types.interfaces import ITextNode
from nti.contenttools.types.interfaces import IParagraph
from nti.contenttools.types.interfaces import IGlossaryEntry

from nti.contenttools.renderers.LaTeX.base import render_output
from nti.contenttools.renderers.LaTeX.base import render_children_output
from nti.contenttools.renderers.LaTeX.utils import search_run_node_and_remove_styles


def search_sidebar_info(root, nodes):
    if ISidebar.providedBy(root):
        if root.type == u"sidebar_term":
            pass
        else:
            nodes.append(root)
    if ITextNode.providedBy(root):
        pass
    elif root.children is not None:
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
    if ITextNode.providedBy(root):
        pass
    elif root.children is not None:
        for child in root.children:
            if IParagraph.providedBy(child):
                if child.element_type == u"sidebars-body":
                    nodes.append(child)
            else:
                search_sidebar_head_and_body(child, nodes)


def process_sidebar_head_and_body(nodes):
    for child in nodes:
        if ISidebar.providedBy(child):
            sidebar = child
        else:
            parent = child.__parent__
            parent.children.remove(child)
            sidebar.add(child)


def search_sidebar_terms(root, sidebars, sidebar_nodes):
    if ISidebar.providedBy(root):
        if root.type == u"sidebar_term":
            search_run_node_and_remove_styles(root)
            base = render_children_output(root)
            str_pos = base.find('-')
            if str_pos > -1:
                term = base[0:str_pos].strip()
                sidebars[term] = base
            sidebar_nodes.append(root)
            parent = root.__parent__
            parent.children.remove(root)

    elif hasattr(root, u'children'):
        for node in root:
            search_sidebar_terms(node, sidebars, sidebar_nodes)


def search_and_update_glossary_entries(root, sidebars):
    if IGlossaryEntry.providedBy(root):
        search_run_node_and_remove_styles(root.term)
        term = render_output(root.term).strip()
        term_lower = term.lower()
        term_capital = term.title()
        terms = (term, term_lower, term_capital,)
        for word in terms:
            if word in sidebars.keys():
                logger.info(term)
                logger.info(word)
                root.definition = sidebars[word]
    elif hasattr(root, u'children'):
        for node in root:
            search_and_update_glossary_entries(node, sidebars)


def update_caption_list(captions):
    new_captions = []
    for caption in captions:
        new_captions.append(render_output(caption))
    return new_captions


def search_and_update_figure_caption_reflowable(root, captions, figures):
    if IFigure.providedBy(root):
        if root.data_type == u'ifsta-numbering-fig':
            old_cap = root.caption
            caps = [cap for cap in captions if old_cap in cap]
            if caps:
                new_cap = caps[0]
                token = u'Figure %s ' % (old_cap)
                new_cap = new_cap.replace(token, u'')
                root.caption = new_cap.rstrip()
                figures.append(root)
                parent = root.__parent__
                parent.children.remove(root)
            else:
                logger.warn('CAPTION NOT FOUND >> %s', old_cap)
    if hasattr(root, u'children'):
        for node in root:
            search_and_update_figure_caption_reflowable(node, captions, figures)