#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import codecs
import logging
import argparse
import simplejson as json

import __builtin__

from zope.exceptions import log as ze_log

from .glossary import glossary_check
from .epub.openstax_epub import EPUBFile
from .util import string_replacer


DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

def _parse_args():
	arg_parser = argparse.ArgumentParser( description="NTI EPUB Converter" )
	arg_parser.add_argument( 'inputfile', 
							 help="The EPUB file" )
	arg_parser.add_argument( '-o', '--output', 
							 default='output',
							 help="The output directory. The default is: %s" % 'output' )
	arg_parser.add_argument( '-a', '--attribution', 
							 default=None, 
							 help="Attribution text")
	arg_parser.add_argument( '-ah', '--atthref',
							 default=None,
							 help="Attribution link")
	arg_parser.add_argument( '-i', '--indexatt', 
							 default=1,
							 help="File index to start writing attribution")
	arg_parser.add_argument( '-s', '--skipspine',
							 default=None,
							 help="Epub spine id")
	return arg_parser.parse_args()

def _title_escape( title ):
	return title.replace(' ', '_').replace('-','_').replace(':','_')

def _configure_logging(level='INFO'):
	numeric_level = getattr(logging, level.upper(), None)
	numeric_level = logging.INFO if not isinstance(numeric_level, int) else numeric_level
	logging.basicConfig(level=numeric_level)
	logging.root.handlers[0].setFormatter(ze_log.Formatter(DEFAULT_FORMAT_STRING))

def _setup_configs():
	# logging
	_configure_logging()
	
def main():
	# Parse command line args
	args = _parse_args()

	_setup_configs()

	inputfile = os.path.expanduser(args.inputfile)


	# Verify the input file exists
	if not os.path.exists( inputfile ):
		logger.info( 'The source file, %s, does not exist.', inputfile )
		exit()

	# Create the output directory if it does not exist
	if not os.path.exists( args.output ):
		os.mkdir( args.output )

	epub = EPUBFile(args.inputfile)	
	logger.info ('Number of spine %s', len(epub.spine))
	if epub.title:
		name = _title_escape(epub.title) + '.tex'
		outputfile = os.path.join(args.output, name)
	else:
		name = _title_escape(os.path.splitext(inputfile)[0]) + '.tex'
		outputfile = os.path.join(args.output, name)

	with codecs.open( outputfile, 'w', 'utf-8' ) as fp:
		fp.write( epub.render() )
	document = epub.document
	
	# Since document only has one body
	global_glossary = {}
	body = document.children[0]
	glossary_file = os.path.join(args.output, 'glossary.json')

	#create a txt file to store information about image's name and location used in nticard
	__builtin__.nticard_images_filename = os.path.join(args.output, 'nticard_images.txt')

	#to write attribution required on copyright terms
	start_attribution = int(args.indexatt)
	appended_text = u''
	attribution = unicode(args.attribution)
	atthref = unicode(args.atthref)
	
	#if attribute link contains percentage '%', it will always be like '\%'
	atthref = string_replacer.modify_string(atthref, u'%', u'\\%')

	if attribution is not None and atthref is not  None:
		appended_text = u'\\subsection{Attribution}\n\\textbf{%s \\href{%s}{%s}}' %(attribution, atthref, atthref)
	elif attribution is not None and atthref is None:
		appended_text = u'\\subsection{Attribution}\n\\textbf{%s}' %(attribution)
	elif attribution is None and atthref is not None:
		appended_text = u'\\subsection{Attribution}\n\\textbf{\\href{%s}{%s}}' %(atthref, atthref)

	for index_child, _ in enumerate(body):
		# append file tex information to nticard_images_filename
		if index_child == 0:
			with codecs.open(__builtin__.nticard_images_filename, 'w', 'utf-8') as fp:
				fp.write('file_'+str(index_child)+'.tex:\n')
		else:
			with codecs.open(__builtin__.nticard_images_filename, 'a', 'utf-8') as fp:
				fp.write('file_'+str(index_child)+'.tex:\n')

		# write each body child into different latex file
		# we use this format : file_1.tex
		outputfile = os.path.join(args.output, 'file_'+str(index_child)+'.tex')
		logger.info('------------')
		logger.info(outputfile)
		tex_content, glossary_dict = epub.render_body_child(index_child)
		with codecs.open( outputfile, 'w', 'utf-8' ) as fp:
			fp.write(tex_content)
		if glossary_dict is not None:
			global_glossary.update(glossary_dict)
			glossary_check.process_glossary(glossary_dict, outputfile)
		logger.info('------------')

		#write required attribution in each chapter 
		#appended_text (attribution text and link) can be different for each books
		if index_child > start_attribution and attribution is not None:
			with codecs.open(outputfile, 'a') as f:
				f.write(appended_text)


	# clean global glossary
	glossary = clean_global_glossary(global_glossary)

	# save glossary to json
	glossary_json = json.dumps(glossary, sort_keys=True, indent=4 * ' ')
	with codecs.open( glossary_file, 'w', 'utf-8' ) as fp:
		fp.write(glossary_json)
	epub.get_media(args.output)

def clean_global_glossary(glossary):
	for key in glossary.keys():
		value = glossary[key]
		new_value = value.rstrip('\n')
		glossary[key] = new_value
	return glossary

if __name__ == '__main__': # pragma: no cover
	main()
