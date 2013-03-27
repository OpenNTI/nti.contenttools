#!/usr/bin/env python2.7

import glob, os, subprocess

if __name__ == '__main__':
    for pathname in glob.glob('*.eps'):
        basename = os.path.basename(pathname)
        print("Converting " + basename)
        subprocess.call(["epspdf", basename])
