#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module is useful to export glossary list written in plain or docx
for example:
	in plain text the list of glossary may be written like the following:
	--------
	afterload >> force the ventricles must develop to effectively pump blood against the resistance in the vessels
	artificial >> pacemaker medical device that transmits electrical signals to the heart to ensure that it contracts and pumps blood to the body
	atrioventricular bundle >> (also, bundle of His) group of specialized myocardial conductile cells that transmit the impulse from the AV node through the interventricular septum; form the left and right atrioventricular bundle branches
	atrioventricular bundle branches >> (also, left or right bundle branches) specialized myocardial conductile cells that arise from the bifurcation of the atrioventricular bundle and pass through the interventricular septum; lead to the Purkinje fibers and also to the right papillary muscle via the moderator band
	atrioventricular (AV) node >> clump of myocardial cells located in the inferior portion of the right atrium within the atrioventricular septum; receives the impulse from the SA node, pauses, and then transmits it into specialized conducting cells within the interventricular septum
	--------
	here we can see that the glossary terms and their definition is separated using token '>>'

	the output of this program in json file will be as follows:
	--------
	{
	    "afterload ": "force the ventricles must develop to effectively pump blood against the resistance in the vessels",
	    "artificial ": "pacemaker medical device that transmits electrical signals to the heart to ensure that it contracts and pumps blood to the body",
	    "atrioventricular (AV) node ": "clump of myocardial cells located in the inferior portion of the right atrium within the atrioventricular septum; receives the impulse from the SA node, pauses, and then transmits it into specialized conducting cells within the interventricular septum",
	    "atrioventricular bundle ": "(also, bundle of His) group of specialized myocardial conductile cells that transmit the impulse from the AV node through the interventricular septum; form the left and right atrioventricular bundle branches",
	    "atrioventricular bundle branches ": "(also, left or right bundle branches) specialized myocardial conductile cells that arise from the bifurcation of the atrioventricular bundle and pass through the interventricular septum; lead to the Purkinje fibers and also to the right papillary muscle via the moderator band"
	}
	--------
	glossary in json file is needed when we run nti_glossary_finder, since it assumes we have the glossary in json file to be able to find and replace particular text with ntiglossary{'key'}{'definition'}
	run this program using nti_glossary_exporter command

.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import sys
import codecs
import logging
import argparse

from zope.exceptions import log as ze_log

from .docx.read import DocxFile
from .glossary import tex_to_json
from .glossary import txt_to_json
from .renders.LaTeX import register
register()

DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

def _parse_args():
	arg_parser = argparse.ArgumentParser( description="NTI Glossary JSON Exporter" )
	arg_parser.add_argument( 'inputfile', 
							 help="The plain text file or docx file having glossary list" )
	arg_parser.add_argument( '-o', '--output', 
							 default=None, 
							 help="Output directory")
	arg_parser.add_argument( '-dp', '--pattern', 
							 default=None, 
							 help="Use when exporting from docx. If glossary term is written as bold in docx use 'textbf', if it is italic use 'textit', if it is bold & italix use 'textbf, textit'")
	arg_parser.add_argument( '-t' '--token',
							 default=None,
							 help ="Use when exporting from plain text")
	return arg_parser.parse_args()

def _title_escape( title ):
	return title.replace(' ', '_').replace('-','_').replace(':','_')

def _configure_logging(level='INFO'):
	numeric_level = getattr(logging, level.upper(), None)
	numeric_level = logging.INFO if not isinstance(numeric_level, int) else numeric_level
	logging.basicConfig(level=numeric_level)
	logging.root.handlers[0].setFormatter(ze_log.Formatter(DEFAULT_FORMAT_STRING))

def _setup_configs():
	_configure_logging()

def set_pattern_as_list(pattern_str, delimiter):
	pattern_list = pattern_str.split(delimiter)
	for i, item in enumerate(pattern_list):
		pattern_list[i] = item.rstrip().lstrip()
	return pattern_list


def main():
	# Parse command line args
	args = _parse_args()
	_setup_configs()

	inputfile = os.path.expanduser(args.inputfile)
	# Verify the input file exists
	if not os.path.exists(inputfile):
		logger.info( 'The source file, %s, does not exist.',inputfile)
		sys.exit(-2)

	# Create the output directory if it does not exist
	if not os.path.exists( args.output ):
		os.mkdir( args.output )

	_, file_ext = os.path.splitext(os.path.basename(inputfile))
	if file_ext == u'.docx' :
		logger.info('Beginning Conversion of ' + inputfile)
		logger.info('First phase')
		#convert docx to tex
		docxFile = DocxFile( inputfile )
		tex_file = u''
		json_file = u''
		if docxFile.title:
			name = _title_escape(docxFile.title) + '.tex'
			tex_file = os.path.join(args.output, name)
			name_json = u'glossary_'+_title_escape(docxFile.title) + '.json'
			json_file = os.path.join(args.output, name_json)
		else:
			name = _title_escape(os.path.splitext(os.path.basename(inputfile))[0]) + '.tex'
			tex_file = os.path.join(args.output, name)
			name_json = u'glossary_'+_title_escape(os.path.splitext(os.path.basename(inputfile))[0]) + '.json'
			json_file = os.path.join(args.output, name_json)
		
		with codecs.open( tex_file, 'w', 'utf-8' ) as fp:
			fp.write( docxFile.render() )

		#convert tex to json
		logger.info('Second phase')
		content = tex_to_json.get_line_from_tex(tex_file)
		open_token = u'{'
		close_token = u'}'
		pattern = [u'textbf']
		if args.pattern is not None:
			pattern = set_pattern_as_list(args.pattern, ',')
			logger.info(args.pattern)
		dictionary = tex_to_json.map_key_value_tex(content, pattern, open_token, close_token)
		tex_to_json. dictionary_to_json(dictionary,json_file)
		logger.info('Conversion successful, output written to ' + json_file)

	elif file_ext == u'.txt':
		name_json = _title_escape(os.path.splitext(os.path.basename(inputfile))[0]) + '.json'
		json_file = os.path.join(args.output, name_json)
		token = args.token
		content = txt_to_json.get_content(inputfile)
		dictionary = txt_to_json.map_key_value(content, token)
		txt_to_json.dictionary_to_json(dictionary, json_file)
	else:
		logger.warn('Unhandled file type')

if __name__ == '__main__':
	main()
