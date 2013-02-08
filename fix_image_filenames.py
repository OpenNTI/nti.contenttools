#!/usr/bin/env python2.7

import re, glob, os

def renamer(files, pattern, replacement):
    for pathname in glob.glob(files):
        basename = os.path.basename(pathname)
        new_filename = re.sub(pattern, replacement, basename)
        if new_filename != basename:
            print("Renaming " + basename + " to " + new_filename)
            os.rename(pathname, os.path.join(os.path.dirname(pathname), new_filename))

if __name__ == '__main__':
#    renamer( "*.png", r'_', r'-' )
    renamer( "*.png", r'\s', r'-' )
#    renamer( "*.pdf", r'_', r'-' )
    renamer( "*.pdf", r'\s', r'-' )
