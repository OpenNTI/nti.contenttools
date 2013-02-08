#!/usr/bin/env python2.7

import os
import re
import sys

from contentimport.fix_latex import fix_latex
from contentimport import fix_unicode
from contentimport.import_docbook import convert_docbook

def import_flatworld(lines):
    output = []

    for line in lines:
        # Fix image paths
        p = re.compile( r'http://images.flatworldknowledge.com/[A-Za-z0-9]*/' )
        line = p.sub( r'images/', line )

        # remove custom image commands
        p = re.compile( r'\\imgexists{[A-Za-z0-9./_-]*}' )
        line = p.sub( '', line )

        p = re.compile( r'\\imgevalsize{[A-Za-z0-9./_-]*}' )
        line = p.sub( '', line )

        # Protect any underscores in filenames
        m = None
        p = re.compile( r'(images/[A-Za-z0-9./_-]*)' )
        m = p.search( line )
        if m is not None:
            orig = m.group(1)
            final = orig.replace( '_', r'-' )
            line = line.replace( orig, final )

        # Properly scale images
        line = line.replace( r'width=full' , r'width=6in,height=8in' )
        line = line.replace( r'width=largel' , r'width=5in,height=7in' )
        line = line.replace( r'width=large' , r'width=5in,height=7in' )
        line = line.replace( r'width=medium' , r'width=4.25in,height=5.5in' )
        line = line.replace( r'width=small' , r'width=2.125in,height=2.75in' )

        output.append(line)

    return output

def import_docbook(lines):
    output = []

    lines = convert_docbook(lines)
    lines = import_flatworld(lines)
    output = fix_latex(lines)

    return output

if __name__ == '__main__':
        data = []
        # Get the input
        with open( sys.argv[1:][0], 'rb' ) as input:
                data = input.readlines()

        # Process the input
        output = import_docbook(data)

        # Output the processed data
        for line in output:
                sys.stdout.write(line)
