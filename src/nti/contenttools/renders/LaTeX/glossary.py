#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from IPython.core.debugger import Tracer

logger = __import__('logging').getLogger(__name__)
from .base import base_renderer


def glossary_renderer(self):
	result = glossary_list_renderer(self)
	trim_result = extract_list(result)
	logger.info('found glossary')
	glossary_dict = dict(trim_result)
	self.set_glossary_dict(glossary_dict)
	return u''


def glossary_list_renderer(self):
	result = glossary_item_renderer(self)
	return result

def glossary_item_renderer(self):	
	result = []
	for child in self:
		result.append(child.render())
	return result
    
def glossary_dt_renderer(self):
	result = []
	for child in self.desc:
	    result.append(child.render())
	desc =  u''.join(result)
	item = base_renderer(self)
	return item, desc

def glossary_dd_renderer(self):
    return base_renderer(self)


def extract_list(list_of_list):
	for child in list_of_list:
		if isinstance(child[0],list):
			return extract_list(child)
		else:
			return child

def glossary_term_renderer(self):
	item = base_renderer(self)
	return u'\\ntiglossaryentry{\\textbf{%s}}{definition} ' % (item)