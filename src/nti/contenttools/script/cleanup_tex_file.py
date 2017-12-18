#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import codecs
import argparse


def parse_args():
    arg_parser = argparse.ArgumentParser(description="Update image in figure environment")
    arg_parser.add_argument('inputfile',
                            help="Input File")
    arg_parser.add_argument('-ct', '--cleanup_type',
                            default='subsubsection',
                            help="The output directory. The default is: %s" % 'subsubsection')
    return arg_parser.parse_args()


def update_image_with_aspect_ratio(text, ratio):
	regex = re.compile(r'ntiincludeannotationgraphics\[width=.[\d]*px,height=.[\d]*px\]')
	result = regex.findall(text)
	result_set = set(result)
	result = sorted(result_set)
	for substr in result:
		regex2 = re.compile(r'width=.[\d]*px|height=.[\d]*px')
		subresult = regex2.findall(substr)
		
		width = subresult[0]
		width_idx_start = width.find(u'=') + 1
		width_idx_end = width.find(u'px')
		width_number = width[width_idx_start:width_idx_end]
		
		height = subresult[1]
		height_idx_start = height.find(u'=') + 1
		height_idx_end = height.find(u'px')
		height_number = height[height_idx_start:height_idx_end]

		if int(height_number) > 600:
			new_height_number = 600
			ratio = 600.0/float(height_number)
			new_width_number = ratio * int(width_number)
			new_width_number = int(new_width_number)
		else:
			new_height_number = int(ratio * int(height_number))
			new_width_number = int(ratio * int(width_number))

		new_substr = substr.replace(width_number, str(new_width_number))
		new_substr = new_substr.replace(height_number, str(new_height_number))

		text = text.replace(substr, new_substr)

	return text

def cleanup_subsubsection(text):
	regex = re.compile(r'\\subsubsection\{.*\}\\\\')
	result = regex.findall(text)
	result_set = set(result)
	result = sorted(result_set)
	for substr in result:
		new_substr = substr.replace(u'\\\\', u'')
		text = text.replace(substr, new_substr)
	return text

def main():
    # Parse command line args
    args = parse_args()

    # Verify the input file exists
    inputfile = os.path.expanduser(args.inputfile)
    if not os.path.exists(inputfile):
        print('The source file, %s, does not exist.', inputfile)
        exit()
   
    with codecs.open(inputfile, 'r', 'utf-8') as fp:
    	try:
    		text = fp.read()
    	finally:
    		fp.close()

	cleanup_type = os.path.expanduser(args.cleanup_type)
	if cleanup_type == u'image':
		ratio = 0.95
		text = update_image_with_aspect_ratio(text, ratio)
	elif cleanup_type == u'subsubsection':
		text = cleanup_subsubsection(text)

	with codecs.open(inputfile, 'w','utf-8') as fp:
	 	fp.write(text)


if __name__ == '__main__':  # pragma: no cover
    main()