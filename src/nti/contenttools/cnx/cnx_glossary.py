#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Process glossary list found in the document

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ..glossary import glossary_check

from .. import types


def create_glossary_dictionary(cnx_glossary_list):
    """
    create glossary dictionary from the list of cnx_glossary
    """
    glossary_dict = {}
    for item in cnx_glossary_list:
        if isinstance(item, types.CNXGlossary):
            glossary_dict = process_cnx_glossary(item, glossary_dict)
    return glossary_dict


def process_cnx_glossary(cnx_glossary_node, glossary_dict):
    for child in cnx_glossary_node:
        if isinstance(child, types.GlossaryDefinition):
            term = child.term.render().strip() if child.term is not None else u''
            meaning = child.meaning.render().strip() if child.meaning is not None else u''
            if term in glossary_dict:
                if meaning != glossary_dict[term]:
                    logger.info(term)
                    logger.info('prev : %s', glossary_dict[term])
                    logger.info('current : %s', meaning)
            glossary_dict[term] = meaning
        else:
            logger.warn('Unhandled CNXGlossary child %s', child)
    return glossary_dict


def lookup_glossary_term_in_tex_file(filename, glossary_dict, search_text=None):
    glossary_check.process_glossary(glossary_dict, filename, search_text=None)


def lookup_glossary_term_in_content(content, glossary_dict, search_text=None):
    return glossary_check.run_glossary_finder(glossary_dict, content, search_text=None)
