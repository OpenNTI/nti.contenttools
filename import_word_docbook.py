#!/usr/bin/env python2.7

import os
import re
import sys

from contentimport.fix_latex import fix_latex
from contentimport import fix_unicode
from contentimport.import_docbook import convert_docbook

def first_pass(line):
    # Discover document structure
    # Mark chapters
    p = re.compile( r'^\\label{TOC[0-9]*}[I][I]*\.[A-Z][A-Z]*\.[0-9][0-9]* ' )
    if p.search( line ) is not None:
        line = r'\chapter{' + line.replace( '\n', '' ) + '}\n'

    # Mark sections
    p = re.compile( r'^\\label{TOC[0-9]*}[I][I]*\.[A-Z][A-Z]*\.[0-9][0-9]*\.[0-9][0-9]* ' )
    if p.search( line ) is not None:
        line = r'\section{' + line.replace( '\n', '' ) + '}\n'

    # Mark References as a section
    p = re.compile( r'^\\label{TOC[0-9]*}References' )
    if p.search( line ) is not None:
        line = r'\section{' + line.replace( '\n', '' ) + '}\n'

    # Mark subsections
    p = re.compile( r'^[I][I]*\.[A-Z][A-Z]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]* ' )
    if p.search( line ) is not None:
        line = r'\subsection{' + line.replace( '\n', '' ) + '}\n'

    return line

def import_word(lines):
    output = []

    lines = convert_docbook(lines)
    lines = fix_latex(lines)

    for line in lines:
        line = first_pass(line)

        output.append(line)
    return output

if __name__ == '__main__':
        data = []
        # Get the input
        with open( sys.argv[1:][0], 'rb' ) as input:
                data = input.readlines()

        # Process the input
        output = import_word(data)

        # Output the processed data
        for line in output:
                sys.stdout.write(line)
