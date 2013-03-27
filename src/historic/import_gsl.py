#!/usr/bin/env python2.7

import os
import sys

from contentimport.fix_latex import fix_latex
from contentimport.fix_unicode import fix_unicode
from nti.contentrendering import gslopinionexport

def import_gsl(lines):
    output = []

    lines = fix_unicode(lines)
    output = fix_latex(lines)

    return output

if __name__ == '__main__':
        data = []
        # Get the input
        with open( sys.argv[1:][0], 'rb' ) as input:
                data = input.readlines()

        # Process the input
        output = import_gsl(data)

        # Output the processed data
        for line in output:
                sys.stdout.write(line)
