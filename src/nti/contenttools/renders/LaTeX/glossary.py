#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: glossary.py 49289 2014-09-12 17:49:09Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from IPython.core.debugger import Tracer

logger = __import__('logging').getLogger(__name__)
from .base import base_renderer
from ... import types
import os
import codecs

import simplejson as json

def glossary_renderer(self):
	result = glossary_list_renderer(self)
	trim_result = extract_list(result)
	glossary_dict = dict(trim_result)
	glossary_json = json.dumps(glossary_dict)
	logger.info("FOUND Glossary, ready to write it to %s",self.filename)
	with codecs.open(self.filename, 'w', 'utf-8' ) as fp:
		fp.write(glossary_json)
	return u'\\textbf{Glossary}'

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